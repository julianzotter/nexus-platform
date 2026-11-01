# NEXUS | IDS / IFC / bSDD / dataholz — Integration Review Candidate
Datum: 2026-10-30 (Europe/Vienna)
Status: REVIEW_CANDIDATE; NOT_INGESTED; NOT_PRODUCTION_RELEASED
Authority: ID01 request in conversation; no schema, registry, ACL, runtime or SSOT mutation implied.

## 1. Source register (candidate, not authoritative source registry)
| source_id | source | identity/version | role | status |
|---|---|---|---|---|
| SRC-IDS-BSI | https://github.com/buildingSMART/IDS | official IDS XML/XSD repository, `Schema/ids.xsd`; freeze commit SHA before execution | standard/schema | VERIFIED_LINK; VERSION_PIN_PENDING |
| SRC-IDS-STANDARDS | https://standards.buildingsmart.org/ | IDS 1.0 final | normative schema | VERIFIED_LINK |
| SRC-DATAHOLZ-IDS | https://www.dataholz.eu/bauteile/ids.htm | publisher labels dataholz_1x5.ids, published 2025-06-10, ~18 MB | property requirement dataset | VERIFIED_METADATA; BYTES_NOT_ACQUIRED |
| SRC-DATAHOLZ-FILE | https://www.dataholz.eu/fileadmin/dataholz/media/ids_1.5.ids | user-supplied direct URL; compare to publisher's 1x5 filename; identity not assumed | candidate file | UNVERIFIED_BINARY |
| SRC-BSAT-BIMCERT | https://www.buildingsmart.co.at/wp-content/uploads/2023/03/BIMcert-Handbuch-2023.pdf | §3.7 IDS | Austrian training context | VERIFIED_LINK |

Do not conflate dataholz dataset release 1x5 with buildingSMART IDS XSD standard 1.0.
Dataholz states its IDS and bSDD publication are synchronized and matching classifications/releases are required for effective checking.

## 2. Domain model and architecture
- Source identity: publisher + immutable URI + retrieval timestamp + binary SHA256 + media type + publisher release + license/terms + source_id.
- Standard identity: IDS XSD version, XSD SHA256, required IFC schema versions, validator version.
- Dictionary identity: bSDD dictionary URI + version + classification URI/code; capture as found in the IDS/IFC, not inferred from a filename.
- Knowledge object: one IDS `specification` = stable source-scoped key + applicability facets + requirement facets + cardinality + allowed values/restrictions + datatype + provenance.
- IFC binding: IFC model SHA256 + IFC schema + element GlobalId + class + classification references + property/quantity values, data type and unit.
- Check evidence: checker tool/version + ruleset SHA256 + model SHA256 + timestamp + per-specification/element PASS/FAIL/NOT_APPLICABLE/ERROR, source locations and machine-readable result.
- Registry relation: SOURCE -> RELEASE -> IDS_SPECIFICATION -> (CLASSIFICATION, PROPERTY_REQUIREMENT) -> IFC_INSTANCE -> CHECK_RESULT. Link; do not duplicate a new master.
- Scope: information requirement checking, not substitute for geometric, structural, fire, approval, or certification verification.

## 3. Deterministic pipeline (proposed, not executed)
1. Acquire the publisher IDS as opaque bytes. Record GET URI, response metadata, bytes, SHA256, license, observed publication version; compare 1.5 vs 1x5 filenames by hash before declaring equivalence.
2. Resolve and pin official IDS 1.0 XSD to immutable Git commit or standard archive; check XML safely (no external entities or network/entity expansion), validate complete IDS against XSD.
3. Parse `info`, all `specification` records: `ifcVersion`, `applicability`, `requirements`, facets `entity`, `partOf`, `classification`, `attribute`, `property`, `material`, cardinalities and restriction predicates. No silent lossy mappings.
4. Extract bSDD dictionary/classification identities and version hints; compare required dictionary/classification URIs with actual IFC assignments, fail closed if release pairing cannot be established.
5. Build normalized JSONL/Parquet candidate objects with raw XML offsets/IDs, namespaced source_id, release version, SHA256 and referential-integrity checks; retain immutable raw original separately.
6. Validate IFC using an independently identified IDS/IFC checker with pinned versions. Assert property type, predefined types, unit normalization, applicability, required/optional/prohibited semantics, and empty-applicability behavior.
7. Export read-only report with pass/fail details; require human signoff before promotion to canonical source registry, RAG indexing, design reuse or release.

## 4. Acceptance gates
- G0 Source: license reviewed; fetched raw IDS and XSD hashes; bSDD pairing traceable.
- G1 Syntax: full XSD validation, parse count and element coverage, no external entity resolution.
- G2 Semantics: lossless extraction verified against XML, cardinality/restriction/unit tests; duplicate/identifier collision gate.
- G3 Checker: reference IFC PASS, deliberately invalid IFC FAIL, wrong dictionary-version FAIL, wrong units/data types FAIL. Retain full tool receipts.
- G4 Knowledge: provenance/URI/hash/readback; index dedupe; source locators, release pinning and no fabricated property claims.
- G5 Governance: canonical WORK ledger ID, approved real Markdown filename, actor identity, three independent reviews where required, explicit ID01 promotion and security/access gate.

## 5. Current execution receipts and blockers
- VERIFIED: User supplied source URLs; buildingSMART IDS repository, XSD structure, publisher release metadata, buildingSMART Austria BIMcert manual §3.7.
- NOT DONE: raw dataholz IDS binary acquisition, size/hash/parse; full specification count; bSDD API lookup; IFC model checks; licensing; production ingest; source-registry mutation.
- DRIVE WORK: `Folder.md` (Drive ID 11Z66aRKzFHfPp2rgUYl26Yd_kA46HWgH) states SECURITY_BLOCKED and GitHub review snapshots only. `_AGBS.md` v003 (ID 10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg) requires `YY_MM_DD_HHMM_ID##_THEMA_###.md` and authorized ledger assignment. No valid new artifact_id was allocated in this execution; do not fabricate one or create a native Google Doc pretending to be raw Markdown.
- GITHUB: this file is a review candidate on a dedicated branch; it is not the canonical Drive WORK status report. No main-branch merge, CI or release claimed.

## 6. Next authorized work package
ID03 / human-controlled ledger: allocate unique artifact ID and validate actor mapping, permit a compliant UTF-8 Markdown WORK status report with byte readback, then record its Drive ID and SHA256. Engineering integration owner: pin releases, fetch original IDS, map bSDD versions, implement XML/XSD parser, test fixtures and IFC checker. Governance owner: review license, security and promotion boundaries. Commit to main only after the corresponding approvals and reproducible test evidence.
