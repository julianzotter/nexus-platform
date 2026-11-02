---
name: NEXUS_AI_SYSTEM_SHARED_LANGUAGE_GLOSSARY
version: 2026-11-02-supplement-1
status: CANDIDATE_WITH_ID01_PERSISTENCE_SUPPLEMENT
timestamp: '2026-11-02T19:35:00.111567+01:00'
agent_id: ID02
executor: OpenAI Codex
executor_instance: /root
artifact_id: gdrive:1MnHMlbPgKRNUlSiW7SzRk20EvLrSLEOJ
ticket_id: WO-20261102-NEXUS-PERSISTENCE-GATE
hash_scope: body_utf8_after_closing_frontmatter_lf
hash: e38f5e19be69fb9bf0da4082f7e85443b26bb266a8fb4766429ce7e844565c31
---
# NEXUS-AI SYSTEM — SHARED LANGUAGE & GLOSSARY

**Status:** consolidated system glossary candidate · 2026-10-27
**Canonical repository path:** `docs/GLOSSARY.md`
**Purpose:** ubiquitous language across NEXUS tasks, agents, skills, evidence, gates, knowledge, deterministic solvers, runtime, delivery, governance and Critical Gate Watch.

## Existing canonical core vocabulary

| Term | Meaning |
|---|---|
| **Task** | Scoped unit of work with owner, acceptance criteria, dependencies and a human gate (`schemas/task.schema.json`). |
| **Agent** | Role with an explicit list of allowed skills and tools. |
| **Skill** | Folder/module with manifest, input/output schemas, tests and an owner. |
| **Evidence** | Measured, reproducible fact backing a claim (e.g. command, tool version, timestamp). Never pre-filled. |
| **Gate** | Human approval/control step (ID-01 in the canonical glossary). No automatic merge. |
| **Knowledge item** | Registered unit of knowledge with a stable ID shared with the NEXUS-AI-AEC knowledge graph. |
| **Norm** | Standard clause (Eurocode, ÖNORM, DIN, …) with edition, national annex and validity status. |
| **Solver** | Deterministic, unit-tested calculation. LLMs orchestrate/call solvers; they are not the arithmetic authority. |
| **Run** | One execution of a task/workflow, recorded with inputs, outputs and scores. |
| **Delta** | Difference between a run and its baseline; drives the smallest required fix. |
| **Score** | Measured accuracy, confidence and cost of a run. |
| **INCOMPLETE** | Source/metric that could not be measured; reported as incomplete and never guessed. |

## Critical Gate Watch extension

## 1. Core language

  -----------------------------------------------------------------------
  Term                                Operational definition
  ----------------------------------- -----------------------------------
  **SSOT --- Single Source of Truth** Designated authoritative source for
                                      a defined information domain. Newer
                                      or more accessible does not
                                      automatically mean authoritative.

  **Kanonisch / canonical**           Authoritative under applicable
                                      NEXUS governance. Noncanonical
                                      inputs may support review but MUST
                                      NOT silently override canonical
                                      state.

  **Evidence / Nachweis**             Inspectable support for a claim:
                                      e.g. commit SHA, workflow run,
                                      artifact, hash, Drive metadata,
                                      ledger entry, authenticated ACK or
                                      human decision.

  **Primärnachweis**                  Evidence emitted/owned directly by
                                      the system/component whose state is
                                      being asserted.

  **Gate**                            Explicit control condition
                                      requiring defined evidence before a
                                      downstream transition/action is
                                      permitted.

  **Fail-closed / `FAIL_CLOSED`**     Missing, contradictory or
                                      incomplete critical evidence
                                      produces no positive gate/release
                                      decision.

  **P0**                              Highest criticality in the Watch.
                                      Source example: WORK ACL
                                      `anyone:writer`.

  **P1**                              High-priority blocking
                                      control/operational defect. Source
                                      examples: native-delivery failure,
                                      scheduler liveness gap, ledger/SSOT
                                      conflict, overdue human checkpoint.

  **Delta**                           Verified change relative to the
                                      preceding Watch baseline. Known
                                      unresolved blockers are not
                                      automatically new deltas.

  **Regression**                      Newly introduced or newly verified
                                      deterioration of a previously
                                      better/valid state.

  **Baseline**                        Previous verified state used for
                                      delta comparison.
  -----------------------------------------------------------------------

## 2. Integrity, ledger and SSOT

  -----------------------------------------------------------------------
  Term                                Operational definition
  ----------------------------------- -----------------------------------
  **Vollhash-Readback**               Read back the complete persisted
                                      object and verify its full-content
                                      cryptographic hash, normally
                                      SHA-256, against the expected hash.
                                      Metadata-only comparison is
                                      insufficient.

  **Rohbyte-Readback**                Verification based on actual
                                      retrieved file bytes rather than
                                      filename/metadata/summary alone.

  **Kanonischer Ledger-Konflikt**     Authoritative ledger identity/state
                                      (e.g. filename, hash, `CURRENT`)
                                      contradicts verified artifact
                                      evidence.

  **SSOT-Konflikt**                   Contradiction between an
                                      authoritative source and verified
                                      system reality, or between sources
                                      expected to represent the same
                                      canonical state.

  **Ledger-Konsistenz**               Ledger IDs, versions, names, hashes
                                      and state markers agree with
                                      verified artifacts and ledger
                                      rules.

  **ID Ledger / `00_ID_LEDGER.csv`**  Governed registry mapping stable
                                      NEXUS IDs to artifact
                                      identity/version/state.

  **`CURRENT`**                       Ledger marker for the governed
                                      current version. Stale or
                                      contradictory `CURRENT` records are
                                      integrity conflicts.

  **append-only**                     Preserve history by appending
                                      successor records/versions instead
                                      of destructively replacing
                                      historical evidence.

  **CAS --- Compare-And-Swap**        Concurrency pattern accepting a
                                      write only if the prior observed
                                      state/version still matches the
                                      expected state. The source requests
                                      proof of such a writer contract;
                                      implementation is not proven there.

  **Drive-Metadaten**                 Provider properties such as stable
                                      file ID, filename, timestamps and
                                      permissions/ACL. Useful
                                      corroboration, but not a substitute
                                      for content-hash verification where
                                      byte identity matters.

  **Drive-ID**                        Stable provider object identifier
                                      independent of mutable filename.

  **WORK-ACL**                        Access-control state of the
                                      governed WORK area. `anyone:writer`
                                      is treated as critical by the
                                      Watch.

  **ACL**                             Access Control List: permissions
                                      controlling read/write/admin
                                      access.
  -----------------------------------------------------------------------

## 3. Runtime, CI and delivery

  -----------------------------------------------------------------------
  Term                                Operational definition
  ----------------------------------- -----------------------------------
  **MAIN / CI**                       Repository `main` state plus
                                      relevant Continuous Integration
                                      result. CI `SUCCESS` proves only
                                      executed CI checks passed.

  **Merge**                           Integration of a PR/branch into its
                                      target branch. Merge is a
                                      repository fact, not automatically
                                      review, governance approval or
                                      production release.

  **Branchschutz**                    Repository controls restricting
                                      changes/merges and optionally
                                      requiring reviews/checks.

  **Run**                             One concrete workflow execution
                                      identified by run ID/time.

  **Joblog**                          Execution record/output of a
                                      workflow job used to inspect what
                                      actually occurred.

  **Scheduler**                       Mechanism triggering workflows at
                                      configured times/intervals.

  **Slot**                            Expected scheduled execution
                                      occurrence/time.

  **Schedule-Liveness**               Evidence that scheduled automation
                                      executes at expected slots.

  **P1-Liveness-Lücke**               Expected scheduler slots lack
                                      execution evidence; continuous
                                      operation is therefore not
                                      demonstrated.

  **Monitor**                         Component/workflow evaluating
                                      critical gates and emitting
                                      status/evidence.

  **Monitorartefakt**                 Persisted output of a Monitor run.
                                      Its semantic content controls gate
                                      interpretation; wrapper `SUCCESS`
                                      alone does not.

  **Poller**                          Repeating component checking
                                      upstream state/events/results. Its
                                      run can technically succeed while
                                      payload status remains blocked.

  **Native Delivery**                 Intended production-like delivery
                                      path executed by native
                                      automation/integration, not a
                                      connector-assisted/manual
                                      substitute.

  **Credential-Preflight**            Pre-execution check that required
                                      credentials/secrets exist and are
                                      usable. Failure blocks delivery
                                      before E2E completion.

  **`BLOCKED_DRIVE_CREDENTIALS`**     Native Drive delivery is blocked
                                      because required credentials are
                                      unavailable/invalid/unusable.

  **E2E --- End-to-End**              Complete intended chain from source
                                      through processing/delivery to
                                      target verification.

  **E2E-Erfolg**                      Verified completion of the entire
                                      native chain including required
                                      final readback/integrity
                                      verification.

  **Native E2E Readback**             Readback through the intended
                                      native delivery path after delivery
                                      to prove target content identity.

  **Coverage**                        Completeness of required
                                      checks/gates/skills. `INCOMPLETE`
                                      coverage is not full validation.

  **Skills**                          Defined NEXUS capability/check
                                      modules invoked by workflows.
                                      `INCOMPLETE` means required
                                      output/evidence is incomplete.
  -----------------------------------------------------------------------

## 4. Status vocabulary

  -----------------------------------------------------------------------
  Status                              Deterministic interpretation
  ----------------------------------- -----------------------------------
  **`SUCCESS`**                       Referenced workflow/job completed
                                      successfully at the technical
                                      execution layer. NOT automatically
                                      gate pass, delivery success or
                                      release.

  **`FAILURE`**                       Workflow/job terminated
                                      unsuccessfully.

  **`INCOMPLETE`**                    Required coverage/evidence/output
                                      is missing. MUST NOT be promoted to
                                      PASS.

  **`BLOCKED`**                       Required completion cannot proceed
                                      because a prerequisite/blocker
                                      remains unresolved.

  **`FALSE_GREEN`**                   Outer run is green/`SUCCESS` while
                                      internal evidence is `BLOCKED`,
                                      `INCOMPLETE`, failed delivery or
                                      equivalent non-pass.

  **`NO_NEW_P0_P1`**                  No newly detected P0/P1 relative to
                                      prior baseline. Does NOT mean
                                      existing P0/P1 issues are closed.

  **`NO_NEW_TECHNICAL_P0_P1`**        No new technical P0/P1 regression;
                                      human/governance/control issues may
                                      remain open.

  **`NEWLY_DETECTED_P1` /             New high-priority issue or newly
  `NEW_P1_*`**                        verified contradiction since
                                      baseline.

  **`KNOWN_BLOCKERS_OPEN`**           Previously identified blockers
                                      remain unresolved.

  **`LEDGER_CONFLICT_OPEN`**          Known ledger inconsistency remains
                                      unresolved.

  **`NATIVE_E2E_BLOCKED`**            Native end-to-end
                                      delivery/verification cannot
                                      currently be proven successful.

  **`HUMAN_GATE_PENDING`**            Required human authorization/review
                                      decision has not been evidenced.

  **`HUMAN_GATE_REQUIRED`**           Valid next transition requires
                                      explicit human review/decision.

  **`HUMAN_REVIEW_REQUIRED`**         Human review is required before
                                      approval/release semantics may be
                                      inferred.

  **`P1_HUMAN_CHECKPOINT_OVERDUE`**   Defined human-control checkpoint
                                      has passed without required
                                      authenticated decision evidence.

  **`NOT_GRANTED`**                   Required permission/approval has
                                      not been granted.

  **`NO_PRODUCTION_RELEASE`**         Production release is explicitly
                                      not authorized/proven. No other
                                      green status overrides it.

  **`GOVERNANCE_SSoT_CONFLICT`**      Governance-controlled SSOT
                                      contradicts verified system state.

  **`NEW_P1_LEDGER_CONFLICT`**        Newly detected P1 ledger
                                      inconsistency.
  -----------------------------------------------------------------------

## 5. Governance and human control

  -----------------------------------------------------------------------
  Term                                Operational definition
  ----------------------------------- -----------------------------------
  **Governance**                      Binding rules defining authority,
                                      ownership, evidence requirements,
                                      allowed transitions,
                                      review/merge/release conditions and
                                      human decision points.

  **Human Gate**                      Control point requiring explicit
                                      authorized human decision. Missing
                                      decision is never implicit
                                      approval.

  **Consumer ACK**                    Authenticated acknowledgement by
                                      the designated downstream consumer
                                      under the applicable workflow.

  **CLAIM**                           Authenticated assertion that the
                                      assigned recipient has taken
                                      ownership/responsibility for a
                                      dispatched item.

  **ACK**                             Authenticated acknowledgement of
                                      receipt/review/acceptance as
                                      defined by the workflow.

  **Release / Produktionsfreigabe**   Explicit authorization for
                                      production use/deployment. Merge,
                                      CI success, artifact creation or
                                      delivery alone do not constitute
                                      release.

  **Owner**                           Role accountable for resolving a
                                      gate/blocker or producing required
                                      evidence.

  **Next Action**                     Explicit next required action
                                      assigned to an owner; not evidence
                                      that the action has happened.

  **ID01**                            Source role associated with
                                      governance review, ACL and
                                      Human-Gate/release decisions. Exact
                                      authority remains defined by NEXUS
                                      governance records.

  **ID03**                            Source role associated with
                                      ledger/registry correction and
                                      reconciliation. Exact authority
                                      remains governed externally.

  **ID05**                            Review/acceptance role in the
                                      source's human-checkpoint chain.
                                      Exact authority is not defined by
                                      this source.
  -----------------------------------------------------------------------

## 6. CPLM

  -----------------------------------------------------------------------
  Term                                Operational definition
  ----------------------------------- -----------------------------------
  **CPLM**                            Named NEXUS audit/reporting process
                                      in the source. The source does not
                                      provide a reliable expansion of the
                                      acronym; no expansion is invented
                                      here.

  **CPLM-Bericht**                    Versioned CPLM output documenting
                                      observed system state, blockers
                                      and/or evidence at a stated
                                      observation time.

  **CPLM-Audit**                      CPLM report used as audit input for
                                      gate verification/conflict
                                      detection. It is evidence/review
                                      input subject to canonicality and
                                      verification, not automatically the
                                      governing SSOT.
  -----------------------------------------------------------------------

## 7. Named Next Actions

  -----------------------------------------------------------------------
  Assignment                          Meaning
  ----------------------------------- -----------------------------------
  **CI-Ops → Schedule-Liveness**      Restore or prove expected scheduled
                                      executions and close unexplained
                                      missing slots.

  **Repository-Admin → Native         Provide authorized runtime
  Delivery**                          prerequisites/credentials and
                                      produce a verifiable native E2E
                                      delivery/readback.

  **Repository-Admin → Branchschutz** Establish/verify required
                                      protection controls for `main`
                                      under governance.

  **ID03 → Ledger-Korrektur**         Reconcile artifact IDs, names,
                                      hashes and version states while
                                      preserving history.

  **ID01 → ACL-Entscheidung**         Authorized governance decision on
                                      WORK access control.

  **ID01 → Human-Gate**               Explicit authorized human
                                      review/release decision. Automation
                                      may not infer it.
  -----------------------------------------------------------------------

## 8. Critical semantic rules

1.  `workflow SUCCESS` **≠** `gate PASS`.
2.  `CI SUCCESS` **≠** `Native Delivery SUCCESS`.
3.  `Merge` **≠** `Review` **≠** `Production Release`.
4.  `NO_NEW_P0_P1` **≠** `NO_OPEN_P0_P1`.
5.  `INCOMPLETE` or missing critical evidence ⇒ **FAIL_CLOSED**.
6.  `formal SUCCESS + internal BLOCKED/INCOMPLETE` ⇒ **FALSE_GREEN**.
7.  Connector-assisted readback **≠** native delivery E2E proof.
8.  Metadata consistency **≠** full-content integrity.
9.  Missing ACK/CLAIM/Human-Gate evidence **≠** implicit acceptance.
10. New documentation **≠** new runtime/delivery/release evidence.
11. Known blocker remains open until positive resolution evidence is
    verified.
12. Conflicting canonical state ⇒ raise SSOT/ledger conflict; do not
    silently reconcile.

## 9. Machine-readable state hierarchy

``` yaml
observation:
  evidence: [VERIFIED, INCOMPLETE, CONFLICT]
  delta: [NO_NEW_P0_P1, NEW_P0, NEW_P1, RESOLUTION_VERIFIED]
  gate: [PASS, INCOMPLETE, BLOCKED, FAIL]
  human_gate: [NOT_GRANTED, PENDING, GRANTED]
  release: [NO_PRODUCTION_RELEASE, RELEASE_GRANTED]

precedence:
  rule: "positive downstream state requires all mandatory upstream evidence/gates"
  missing_or_conflicting_evidence: FAIL_CLOSED
```

## 10. Interpretation boundary

This glossary formalizes terminology **as used by the supplied Critical
Gate Watch source**. Where the source does not define an acronym,
authority or implementation contract completely (notably the expansion
of `CPLM`, exact ID01/ID03/ID05 authority, and full CAS/writer-contract
semantics), this document does not invent one.


## Persistenz, gemeinsames Verständnis und sichere Entwicklung — ID01 2026-11-02
Status dieser Ergänzung: direkte ID01-Anweisung, abgeglichen mit AGB v005. Bestehender Glossarkorpus bleibt in seinem bisherigen Kandidaten-/Referenzumfang; keine pauschale Neuerklärung zum kanonischen Master.

| Begriff / Domänentyp | Präzise Bedeutung / Abgrenzung |
|---|---|
| Google Drive API | Providerschnittstelle für Driveoperationen. Ein API-Aufruf ist eine konkrete Ausführung, noch kein Beweis des vollständigen Auftragsabschlusses. |
| MCP-Connector | Werkzeug-/Integrationsweg; kann Provider-APIs aufrufen. Die Connectorantwort muss auf tatsächlichen Providerzustand geprüft werden. Kein Synonym für Drive API. |
| Drive-Datei-ID | Identität einer Providerdatei, getrennt von Inhalt, Revision, Tool- oder Request-ID. Eine syntaktisch passende ID allein bestätigt keinen neuen Schreibvorgang. |
| Tool-/Request-ID | Identität eines Werkzeugaufrufs/einer Anfrage. Kein automatischer Dateinachweis und keine Rollenidentität. |
| Rohbyte-Readback | Rücklesen vollständiger untransformierter Dateibytes. Extrahierter Markdown-/Dokumenttext ist kein Ersatz für Bytegleichheit. |
| SHA256 / Hashbereich | Deterministisch berechneter Digest eines ausdrücklich benannten Bytebereichs. Vollfilehash und Bodyhash sind getrennte Nachweise. |
| WRITTEN_UNVERIFIED | Providerwrite bestätigt, Rohbyte-/Integritätsprüfung noch nicht bestätigt. |
| FILE_VERIFIED | Vollständiger Rohbyte-Readback mit SHA256-Gleichheit sowie bestätigter Ziel- und stabiler Versionsstand; Registry-/Review-/Releasebedingungen können weiter fehlen. |
| REGISTRATION_PENDING | Passender Eintrag/Readback im bestehenden file-registry.jsonl noch nicht bestätigt. Datei kann trotzdem real vorhanden sein. |
| PERSISTED_VERIFIED | Im angegebenen kontrollierten Pfad bestätigte zusammengehörige Datei-/Versions-/Hash-/Registerkette; keine Humanfreigabe, globale Garantie oder zukünftige Unveränderbarkeit. |
| Validierungsgate | Deterministische Prüfung im vertrauenswürdigen Ausführungspfad. Ein Prompt ist eine Verhaltensanweisung, kein technisch erzwingender I/O-Lock. |
| Idempotenz | Wiederholung derselben gebundenen Operation erzeugt kein unbeabsichtigtes zweites Ergebnis. Geänderte Inputs mit derselben Operations-ID ergeben Konflikt; eine Datei-/Artefakt-ID darf bei erlaubten neuen Versionen gleich bleiben. |
| Exklusiver Writer | Tatsächlich durchgesetzte Schreibzuständigkeit. Ein Konfigurationsflag oder lokaler Lock beweist keine Exklusivität aller Cloudschreiber. |
| Sicherer Testmodus | Autorisierte unabhängige Entwicklung, Lesen, lokale Tests und reversible WORK-Kommunikation laufen trotz dokumentierter Richtlinien-/Nachweislücke weiter; keine Löschung/E-Mail oder unbelegte Erfolgs-/Freigabeaussage. |
| Personal Memory / Personal Settings | Tatsächliche dauerhafte plattformspezifische Erinnerungs-/Instruktionsfläche; keine pauschale Garantie modellübergreifender Verwendung. Eine Chatnotiz, WORK-Datei oder behauptete Sessionerinnerung ist kein Nachweis einer solchen Mutation. |

### Shared Understanding — operative Invarianten
1. Kommunikation und sichere Entwicklung kontinuierlich fortführen. Ein fehlgeschlagenes Gate sperrt den betroffenen kritischen Schritt/Claim, nicht das gesamte NEXUS-System. Abweichungen mit Wiener Timestamp, Rollen-ID, Teilstatus und nächster Aktion in textbasiertem WORK-Markdown melden.
2. Lokale Datei ≠ Browserdownload ≠ Drivewrite ≠ Rohbyteprüfung ≠ Registrierung ≠ Peerreview ≠ technischer Release. Statusachsen nie ineinander übersetzen.
3. Alle neuen Begriffe im bestehenden Glossar mit Definition/Quelle/Status nachführen; UL und SU sind das gemeinsame Begriffs- und Bedeutungsverständnis. Vorhandene Masterregister bleiben erhalten.
4. Separate reale Reviewerinstanz erforderlich; zwei Rollenlabels sind keine Unabhängigkeit. Veröffentlichung ≠ Zustellung ≠ ACK.
5. Dieser Nachtrag speichert nichts in persönlichen Kontoeinstellungen und aktiviert keine fremde LLM-Runtime.

Quellen: ID01-Anweisungen im aktuellen Chat vom 2026-11-02; AGB v005 https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view; Manifest §4/6/10 und Baseline MUST-50–54/60–68/150–159.
