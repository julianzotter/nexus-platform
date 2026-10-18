# NEXUS Runner aktivieren — OAuth, OpenAI und Branch-Schutz

Stand: 18.10.2026. Review-Snapshot; Drive bleibt Dokument-SSOT. Kein Secretwert gehört in Repo, WORK oder Chat.

## Tatsächlich ausgeführt

- PR27 mit ausdrücklicher ID01-Freigabe gemergt: `1ad8874f1bcf9a37c3807c12fdfb4afb3346ad81`.
- CI `39163269115` und Monitor `39163269102` auf diesem main-Commit erfolgreich. Coverage/Publikationsreife trotzdem unvollständig.
- Neuer OpenAI-Projektschlüssel `NEXUS-Python-Monitor-20261018` im verbundenen Platform-Projekt erzeugt, lokal mit0600 gespeichert. Modellzugriff HTTP200 bestätigt. Schlüsselwert nicht veröffentlicht; kein GitHub-Secret-Write behauptet.
- Echte Python-Inferenz mit ausschließlich synthetischem Kontrollinput erfolgreich: response_id `resp_0f9fb238a0e40e4d016ad52c7c3ef087d0ad14f95202a3b84f`; 137 Input- und137 Outputtokens. Keine privaten Repositorydaten in diesem erfolgreichen Test.
- Der Versuch mit internen Monitor-Metadaten wurde von der automatischen Sicherheitsprüfung abgelehnt. Der Code sperrt diesen Export zusätzlich durch `NEXUS_LLM_EXPORT_APPROVED`, standardmäßig nicht aktiviert.

## Warum Actions→Drive noch scheitert

Delivery-Run39162534310 (auch Nachfolger39163287347) scheiterte mit `BLOCKED_DRIVE_CREDENTIALS`. Im Job waren `NEXUS_GOOGLE_CLIENT_ID`, `NEXUS_GOOGLE_CLIENT_SECRET` und `NEXUS_GOOGLE_REFRESH_TOKEN` leer. Ein OpenAI-Key authentifiziert keine Google-API. Der verbundene ChatGPT-Drive-Zugang exportiert sein OAuth-Token nicht als Runner-Secret.

GitHub-Connector dieser Sitzung bietet keine Operation zum Setzen von Actions-Secrets; auch kein authentifizierter lokaler GitHub-CLI-Token liegt vor. Die Nutzerfreigabe ist vorhanden, der erforderliche technische Zugang fehlt. Keine neue Nutzerfreigabe für denselben Secret-Schreibauftrag erforderlich; sobald ein geeigneter authentifizierter Zugang bereitsteht, kann der vorbereitete Installer schreiben.

## Einmalige Google-Einrichtung auf dem lokalen Windows-Rechner

1. [Google Cloud Console](https://console.cloud.google.com/) öffnen; ein eigenes Projekt `NEXUS-Drive-Runner` erstellen oder ein geeignetes bestehendes wählen. Unter APIs & Services die **Google Drive API** aktivieren.
2. In **Google Auth Platform** Branding/Audience konfigurieren. Bei externer Test-App das tatsächlich zugriffsberechtigte Google-Konto als Testnutzer hinzufügen. Den realen Publishing-/Verifikationsstatus für Dauerbetrieb prüfen: Testing mit Drive-Scope ist keine dauerhafte Token-Garantie; Refresh-Token können bei externen Test-Apps nach7 Tagen ablaufen. Kein Dauerbetrieb mit ungeprüfter Testkonfiguration behaupten.
3. Unter **Clients → Create client → Desktop app** den Client `NEXUS-Drive-Runner-Desktop` anlegen und das originale Client-JSON lokal außerhalb synchronisierter Ordner speichern. Kein JSON in WORK hochladen.
4. Für diesen bestehenden WORK-Ordner verwendet der Setup-Helper `https://www.googleapis.com/auth/drive`. Dieser Scope ist **nicht auf einen Ordner beschränkt**. Die Anwendung bindet Writes an WORK-ID `1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP`; eine tatsächliche Kontogrenze erfordert einen dedizierten Writer-Account, dem nur die benötigten Bestände zugänglich sind. `drive.file` reicht ohne separate Datei-/Ordnerfreigabe an diese OAuth-App nicht automatisch für vorhandene WORK-Dateien.
5. Aktuellen Repo-Stand inklusive dieses Review-PR lokal bereitstellen. Mit Python3.12 und authentifiziertem GitHub CLI aus dem Checkout ausführen:

```powershell
python -m pip install -r tools/oauth-setup-requirements.txt
gh auth login --hostname github.com --web
python tools/configure_drive_oauth.py --client-json 'C:\NEXUS-Secrets\client_secret.json' --publish
```

Der Helper öffnet den lokalen Browser, verwendet Loopback/PKCE und fordert Offline-Zugriff an. Das Google-Konto mit WORK-Schreibrecht wählen und die Einwilligung im Google-Dialog erteilen. Diese Google-Konto-Einwilligung kann eine Chat-Freigabe nicht technisch ersetzen. Der Helper schreibt die folgenden drei Actions-Secrets ohne Ausgabe der Werte:

- `NEXUS_GOOGLE_CLIENT_ID`
- `NEXUS_GOOGLE_CLIENT_SECRET`
- `NEXUS_GOOGLE_REFRESH_TOKEN`

Eine lokale Sicherung liegt im ignorierten Ordner `.nexus-credentials/`. Auf Windows ist zusätzlich eine passende NTFS-ACL sicherzustellen; Unix-Modus0600 allein ist keine Windows-ACL-Garantie. Client-JSON und Token nicht im gemounteten Drive/Git-Repositoryarchiv verbreiten.

Alternative UI-Ziel: [Repo → Settings → Secrets and variables → Actions](https://github.com/julianzotter/nexus-platform/settings/secrets/actions). Dort exakt diese drei Secret-Namen verwenden, Werte nur aus der lokalen autorisierten OAuth-Einrichtung. Kein manueller dauerhafter Access-Token-Copy: Der Refresh-Token erneuert kurzlebige Access-Tokens.

## OpenAI-Secret in GitHub installieren

Der neu erstellte Schlüssel liegt derzeit nur in der lokalen Codex-Laufzeit, nicht auf deinem Windows-PC und nicht im GitHub-Secretstore. Er wurde absichtlich weder als Downloadlink noch im Report offengelegt. Der hier vorbereitete Helper kann ihn **in derselben autorisierten Laufzeit** nach vorhandener GitHub-CLI-Authentisierung installieren:

```bash
python tools/configure_drive_oauth.py --openai-env /workspace/scratch/a7e437474a03/nexus-health/.env.local
```

Das Ziel ist ausschließlich `julianzotter/nexus-platform`, Secret `OPENAI_API_KEY`. Secretwerte gehen über stdin an `gh secret set`, nicht über Kommandoargumente. Die aktuelle Sitzung hat dafür keinen GitHub-CLI-Zugang. Lokale temporäre Ablage ist kein dauerhaft eingerichteter Runner; sichere Installation muss vor einem Verlust der Laufzeit erfolgen. Ist dieser Schlüssel später nicht mehr erreichbar, keine Wiederherstellbarkeit behaupten: sicher neu provisionieren und den ungenutzten alten Schlüssel im Platform-Projekt widerrufen.

Repository-Variable `OPENAI_MODEL` ist optional (Default `gpt-4.1-mini`). Repository-Variable `NEXUS_LLM_EXPORT_APPROVED=true` **erst nach expliziter Freigabe des internen Datenexports** setzen. Gesendet werden nur Commit-ID, Gesamt-/Check-Status und PR-Nummer/-Zustand; keine Quelleninhalte, Namen, Normtexte, stdout/stderr oder Secrets. Die Analyse ist beratend, maximal700 Outputtokens und3 nächste Aktionen, ohne Toolausführung, mit `store=false`. PASS ohne Befund löst keine Inferenz aus. Ein fehlender Schlüssel oder Export-Gate erzeugt einen BLOCKED-Bericht; deterministische Ergebnisse bleiben maßgeblich.

## Aktivierung und Abnahme

Nach sicherer Secretinstallation und gesonderter Integration dieses PR:

1. NEXUS Monitor manuell starten; `reports/monitor/llm-advisory.json` prüfen.
2. **NEXUS GitHub to WORK** aufrufen: `source_run_id=39163269102`; nach Token-Konfiguration eine fehlgeschlagene Delivery mit Re-run jobs wiederholen. Für ein neues Dispatch auf eine alte Quelle gegebenenfalls `resume_delivery_run_id` der vorherigen Delivery angeben.
3. Paket-Hash gegen GitHub-Digest und Drive-Rohbytes vergleichen; Receipt ebenfalls zurücklesen.
4. Wiederholung muss dieselbe Paket-ID verwenden. Danach tatsächlichen Consumer-ACK und ID01-Abnahme gesondert erfassen. Kein neuer Server/Runner erforderlich: `ubuntu-24.04` ist bereits GitHub-hosted.

## Branch-Schutz — genauer Name und Anwendung

**Vorhandene Vorschlagsdatei:** `.github/nexus-branch-protection.proposal.json`.

[Datei auf main](https://github.com/julianzotter/nexus-platform/blob/main/.github/nexus-branch-protection.proposal.json)

Dies ist ein Payload für die klassische Branch-Protection-REST-API, **kein importierbares Ruleset-JSON**. Es existiert noch keine dadurch aktivierte Schutzregel. Für eine neue UI-Regel kann `NEXUS-main-human-gate-v1` als vorgeschlagener Name verwendet werden; das ist kein Name einer bereits angelegten Regel.

API-Befund: `main.protected=false`; Rulesets-API403 mit `Upgrade to GitHub Pro or make this repository public to enable this feature`. GitHub Free unterstützt Schutz für öffentliche Repos; private Repos benötigen einen passenden Tarif (bei persönlichem Repo z.B. GitHub Pro, bei Organisation z.B. GitHub Team). ChatGPT-/Copilot-Abonnements sind keine Freischaltung dieses Repository-Tarifs. Repo nicht als Workaround öffentlich machen. Es wurde kein kostenpflichtiger Plan gekauft.

Nach geeigneter Tarif-/Admin-Konfiguration: [Settings → Branches](https://github.com/julianzotter/nexus-platform/settings/branches), klassische Schutzregel für `main`: PR erforderlich, mindestens1 unabhängige Zustimmung, veraltete Reviews verwerfen, Zustimmung nach letztem Push, Statuscheck `test` erforderlich und Branch aktuell, auch Admins einbeziehen, Force-Push und Branch-Löschung verbieten. Vorher einen tatsächlichen unabhängigen Reviewer berechtigen; eine Person kann ihren eigenen PR nicht selbst approven. Agentenlabels unter demselben GitHub-Account schaffen keine unabhängigen Identitäten.

## Offizielle Quellen

- https://developers.google.com/identity/protocols/oauth2/native-app
- https://developers.google.com/identity/protocols/oauth2#expiration
- https://developers.google.com/workspace/drive/api/guides/api-specific-auth
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches
- https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses
