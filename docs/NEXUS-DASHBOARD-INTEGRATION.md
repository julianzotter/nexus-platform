# Platform ↔ Dashboard integration / v1

Status: implementation for review; snapshot transport, no production or human release.

## Responsibilities

- `julianzotter/nexus-platform`: canonical repository schemas, file registry, knowledge items, deterministic monitor, snapshot producer.
- `julianzotter/NEXUS-AI-ECOSYSTEM-LOOP_3D-STUDIO-VISUALS-DASHBOARD-`: consumer, provenance inspection, knowledge orbit and lifecycle display. New canonical entrypoint: `index.html`. Existing HTML/Python variants remain historical prototypes and are not invoked by this entrypoint.
- Drive WORK remains document SSOT according to its current Folder policy. This integration does not create a second registry, an automatic cloud writer, a feedback training loop or a bidirectional sync service.

## Executable transport

The existing NEXUS Monitor workflow now exports `reports/monitor/nexus.snapshot.json` and its SHA-256 sidecar into its existing run/attempt artifact, even when monitor checks fail. An invalid report or knowledge record fails export and leaves no prior snapshot at that output. Existing `report.json` and `report.md` remain unchanged and available for diagnosis.

1. Download `nexus.snapshot.json` from an observed Actions artifact and import it using the dashboard file picker. This works without transferring GitHub or Drive credentials to a browser.
2. For local checkouts at a committed revision, run the monitor and then in the dashboard checkout:

```sh
npm ci
npm run sync:platform -- ../nexus-platform
npm run dev
```

`sync:platform` reads the platform Git HEAD, refuses dirty registry/schema/exporter inputs, calls the producer and writes only local dashboard `public/nexus.snapshot.json`. Select “Lokalen Export laden”. Re-run synchronization after a new monitor report; mismatched report/checkout revisions are rejected. `NEXUS_PYTHON` can identify a Python interpreter with jsonschema installed. Windows paths containing spaces are supported through argument arrays, without a shell.

## Versioned contract

`schemas/dashboard-snapshot.schema.json` defines `nexus-integration/1`. The dashboard vendors an exact schema copy and digest lock. Changes require a coordinated version decision and both test suites. The exporter uses the existing knowledge validator, rejects duplicate object IDs and missing source-file references, projects only explicit fields and includes hashes of the exact monitor and knowledge-record bytes. `source_sha256` is registry metadata, not proof of current external source access. The sidecar protects comparison of local bytes when checked against a trusted receipt; it is not a signature.

The producer preserves `observed_at` from the report; `generated_at` cannot refresh the observation. Commit identity must match the explicit source revision. No check logs, provider keys, full note bodies or fabricated graph edges are exported. Objects keep DRAFT/VALID/SUPERSEDED; this state is not newly awarded by export.

## Backward compatibility and gates

The dashboard also accepts native `1.0.0` monitor reports and existing `nexus-controller/1` packages. Native monitor input carries no knowledge nodes or transport receipts. Controller input preserves its own delivery, ACK, human acceptance and lifecycle gates. Inputs are imported separately rather than merged across timestamps or revisions. Unknown versions, contradictory check states, malformed hashes and duplicate knowledge IDs are rejected. On import failure the prior displayed result is cleared.

Observation age >2 hours is labelled VERALTET; >5 minutes into the future is ZEITKONFLIKT. These are UI freshness thresholds, not execution SLAs. File import validates structure and consistency, not the authenticity of an arbitrary uploaded JSON document. A successful workflow or HTTP health endpoint cannot override an INCOMPLETE result or imply engineering approval.

## Acceptance and remaining release work

- Producer → schema validation → UTF-8 file/hash → JavaScript consumer; tests cover incomplete/failure states, draft objects, source/commit mismatch and invalid input.
- Dashboard builds with a lockfile; its CI tests the consumer and compiles historical Python variants without executing them.
- Private cross-repo cloud polling, durable feedback storage, delivery authentication and external writer activation are separate work. No credentials or sharing settings are changed.
- Release requires the three review perspectives, delta consolidation/review and explicit human decision required by AGENTS.md. These changes are review candidates, not a production release.

Governance read for this implementation: current WORK Folder.md `11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH`, policy 0.4.0-pilot; Workorder Addendum v1.1.0 `132LgGmEDN3OqQFItB9NIEZNi8Frcrc43`. The HBV fixture workorders are preserved and not represented as completed by this integration.
