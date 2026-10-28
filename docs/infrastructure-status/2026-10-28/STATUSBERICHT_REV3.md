# Konsolidierter Statusbericht KI-Engineering-Infrastruktur
28.10.2026 · Rev.3 · Review-Snapshot / global INCOMPLETE

## 1 Auftrag, Methode und Erfassungsgrenzen

Der Bericht konsolidiert die KI-Engineering-Infrastruktur für Julian Zotter zum 28.10.2026. Grundlage sind der Statusbericht vom 15.03.2026, Dashboard-Roadmap Rev. 2 vom 09.04.2026, Septemberberichte, Oktober-Indizes, ausgewählte HTML-Quellen und das private Repository julianzotter/nexus-platform. Dokumentstatus: Vorabzug zur Freigabe / Review-Snapshot.

Die vier vollständigen Tree-Dateien wurden als Originalbytes gelesen und mit Windows-1252 dekodiert. Aus ihnen werden vollständige Pfadregister für den überlieferten Juli-Snapshot erzeugt. Die gezielte Drive-Ordnersuche wurde über alle Providerseiten ausgeschöpft. Sie ersetzt keinen rekursiven Vollscan sämtlicher Cloud- und lokaler Speicherorte.

Gelesene Quellen belegen Dokumentaussagen. CODE_PRESENT bedeutet sichtbarer Code; TESTED_SCOPED benötigt einen abgegrenzten Test; DEPLOYED_VERIFIED benötigt einen identifizierten Betriebslauf. Historische Kennzahlen werden nicht zum heutigen Ist-Stand hochgestuft. Dateien und Normtexte wurden überwiegend als Metadaten erfasst, nicht fachlich oder auf Transkriptionsvollständigkeit geprüft.

## 2 Konsolidierter Status und Entwicklung

März: 44 KB-Ordner, 201 katalogisierte Unique-Dateien, 0 % systemweite RAG-Indexierung und 4 von 14 als produktionsreif bezeichnete GPTs. Diese Werte sind historische Berichtsaussagen. Bereits dort steht produktives JSON-Retrieval für BRAND neben 0 % Indexierung: lokale Retrieval-Funktion und flächendeckender Index sind verschiedene Größen.

April Rev. 2: Sprint 1 wird als abgeschlossen dokumentiert. 21.296 Dateien und 43,16 GB stammen aus sechs dateitypbezogenen Listings. Die 201 kuratierten Dateien bleiben eine getrennte Schicht. Die Kennzahlen des älteren Mock-Dashboards sind kein belastbarer Ist-Vergleich.

September: Parser und Graph-Extractor sind dokumentiert; fünf Graph-Fixturetests wurden berichtet. Der Konflikt 1.409 versus 755 Kanten bleibt offen. Der Bericht trennt Freigabe, Code, Test und produktiven Betrieb ausdrücklich.

Oktober: Repository enthält bestehende Registry, Monitor, Drive-Poller und Dashboard-Snapshot-Vertrag. Der 27.10.-Bericht nennt ACB-Fixturetests und fehlende zentrale Python-Solver. Ein Artefakt oder grüner Workflow bestätigt weder produktiven Datenaustausch noch erfolgreiche Engineering-Bemessung.

| Stand | Belegter Erfassungsgegenstand | Nicht daraus ableitbar |
|---|---|---|
| 15.03.2026 | 44 KB / 201 kuratierte Dateien | heutiger Gesamtbestand |
| 09.04.2026 | 21.296 Dateien / 43,16 GB aus Listings | vollständige semantische Erschließung |
| 28.09.2026 | 1.468 Eingabeobjekte / 733 Knoten / 755 Kanten, berichtet | aktueller E2E-Betrieb |
| 28.10.2026 | 30985 Tree-Einträge und 162 gefundene Ordnerobjekte | vollständiger aktueller Datenbestand |
| Nutzer-Screenshot | 2.880.408 AnythingSearch-Einträge im Speicher | validierte DB-Zeilen, Unique-Dateien oder RAG-Chunks |

## 3 Bestandsarchitektur und verbindende Wegweiser

Drive bleibt Dokument- und Wissensablage; GitHub verwaltet versionierten Code, Schemas und Konfiguration. Die neue Auswertung ist eine abgeleitete Sicht und ersetzt weder bestehende Masterregister noch Ledger.

Die aktuelle Dokumentation beschreibt WORK unter LLM-LOCAL-SSOT, AI-CODEBASE, AI-ENGINEERING-KNOWLEDGEBASE, AI-PYTHON-PARSE, _INDEX.MASTER, _INDEX und _INDEX_LNK. Gleiche Namen mit verschiedenen Drive-IDs bleiben getrennte Objekte. Ein Ordnername mit LNK beweist keinen funktionsfähigen Shortcut.

Verlinkte Einstiegspunkte: https://drive.google.com/drive/folders/1oWX4JbZlJkUZJWwgSA_KxuFJRemvZoxK (_INDEX.MASTER); https://drive.google.com/drive/folders/1zf1aNaIFo0dJ8wQpDnJzWnvgVt2ASx66 (05-INDEX+LISTS+TREE); https://drive.google.com/drive/folders/1YgSdE8x2nelUcHQ_FhPAraoKPmlB-7AM (AnythingSearch).

## 4 Vollständiger Index innerhalb des erfassten Snapshot-Umfangs

QUELLENREGISTER_DATEIEN.csv enthält alle sicher veröffentlichbaren Datei- und Ordnerzeilen der vier vollständig gelesenen Tree-Dateien mit rekonstruiertem Windows-Pfad, Quell-ID, Originalzeile, Root, Erweiterung, Wissensclustern und Prüfstatus. Versteckte Konfigurationspfade und potentielle Zugangsdaten werden nicht weiterveröffentlicht. Namensgleichheit wird nicht als Dublettenbeweis verwendet.

ORDNERREGISTER.json enthält sämtliche 162 Objekte der vollständig paginierten gezielten Drive-Suche. Enthalten sind Parent-IDs und Links. KB-Nummern sind historisch mehrfach vergeben und teils geändert; dauerhafte Identität wird über Provider-ID und nicht KB-Präfix geführt.

Für den aktuellen globalen Vollindex ist der konsistente AnythingSearch-Snapshot weiterhin erforderlich. Die vorliegenden Register sind im deklarierten Umfang vollständig verarbeitet, global aber INCOMPLETE.

| Root | Erfasste Metadatenzeilen |
|---|---|
| AI-ENGINEERING-KNOWLEDGEBASE | 10659 |
| AI-CODEBASE | 5465 |
| AI-PYTHON-PARSE | 14715 |
| AI-WISSENS_INDEX | 146 |

## 5 KB-Ordnerstruktur: gefundene Ordnerobjekte

Alle in der gezielten Suche gefundenen KB-Ordner sind nachfolgend aufgeführt. Mehrere Einträge mit gleichem Namen bleiben erhalten. IDs und vollständige Links stehen im beigefügten ORDNERREGISTER.json; ein Fund belegt die Existenz des Objekts, nicht dessen fachliche Vollständigkeit.

| KB-Ordner | Drive-ID |
|---|---|
| KB-000-AI-VIBE-CODE-DASHBOARD | 1e4dzSRwgPxa7DGltvalG3Bl9qCLYfTgq |
| KB-000-BACKUP | 1Va3p06mBwK0rkAbtpqLseks-YPaV-wmh |
| KB-000-BWBp128a | 1S9UYz99cykzn0dTg48t81fsOlIbrgwO8 |
| KB-000-ChatGPT-EXPORT | 1rXnL5JvdYM00qgUhe9LgwZbDBxZsS4sf |
| KB-000-Custom-GPT-Repos | 1fE7oh4Ilh0ddbJh6BU5YUFUJH9V83n0u |
| KB-000-FFG eCALL ffg.at | 10F5QoGUpYCfKLMQ0rAORtO77ujQlJ_tQ |
| KB-000-GPT-IMPLEMENTIERUNG | 1vFShMXv9TdU18TnnSPuTfIT6zcQFfuqi |
| KB-000-SYSTEM | 1NW2Js4aDpnVJCrnH4GCOkCqT6RRjO6h- |
| KB-000-SYSTEM-ZIPS | 1fvTRl4Hlo33xYbMZQuoxwMIh-9_IWXDF |
| KB-001-AI-DATA-SYSTEMS+CDQ+SUPERBASE | 18eqBnhcFStgzUa1kZUDlXwO_tAaZ6CGR |
| KB-001-BAURECHT | 1jLbE-mQzmHnY3Et9WfOaL-uJzd0eEhVf |
| KB-001-GPT-TCC-CODEBASE | 1RVBlxBccvBrRE_yMn_TtCS_RVWuMtwaK |
| KB-001-HBV-GPT | 14nta4SRvxQgsTiDpRFuMqF5Xdv31CtJL |
| KB-001-PROMPT-SNIPPETS | 1u0sif4Wpc-c8HOM3bL_ER93PP6mNz1yV |
| KB-001-PROMPT-SNIPPETS | 1y1qavfERKBk4zYuO0QbB4w-ioL-r5Z92 |
| KB-001-SERIELLE-BAUSYSTEME | 10s-jZH4J3ZkRQ07ymoDs_b1wX6s-qkR9 |
| KB-001-TCC-PYTHON-CHUNKS | 1QuIfME14XosoobZHvJ_CvlHBy2fvaX-L |
| KB-002-AI-LLM-Engineering-GPTs+RAG-KB | 1664HqanXlnMXyUSNkDr-CT6Eb1jm2iIA |
| KB-002-AI-LLM-Engineering-GPTs+RAG-KB | 1JVdHYL-juUq2ncKifbg071MdYGUBFwDY |
| KB-002-ÖKO BAUSTOFF GPT (ökolog. Baustofflexikon) | 1TviTsWtHyXUyT-3tFzLzyvfD6XRBlHku |
| KB-003-HOLZ-GPT | 1OHfYPYhKF9TN2mPRrmkUFqvg64Mhs5u- |
| KB-004-BETON-GPT | 1LZSemufpBjQ22poscBVjG3VvOeDYxh9- |
| KB-005-STAHL-GPT | 1S7iBD1bv12DE2lxLBpyU5YorxBy-kX1T |
| KB-006-BRAND-GPT | 17OPsZLKpb5CInAdQeVEM4CmoCVlwlwsV |
| KB-007-DZDXF+IFC+CAD+BIM+AEC+VRML+RFEM-GPT | 1gVFfmyQZk1viZDHjGj8xVZGz3CXo8jt2 |
| KB-008-Plan-Korrektur-GPT | 19USHGw9Cv4poc5sTFxc4IYWdrT8lACDc |
| KB-009-HRW-FASSADEN-ELEMENTE | 1T6Vcog5dulYGVpbSAcorcTEy8HB6QiCA |
| KB-010-SERIELLE-BAUSYSTEME-Verknüpfung-0f5e9d27968b | 11QDKUMx4efdxtjdlYHVHj79hyx5_sHBY |
| KB-010-SERIELLE-BAUSYSTEME-Verknüpfung-0f5e9d27968b | 1rZjdAnDePLNnmUITyAmJhCBnDro_9ue1 |
| KB-011-STATIK+PI-HOB-S | 1xs3qIwYdejEaG9v-2hy_zOkGuoI-WERY |
| KB-012-SIGEPLAN-BAUKG | 18POTN2ZtSdQYe1sdQrI2D-5R3r3_IeBY |
| KB-013-LV-GPT | 1XQeD5aY0Nkf4G6rENPn_CjNT2D258ZQI |
| KB-014-EISTEICHE | 1STlPxcQIVRzVdofwi7cUzBnQjCSgoQY0 |
| KB-015-BAUKOSTEN | 1t-QpPIDuFdRmeV7H3w2mnK-fq979WOd- |
| KB-016-SIGNAL-MATRIX-DESIGN | 1c9mAP8nbd3YgR6HCxoavwXtxNXVg0RuX |
| KB-017-GenAI-GODMODE+WEBCRAWLER | 1-wGRG3G95wNuhtTCIbsRi31_BsI27Fh3 |
| KB-017-GenAI-GODMODE+WEBCRAWLER | 1zMsP96YULM1WizH2O8MiMjQQLHW8tZBZ |
| KB-018-ProjectPlanner-GPT | 1JoUSOtLDuAwdTQyF-XaB5seBA-iTPn3r |
| KB-020-HUMAN-AI-STRUCTURAL-ENGINEERING-COLLABORATION-KIT | 1mkY-Mla-GUirF1Yefco0vl_nCq3_d95y |
| KB-021-OPEN-ACCESS-LEAPSPACE | 1-sOZWYN-WVR-L5q8C5PmA96K1sRksyNI |
| KB-022-TEXTEN-mit-KI-CHAT-GPT_KAI_SPRIESTERSBACH | 177bvqv-3dAVkP4qRUHZnd3G5j6AHa1yb |
| KB-023-LITERATUR | 1_AfzFN8-fLmcVjB6IVjT3U51LOIwIKwa |
| KB-024-CEPA-SOLUTION | 1VkR7xWHwPtnhBlehqk_q2zjjJN-NRLCX |
| KB-025-EGGER-HOLZ | 1qrrOWRbTJrUnFWjVdYPaQciQxn4IbPXs |
| KB-026-OEKO-BILANZ-DATA-Kreislauf-Baustoffe | 1Tb7xSYZHOpkLGAj1uGDfTdcRVLoApoF5 |
| KB-027-WIEHAG-AI-ENGINEERING | 15IYZvOwTfAsZdj3DGRIm6WN-ezDrYcti |
| KB-028-DETAILS-HOLZ | 1vSYEBq_IVs3kwmha0KcwcpiVlk0iz-CK |
| KB-029-EA-RECHNG-DATEN | 1wKHN5Zhto7SH6BI9YnaByN4w_kgQo_jE |
| KB-029-EA-RECHNG-DATEN-99-RECHERCHEORDNER-91ab10a282c1 | 10bAxXoHbNzLOmf3DGNT-oJZLlhpn8qBF |
| KB-029-EA-RECHNG-DATEN-99-RECHERCHEORDNER-91ab10a282c1 | 1bF17H4Rah7cWbqyeRC_Nw-i3lupkWRlV |
| KB-030-OPENCLAW-PeterSteinberg | 1rVW3LQ3uDoJr2uotrl7qUhOD11BAh45L |
| KB-031-QWEN | 1S6PUnCCH1iQTxSHd3VxfgXjGcpak5eOq |
| KB-032-OR1ON | 1rUuutbGRDF0k7UU2bK4kmvMhg0-kxZOL |
| KB-040-GPT-Developement-OneDrive | 1ZWTL7AInt8UdYvgk03N8chHsLkT4okJH |
| KB-041-SUPER-GPT-REPOSITORY | 1_b-Twyvz0NGoOirNXK12QPgeXYbkDq6q |
| KB-042-HBV-GPT-CHUNKS-ATLAS | 1eADFXFjVgK4dl4rBCwikT5xuA2OB8wRY |
| KB-043-REUSE HBV | 1g0AD1LB5ISLOaO81KavAFe2YNh603lGO |
| KB-044-BETONBAU-GPT | 1xC_I-ii6oVSHtm4tnF3SL-WtLWY-mefj |
| KB-045-REUSE | 1n4HqUdOzwx_eFM1yEXnMGgh5OhSURLzl |
| KB-046-AI-DATA-Management+MultiAgentSystem-GPT | 1_9jf339BQrauWHyqy6hlnFK-5mQYYx_g |
| KB-047-TAHLBAU GPT | 1lDfvKGGDu8WNWyVwOEjxot4KHwZ3PAbU |
| KB-048-Ökobaustoff-GPT | 1jw7btDQp4X_txIXDz7hnEgNYr_NKLBO8 |
| KB-049-BAUKG+SIGEPLAN GPT | 1lrz5QSHOVhLbBV20zfukZi7Ffy1foTIm |
| KB-050-CEPA SOLUTION GPT | 1V7LnTBqRaLj_k9azcsAZzUoqOsC8uf4S |
| KB-050-GEOTECHNIK | 1HwLcHRQxB1nm5l_ddJS6h4WinWRCWXXg |
| KB-051-CUSTOM GPTS in open.ai gpt.builder | 1MbPtFjYIiRN8b7XxdGXlKHLQ4N9dV1WJ |
| KB-052-KI Anwendungen im Bauwesen | 12ouW3B-zKdalblN_zhBGK_GOkrzWD5Mk |
| KB-053-PromptEngineeringBase-GPT | 1kYflRDsWUa7ycUtvE04neJdEF4HUqWS5 |
| KB-054-Künstliche Intelligenz im Bau | 1MfYoGyi0fxEmvdrPXtFZZZ5kmqKaFkXe |
| KB-055-STROHLEHM GPT | 158mk_Zn-4zTpl0J7mMghrjzivv-8I49c |
| KB-056-UBAKUS GPT | 1zAENJIlevkCG3MNPDc1qWrhsA7olbGaK |
| KB-057-WEBSCRAWLER GPT | 1YfpnT8rymhlEOmQd4bqeUzjkjrr2nqSo |
| KB-058-DETAIL-Planungs-GPT | 1q6HOdBzTkl8ge39xGSsmn1Gtslhpi4Zd |
| KB-059-HOLZ-HOLZ-VERBINDUNGSSYSTEME | 15P-Wo8S6u3EGiU6ziE5JQ62r3BuJLWb6 |
| KB-060-Midjourney Prompt Bibliothek | 1YksW4TzVa0dwX6N6dXFQXfEO4-4RltOX |
| KB-061-NEWs+INFOS+PodCast-GPT | 1PW1amozkYcyKItKe0jjK2ZGG7niF5cSd |
| KB-062-TIMBER JOINTS | 1g-RthcdQ_fiW2C5YlvmSRRZpbYYBwEPV |
| KB-063-LessonsLearnedBase-GPT | 1ywMieyd89rRFZ_7mw0O5UreJtTJuz2iu |
| KB-064-Ruben Esparza - CLT-Highrise-Residential-Building | 1o4OKZmXXiysAGZwS7fOXZjugvIo1aYQW |
| KB-100-DATENSAMMLUNG | 1090P-be9JVaHgJNmB79LxHHS7vuyc7vR |
| KB-102-KI-im-BAUWESEN | 13ZfEYxnWW44PQKkPbE_JtzfQm76-F3x7 |
| KB-103-SCANS+SCREENSHOOTS | 1ZA6Ig3AsbE1z-ozX0mrj1UFFnebAUdQz |
| KB-104-PRESSE-ARCHIV-ZT-KAMMER | 111aQL7mHOW-uNbBxs2KA_xzotMOkis4a |
| KB-105-ARCHITEKTUR+BAUKULTUR-PICS | 1wDghDKZT4WuTyD6f6VRTTb8eq6b-Pxrs |
| KB-888-MODELLVERGLEICH-Plus+Business-Pro | 1R2DzFFmTqJtXgPR12GeK72AhaPhIj-Gn |
| KB-999-JUL | 1GDLMtMk8Z8R0xdIWoOCopO-GOey4B00C |
| KB-BILDER | 1icpuMEHZnFpAPHD5UPl2iuXh7O8iRKDo |
| KB-LINKTREE.DIRECTORYS | 1grrbiGPEQqn6RtcK2hMo3qg4Oj72mkpy |
| KB-OIB_RL2 | 16ivKsEK3KQNxylt8bgJr5S9t_bUGhQR6 |
| KB-PARSING-PIPELINE | 12t4oznSwu8JWwf2zUMu01qRMSXRPHbD2 |
| KB-RECHERCHE_OFFEN | 1a3pUqrF8YhllME10QubEBezifaofvaVL |
| KB-SCAN | 1_GbgCofInAw0pfEk5p0LX6FZSlanaJSt |

## 6 AI-Ordnerstruktur und Masterlisten

Die vollständige historische Unterstruktur ist im CSV über root und kind=folder filterbar. Die vier Wurzeln bilden Engineering-Fachwissen, Code/Prompts, Parser und Wissensindex ab. Nicht alle Unterordner sind heute live bestätigt.

_INDEX.MASTER.txt vom September listet Tree- und DIR-Snapshots für C:, D:, E:, OneDrive, Dropbox und Drive sowie AI-CODEBASE_TREE, AI-PYTHON-PARSE_TREE, AI-ENGINEERING-KNOWLEDGEBASE_TREE und KB-spezifische Trees. Die Liste ist ein Wegweiser zu Erhebungen mit unterschiedlichen Stichtagen.

NEXUS_MASTER_SOURCE_INDEX_v0.3 vom Oktober und die bestehende Repository-Registry werden referenziert; sie werden nicht mit der Juli-Dateiliste zu einer neuen kanonischen Master-Registry verschmolzen. Rohdatei-ID, Knowledge-Object-ID, Version und Inhalts-Hash bleiben getrennte Felder.

## 7 Wissenscluster, Domains und Use Cases

Die Zuordnung im Register erfolgt nachvollziehbar anhand von Pfad- und Namensbegriffen. Sie ist ein Routinghinweis und keine semantische Validierung. Mehrfachzuordnungen sind beabsichtigt; Clusterzahlen dürfen nicht zu einer Gesamtzahl addiert werden.

| Domain | Use Cases / notwendiger Nachweis |
|---|---|
| EC2 Betonbau | Biegung, Querkraft, Durchstanzen, FT-Träger, Öffnungen; Solvercode, Einheiten, Referenzfälle und Testlauf verknüpfen |
| EC5 Holzbau | ULS/SLS, Stabilität, Verbindungen, CLT; Materialquelle, nationale Parameter und Benchmark identifizieren |
| HBV / TCC | Gamma-Verfahren, diskrete Methode, Schlupf/Kerben; Kser-Definition und Einheiten prüfen |
| EC3 Stahlbau | Querschnitt, Knicken, Biegedrillknicken, Anschlüsse; Implementierungsumfang pro Modul |
| CAD / BIM / FEM | DXF/IFC, Mengen, RFEM5/6, Austausch und Revisionsvergleich |
| Parser / Normen | Original -> seitenverankerte Transkription -> MD/JSON -> Formelobjekte -> Prüfung |
| AI / RAG | Prompt- und Skillregister, Retrieval mit Quellenankern, Extraktionsevaluation |
| Governance / Betrieb | IDs, Ledger, Manifest, Änderungsprotokoll, Zuständigkeit, Refresh und Fehlerstatus |
| Bauphysik / Nachhaltigkeit | Brandschutz, Feuchte/Wärme, Ökobaustoffe, LCA/ESG, Reuse und Bauteilbörsen |

## 8 Normen, Volltexttranskriptionen und Code

EN-Serie und ÖNORM-B-Serie werden als eigene Quellenklasse geführt. Erforderliche Metadaten: Normnummer, Ausgabe, Land, nationaler Anhang, Originaldatei-ID, Recht/Nutzungsstatus, Seitenanker, OCR-Methode, Prüfumfang und abgeleitete MD-/JSON-/PY-Beziehungen. Eine Datei mit passendem Namen beweist weder aktuelle Anwendbarkeit noch vollständige Transkription.

MD dient lesbarem Wissen; JSON strukturierten Objekten, Schemas und Provenienz; PY implementierten Algorithmen; PDF/DOCX bewahren Quellen und Satz. Ein PY-Fund bestätigt keinen erfolgreichen Import oder korrekten Solver. Ableitungen erhalten DERIVED_FROM zum Original und einen eigenen Versionshash.

Die ausgewählten AnythingSearch-Listen EC2 und EC5 enthalten konkrete Python-Kandidaten, darunter ec2_beam_specialized.py, ec2_custom_gpt_repo-v2.py und timber_pipeline. Das zentrale Repository hatte laut 27.10.-Bericht diese externen Solver noch nicht integriert. Die Listen belegen Suchkandidaten mit Pfad und Datum, keine Rechenfreigabe.

Dieser Auftrag erzeugt keine neuen Norm-Volltexttranskriptionen und keine statischen Berechnungen. Er katalogisiert vorliegende Hinweise und schafft den prüfbaren Einstieg für die nächste gezielte Inhaltserschließung.

## 9 Dashboard-Bestand und aktualisierte Roadmap Rev. 3

Die Rev. 2 vom 09.04.2026 ist im Inhalt bestätigt. Die Suche ergab neuere HTML-Artefakte bis 26.10.2026; ein jüngeres Datum allein beweist keine Ablösung der April-Linie. Der neue HTML-Bericht bündelt Status, Filterregister, Ordner und Roadmap als eigenständige Offline-Datei.

Bestehende Architektur wiederverwenden: schemas/dashboard-snapshot.schema.json und tools/export_dashboard.py liefern den dokumentierten versionierten Snapshot-Vertrag; prototypes/data-dashboard bietet dateibasierten Import und lokale Filter. Diese Integrationspunkte haben Vorrang vor einer weiteren unabhängig gepflegten Registry.

| Priorität | Arbeitspaket | Abnahme |
|---|---|---|
| P0 | AnythingSearch konsistent bereitstellen | SQLite backup, quick_check, Schema, Snapshotdatum, WAL-Herkunft dokumentiert |
| P0 | Masterlisten und Cloud-Pfade abgleichen | Parent-Ketten und Provider-IDs; Scope/Pagination je Root vollständig |
| P0 | Rev.3 Register und Status anzeigen | Filter, Quellenanker, Export; UNKNOWN statt künstlich grüner KPIs |
| P1 | Schema/Parser prüfen | MD/JSON/Formeln mit Seitenankern und Fehlerfällen; keine Verlustfreiheitsbehauptung ohne Vergleich |
| P1 | Solver verknüpfen | ein echter EC2/EC5/HBV-Referenzfall mit Codecommit, Input, Output, Toleranz und Run |
| P1 | Snapshot-Vertrag nutzen | Producer/Consumer-Version und Digest; beobachtetes Datum bleibt erhalten |
| P2 | Knowledge Graph real integrieren | nur belegte Kanten mit Herkunft; Kandidaten getrennt |
| P2 | Projekt-Audits und RAG-Evaluation | Mylius/Eisteiche/Böblingen mit Scope; Retrieval-Testset und Quellenabdeckung |
| P2 | Dauerbetrieb abnehmen | Fehler-/Löschfälle, Credentials, Zielreadback, ACK; gesonderte Freigabe |

| Dashboard / Stand | Prüfbefund / Verwendung |
|---|---|
| NEXUS Dossier RUN04 / 26.10. | HTML-Quelltext gelesen; eingebetteter Volltext/Blueprint; keine Ausführung geprüft |
| Technisches Dossier / 26.10. | HTML-Quelltext gelesen; UI-Dossier, kein Live-Betriebsnachweis |
| NEXUS_PARSE v1.1 / Oktober | HTML-Quelltext gelesen; externe chart.js/marked-CDNs, nicht vollständig offline |
| P3 Registry / 13.10. | Manifest berichtet 860 Inventarzeilen, 443 Primaries, 48 angereicherte Zeilen; kein eigener Recount |
| prototypes/data-dashboard | README gelesen: Offline-HTML, CSV/JSON Import; vorhandenen Baustein wiederverwenden |
| Loop 3D Consumer | Repo-Dokumentation beschreibt schema-validierten Snapshot-Import; Betriebsfreigabe offen |

## 10 Data-Refresh und AnythingSearch-Anbindung

AnythingSearch.db ist ein Dateimetadatenindex. anythingllm.db ist eine andere Anwendungsdatenbank und kein Ersatz. Die vom Nutzer genannten DB/WAL/SHM-Pfade sind Routingziele, kein hier zugänglicher Mount. Die gezielte Drive-Suche nach DB/ZIP lieferte keinen Snapshot; der gefundene Database-Unterordner war leer.

Die Routine umfasst eine regelmäßige Delta-Recherche über Drive und GitHub sowie ein ausführbares lokales SQLite-Werkzeug. Es öffnet die Quelle nur lesend, erstellt per SQLite-Backup einen konsistenten Snapshot, führt quick_check aus, prüft Files/Folders-Spalten und exportiert das Metadatenregister. WAL/SHM werden nicht als unabhängige Datenquellen zusammenkopiert. Die Quell-DB wird nicht verändert.

Der vorhandene GitHub-Poller arbeitet bereits mit changes.list und Page-Token; laut gelesenen Oktoberberichten war er BLOCKED_DRIVE_CREDENTIALS. Eine zusätzliche Automation ersetzt diesen Nachweis nicht. Ein wöchentlicher Quellencheck kann neue Berichte finden und den Delta-Bericht aktualisieren; lokaler Auto-Watch bleibt ein gesonderter Hostbetrieb.

## 11 Konflikte, Lücken und nächste konkrete Schritte

Offen sind der konsistente aktuelle SQLite-Snapshot, die vollständige heutige rekursive Cloud-Erfassung, Normtranskriptions-QA und echte Solver-/Retrieval-End-to-End-Läufe. Die Existenz heutiger Ordner und der historische Inhalt der Trees werden deshalb getrennt angezeigt.

KB-Nummerierung: Märzzuordnung und heutige Namen differieren, beispielsweise LV und Projektplanung. Keine automatische Umbenennung; eine Alias-/Migrationsmap referenziert alte Namen auf dieselbe Provider-ID, soweit belegbar.

Governance: WORK/Folder.md dokumentiert offene externe Integrations- und Freigabegates. Die neue Fassung ist ein Review-Snapshot und ändert weder Zugriffsrechte noch bestehende Betriebsfreigaben. Ein unabhängiger Review dieses neuen Gesamtpakets wurde in diesem Lauf nicht ausgeführt.

Empfohlene Reihenfolge: konsistenten DB-Snapshot erschließen; Root-/Masterlisten-Abgleich abschließen; einen Normtext und einen Solver als Golden Slice durchgängig prüfen; erst danach RAG- und Graphkennzahlen als neue Ist-Werte ausweisen.

## 12 Quellenregister und Herkunft

Alle tatsächlich gelesenen Dokumente und Tree-Originale stehen mit Hashscope in QUELLENREGISTER_DOKUMENTE.json. Die unveränderten Roh-Trees werden wegen potentieller vertraulicher Konfigurationsnamen nicht im Versandpaket weitergegeben. Das abgeleitete Register enthält nur freigegebene Metadatenfelder und gefilterte sichere Pfade.

Die folgenden URLs sind Original-Wegweiser. Die Juli-Trees sind die Grundlage der vollständigen historischen Register, die Oktober-Ordnersuche liefert den begrenzten heutigen Metadatenstand.

| Quelle | Original-Link |
|---|---|
| NEXUS-DASHBOARD-INTEGRATION.md | https://github.com/julianzotter/nexus-platform/blob/main/docs/NEXUS-DASHBOARD-INTEGRATION.md |
| 26_10_20_16_32_NEXUS-SYSTEMSTATUS_v1.37.0.md | https://drive.google.com/file/d/1oEcA7qmDkRhFkFUNWXMtDfl2p_XiiKIK/view |
| 26_10_11_MAIN-DRIVE-FOLDERS. GITHUB-SYNC+BACKUP-REPOS(NEXUS-AI-OS).md | https://drive.google.com/file/d/17bJuKzj9sgRMu1bHIJRAHSAPKzSaugHi/view |
| README.md | https://github.com/julianzotter/nexus-platform/blob/main/prototypes/data-dashboard/README.md |
| inventory-summary.txt | https://github.com/julianzotter/nexus-platform/blob/main/registry/inventory-summary.txt |
| KONSOLIDIERTER STATUSBERICHT SEED CONTEXT.txt | https://drive.google.com/file/d/1Ac-z2h9Q0vMakV13_V5SBrb2oLO6y1gh/view |
| NEXUS-GOVERNANCE-CURRENT-STATE-2026-10-25.md | https://github.com/julianzotter/nexus-platform/blob/main/docs/NEXUS-GOVERNANCE-CURRENT-STATE-2026-10-25.md |
| 26_10_03_AnythingSearch-Index-EC5-HOLZ.txt | https://drive.google.com/file/d/1FZBogewisesFd9yVSIpjxfAAN044G8T6/view |
| 2026-10-13_NEXUS_DASHBOARD_REGISTRY_P3_MANIFEST.md | https://drive.google.com/file/d/1k7KLPq9paq3hlKh0GK4wCniNF7LJQHwc/view |
| 26_10_03_AnythingSearch-Index_EC2-BETON.txt | https://drive.google.com/file/d/1hp5Wb2WaWDOPDiAz-sxhTSffd2Kk8sE1/view |
| NEXUS_TECHNISCHES_DOSSIER_DASHBOARD_RUN04_v1.0_2026-10-26.html | https://drive.google.com/file/d/1uV39f5vgOelDj-d4Pzy42RqzkWvj8O38/view |
| 26_10_17_NEXUS_MASTER_SOURCE_INDEX_.txt | https://drive.google.com/file/d/1tFVq-3GmLu4FldDgr-E3U6lhwZFP_f69/view |
| 00_KONSOLIDIERTER-EINSTIEG.md | https://drive.google.com/file/d/1eV-QfTe5qENLZK9jPTJ-X4IWDLJv_oOL/view |
| 26_10_26_nexus_ai_os_technisches_dossier_dashboard.html | https://drive.google.com/file/d/1Ubo4DEl70yYQlPPjEOsrCHcHI3DeHdQT/view |
| 26_10_27_1815_ID06_WO-GOV-ACB-ENG-STATUSBERICHT_0127.md | https://github.com/julianzotter/nexus-platform/blob/main/WORK/REPORTS/26_10_27_1815_ID06_WO-GOV-ACB-ENG-STATUSBERICHT_0127.md |
| 26_09_28_NEXUS_Konsolidierter_Statusbericht_NEU.docx | https://drive.google.com/file/d/1hPXyjL_oLIpD8v_T2yMi7bV2LKjN6Ykx/view |
| NEXUS_Konsolidierter_Statusbericht_2026-09-28.docx | https://drive.google.com/file/d/1uPAEvlLRYWLFcHXzcdbYz5JoPShD9Lag/view |
| drive_changes_poll.py | https://github.com/julianzotter/nexus-platform/blob/main/tools/drive_changes_poll.py |
| _INDEX.MASTER.txt | https://drive.google.com/file/d/12yavwDPVcokfxhMW6JAlUIupwFjVPlAU/view |
| AGENTS.md | https://github.com/julianzotter/nexus-platform/blob/main/AGENTS.md |
| Arbeitsplan_Roadmap_WISSENS_Dashboard_v2.docx | https://drive.google.com/file/d/1HH1B927AIhTuES8W_w_AHCKaSddrYqfM/view |
| NEXUS_PARSE_DASHBOARD_v1.1.html | https://drive.google.com/file/d/1nO2sET4YI7wYtgU5S-0b0xBVBdYwSB5N/view |
| AI-ENGINEERING-KNOWLEDGEBASE_TREE.txt | https://drive.google.com/file/d/1C7RHeCfO2hSnsZh5f3OH-T3YXnOzDIR5/view |
| AI-CODEBASE_TREE.txt | https://drive.google.com/file/d/1KjochvARFNJPTosvVsu67SGqZSH4jKZz/view |
| AI-PYTHON-PARSE_TREE.txt | https://drive.google.com/file/d/1mEjjGCWkWAfDrvQEan53fnyb--LwO49C/view |
| AI-WISSENS_INDEX_TREE.txt | https://drive.google.com/file/d/1UNNpOEeUUN5pKpXJ5ACOZS0dphn38ZrV/view |