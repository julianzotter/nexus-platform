---
ticket_id: WO-20261124-ID03-ROLES12-COPILOT
author_role: ID03
assigned_to: ID02
reviewer_account: ChatGPT Business
timestamp: "2026-11-24T22:58:21+01:00"
run_id: c7134298-77a8-45e3-b4ea-9f23fda8ecb5
status: OPEN
review_status: REQUESTED
registration_status: REGISTRATION_PENDING
---
# Auftrag an ID02 · Unabhängiger Peer-Review
ID01 beauftragt ID02 (ChatGPT Business), den Rollen- und Startmeldungs-Writeback von ID03 eigenständig zu prüfen. Der Auftrag ist in der WORK-Warteschlange veröffentlicht. Für den Rücklauf bitte Ticket-ID und geprüften Git-Stand angeben.

1. In WORK mit echtem START_ACK antworten. Rollen-ID, tatsächliche Runtime und Instanz, beobachtete Modell-ID oder null und Zugriff je Ziel/Operation samt Prüfbeleg angeben.
2. Jede der vier Drive-IDs als Rohdatei abrufen. SHA-256 gegen die folgenden Werte prüfen. Den Vorgängersnapshot heranziehen. Im aktuellen Regeltext ID02 Business, ID03 Private und Chief Orchestrator, gleichen administrativen Rang und ID01-Freigabe kontrollieren. Historische eingebettete Quellen und der ENTWURF-Status des Frontmatters bleiben erkennbar.
3. Startpflicht und Copilot-Zuordnung im neuen Manifest und in der Baseline prüfen. Mindestens je ein positiver Nachweis und ein Fall ohne belegten Task-zu-PR-Link. Einen beliebigen PR-Head oder einen PR-Review durch einen anderen Agenten nicht als Task-Nachweis verwenden.
4. Antwort als eigenständiger WORK-Bericht mit Ticket-ID, eigener Identität, Zeit, Quell-IDs, vier selbst berechneten SHA-256, geprüftem Git-Commit, PASS/CHANGES_REQUESTED je Punkt und offenen Befunden. Den Code- und GitHub-Teil gegen den in der Statusmeldung verlinkten Review-PR prüfen. Reviewer und Autor müssen unterschiedliche Instanzen sein. Bei fehlendem Zugriff den konkreten Teil als BLOCKED kennzeichnen.

| Drive-Original | Erwarteter SHA-256 |
|---|---|
| [_AGBS.md](https://drive.google.com/file/d/10TzHQJzmqhCjfi1CLYIQyW4J2kyryFqg/view) | `4e0efb661676747f286734f17d490106ccfe6fd179ba54324dd8454fa6b71738` |
| [_FRONTMATTER.md](https://drive.google.com/file/d/1rKnQMZbhO6ii0ThnJLhUCRYrXFcDvRbi/view) | `4755b083d1d037cbd84b2a91e77bcc171cc5d5925b01bcb604652b6732e46dbe` |
| [00_NEXUS_MANIFEST__CURRENT__2026-09-28.md](https://drive.google.com/file/d/1POfiQCWHDU_7iVMj_A2X3mxNvEjR5Lvn/view) | `09c8786b9064c1e5f7933d7b2cd2aae50a55f3637cfb99c1b1465c077910a055` |
| [00_NEXUS_BASELINE_INSTRUCTIONS__CURRENT__2026-09-28.md](https://drive.google.com/file/d/1CdwNHr6i8lMG3k8A939kiznLMw8q7J69/view) | `893bf97595b62cd3b930df78bf9b4e4de5ed162535242b8a6fa9f813cea7100e` |

[Vorgängersnapshot](https://drive.google.com/file/d/11H_r85rkEsQAMm9brsR2jRqxWmUt1_uv/view?usp=drivesdk) · [Beschluss von ID01](https://docs.google.com/document/d/1lLqeLzUrJPnKd027M7q3XFzPZvu-0AXMpAuuAsZvbu0/edit)
