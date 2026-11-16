# NEXUS-AEC Knowledge Seed v1 — REVIEW CANDIDATE

Status: `IMPLEMENTED_OFFLINE_COMPONENTS` / `NOT_INGESTED` / `NOT_RELEASED`.
Source of authority: ID01 → CURRENT Manifest and Baseline → `_AGBS.md` v006 → WORK `Folder.md` 0.4.0-pilot.

## Input analysis and changes

- Previous chat: TOP20 target domains (rank 1–20). No persistent, verified TOP20 artifact located in bounded Drive/repository searches before this version.
- Attached `Eingefügtes Markdown(9).md`: generic Crawl4AI/Playwright/Scrapy proposal, including malformed concatenated Python code and an anti-bot stealth proposal; not adopted as executable code. Crawl access controls must not be bypassed.
- Existing GitHub `docs/integrations/2026-10-30-ids-dataholz-review-candidate.md`: authoritative prior **design candidate** for dataholz IDS; no IDS bytes or G0–G5 approvals verified here. Reused, not overwritten.
- Already active weekly automation `Meta-Wissen Holzbau Weekly` (Mon 08:00, Europe/Vienna). Extend this single task; do not create duplicate runs.

## Main goals and three implementation lanes

| Priority | Lane | Source chain | Deterministic deliverable | Release gate |
|---|---|---|---|---|
| P0 | OIB/Material/Nachweise | OIB jurisdiction → dataholz assembly → EOTA ETA/EAD → baubook/product evidence | Versioned material/assembly records, source locators, declared SI units | Confirm applicable state/edition and technical classification |
| P0 | LCA/Zirkularität | baubook/ÖKOBAUDAT EPD → IBO ZiFa → EUR-Lex criteria | EPD module/declared unit mapping and DfD/reuse evidence per layer | Verified EPD/module scope and method version; no synthetic GWP |
| P0 | Automatisierung/RFEM | TU Wien research → reviewed calculation contract → Dlubal gRPC Python API → RFEM runtime | Read-only model-data contract, audited JSON results and test harness | Working licensed RFEM runtime, official API compatibility, independent verification |

## Repository artifacts

- `seed/nexus_aec_top20_seed_v1.json`: TOP20 registry **candidates**, retrieval cadence, access policy and cross-links. It is not a replacement for the NEXUS canonical file-registry or AnythingSearch metadata index.
- `schema/knowledge_record_v1.schema.json`: separate evidence/units/edition contract. Typical values (not prefilled) are conductivity `lambda` W/(m·K), density `rho` kg/m³, vapor factor `mu` [-], fire classification, fire resistance R/REI [min], `Rw` [dB], E-modulus [N/mm²], EPD `gwp` [kg CO₂-eq per declared unit] and stage (`A1-A3` to `D`), reversible connections, service life [a], layer group and method version. Units MUST be asserted by the data source; the schema does not convert or certify them.
- `scripts/validate_seed.py`: checks uniqueness, referential integrity, HTTPS host identity, safe-access flags; optional separate, no-overwrite SQLite catalogue.
- `scripts/validate_knowledge.py`: additional binding-date/Bundesland and canonical-unit/EPD-declared-unit checks. JSON Schema formal validation additionally requires a JSON Schema 2020-12 engine.
- `scripts/meta_wissen_digest.py`: converts already source-verified observations into a reproducible weekly digest (dedup; no invented changes).
- `tests/`: offline regression tests. Neither script crawls web sites or executes structural analyses.

## Source-of-truth and cross-reference rules

1. `SOURCE → URI/ID → edition/date/licence/hash → EXTRACT → KNOWLEDGE RECORD → QA → registry promotion`. Each property retains a source-specific locator. Unknown values remain `null`, never imputed from similar components.
2. `OIB`: edition plus adoption in **each Austrian Bundesland**, effective date and applicability. OIB RL7 draft from June 2026 / 2027 consultation must be recorded as `DRAFT`, **not** binding; official status [OIB 2027](https://www.oib.or.at/kernaufgaben/oib-richtlinien1/richtlinien/oib-richtlinien-2027/) and [adoption overview](https://www.oib.or.at/kernaufgaben/oib-richtlinien/).
3. `dataholz`: prior IDS ingestion proposal [GitHub candidate](https://github.com/julianzotter/nexus-platform/blob/main/docs/integrations/2026-10-30-ids-dataholz-review-candidate.md), [publisher](https://www.dataholz.eu/bauteile/ids.htm). Do not assign IDS validity/coverage until bytes, version and schema compatibility are verified; match IFC/IDS according to [buildingSMART](https://standards.buildingsmart.org/).
4. `EOTA`: [current ETAs](https://www.eota.eu/etassessments) and [EADs](https://www.eota.eu/eads) link product assessment to declared performance. ETA ≠ Eurocode capacity calculation or product-specific approval for unrelated construction.
5. `LCA`: [ÖKOBAUDAT](https://www.oekobaudat.de/), [baubook](https://www.baubook.at/), [IBO](https://www.ibo.at/). Distinguish generic datasets from product EPD; never sum module `D` into `A1-A3` without a declared study method. Keep GWP-fossil/biogenic/LULUC and conversion basis where available, and release/version/licence.
6. `Research`: [TU Wien HBV/TS19103 thesis](https://repositum.tuwien.at/handle/20.500.12708/210734) is methodological evidence, not itself an Austrian regulation or approved design result.
7. `RFEM`: official [Dlubal Python client](https://apidocs.dlubal.com/installation_python.html), [Application API](https://apidocs.dlubal.com/source/rst_methods/rfem_methods.html), [API overview](https://apidocs.dlubal.com/). At 2026-11-16 docs report 2.16.6 release; establish local SDK/Windows RFEM compatibility at execution. No autonomous solver calls from LLM; approved Python adapter makes deterministic API calls and stores input/output JSON with hashes.

## Execution and checkpoints

```bash
python -m unittest discover -s tests -v
python scripts/validate_seed.py --seed seed/nexus_aec_top20_seed_v1.json
python scripts/validate_seed.py --seed seed/nexus_aec_top20_seed_v1.json --sqlite /path/to/new-source-discovery.sqlite
python scripts/meta_wissen_digest.py --observations /path/to/verified-observations.json --output /path/to/new-digest.md --as-of 2026-11-16T08:00:00+00:00
```

The final two commands require user-supplied paths and verified observations; they are interface examples, not claims of execution.

### Required next gates

- G1 `SOURCE_ACCESS`: public APIs, licences, robots policy and norm rights reviewed.
- G2 `GOLDEN_SLICE`: obtain one OIB edition+state, one dataholz component, its product/ETA (when applicable), one source-valid EPD and one layer-level ZiFa record, all with locator, hash and version.
- G3 `RFEM_RUNTIME`: Windows RFEM6 gRPC live connection, controlled model read/export, RFEM-native result and independent check; do not reuse prior blocked RFEM probe as proof of operation.
- G4 `GOVERNANCE`: GitHub draft review, ID03 canonical registry/ledger entry, WORK readback SHA256, independent reviewer and explicit ID01 release. WORK `anyone:writer` security gate remains open unless separately revalidated.

No production or regulatory conformity is claimed by this version.
