# Quellen und Aussagegrenzen

Recherche-/Abrufkontext: 27.10.2026. Die Quellen begründen Architektur- und
Werkzeugentscheidungen; sie zertifizieren weder diesen Code noch einen Solverlauf.

| ID | Primärquelle, Version/Fundstelle | Verwendete Aussage |
| --- | --- | --- |
| S01 | Alistair Cockburn, *Hexagonal Architecture*, 2005, Intent/The Pattern: https://alistair.cockburn.us/hexagonal-architecture/ | Ports/Adapter und Isolation von Laufzeitgeräten |
| S02 | Robert C. Martin, *The Clean Architecture*, 13.08.2012, Dependency Rule / Crossing boundaries: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html | Quellcodeabhängigkeiten nach innen, DTOs über Grenzen |
| S03 | Matt Pocock, *How To Make Codebases AI Agents Love*, aktualisiert 26.02.2026: https://www.aihero.dev/how-to-make-codebases-ai-agents-love | Deep Modules mit kleinen kontrollierten Schnittstellen |
| S04 | Stewart Brand, *Pace Layering*, 17.01.2018: https://longnow.org/ideas/pace-layers/ | Unterschiedliche Änderungsgeschwindigkeiten; keine konkreten NEXUS-Jahresintervalle |
| S05 | Python, `dataclasses`, Frozen instances / field inspection: https://docs.python.org/3/library/dataclasses.html | Frozen ersetzt keine vollständige Wertvalidierung oder tiefe Unveränderlichkeit |
| S06 | Python, `typing`, runtime_checkable: https://docs.python.org/3/library/typing.html#typing.runtime_checkable | Annotations-/Protocol-Grenzen; keine fachliche Richtigkeitsgarantie |
| S07 | Import Linter, Layers / Multi-item layers: https://import-linter.readthedocs.io/en/stable/contract_types/layers/ | Unabhängige Geschwister über Pipe-Syntax |
| S08 | Import Linter, Configuration: https://import-linter.readthedocs.io/en/v2.9/get_started/configure/ | include_external_packages im globalen Abschnitt |
| S09 | JSON Schema Draft 2020-12, Core/Validation: https://json-schema.org/draft/2020-12 | Generierte Strukturschemata; zusätzliche Fachvalidierung ist Implementierungsentscheidung |
| S10 | Pydantic, Type Adapter: https://docs.pydantic.dev/latest/concepts/type_adapter/ | Alternative externe Validierung/Schemaerzeugung aus Dataclasses möglich |
| S11 | dataclasses-jsonschema, Projektstatus/Feature Overview: https://pypi.org/project/dataclasses-jsonschema/ | Wartungsmodus und dokumentierte ältere Schema-Dialekte |
| S12 | PyNite, Members / Tension-Compression Only: https://pynite.readthedocs.io/en/latest/member.html | Zug-only ist nicht gleich Formfindung; räumliche Stab- und Ergebnissemantik prüfen |

## Klassifikation

- VERIFIED: unmittelbar in der genannten Primärquelle dokumentierte Aussagen;
  tatsächlich beobachtete lokale QA-Ergebnisse laut `qa/report.json`.
- DERIVED: NEXUS-Modulstruktur, SI-Profil, Validierungsregeln, Capability-Profile,
  lokales Hashprofil und Umfang dieses Pakets.
- UNVERIFIED: Eignung für ein konkretes Herstellerprogramm/Projekt, fachliche
  Vollständigkeit für beliebige AEC-Systeme, numerische Ergebnisse und Normnachweise.

Die Quellenversionen der lokalen QA-Abhängigkeiten stehen separat in
`requirements-qa.txt` und `qa/report.json`. Ein Online-Link zu einer fortgeschriebenen
Dokumentation ist kein unveränderlicher Quellsnapshot.
