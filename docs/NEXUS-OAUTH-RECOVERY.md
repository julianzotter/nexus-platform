# NEXUS Drive OAuth recovery
Run locally from the updated repository on the Windows PC:
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\windows\repair_drive_oauth.ps1
```
The wrapper installs the setup-only dependencies, checks GitHub CLI login, and opens Google consent. With an existing private `.nexus-credentials/drive-oauth.json`, it reuses the Desktop client's ID/secret without needing the original client download. Otherwise a local file picker requests the original Google **Desktop OAuth client JSON**. Do not upload that JSON or credential values to WORK or chat. `py` and `gh` must be installed.
Equivalent direct renewal, with setup dependencies already installed:
```powershell
py tools/configure_drive_oauth.py --renew --publish
```
The fresh candidate must refresh successfully and access the exact WORK folder with `canAddChildren=true` before the old local credentials are replaced. A prior byte-identical private snapshot is preserved; local renewal uses an exclusive local lock and atomic replacement. This lock covers that credential file, not distributed registry writers. Windows ACL restriction precedes writing new credential bytes. GitHub secrets are supplied over stdin, never command arguments. A failed publication can leave a valid new local credential and partially updated repository secrets; rerun `--publish-existing` only after checking the local credential with `--check --require-write`.
Check/renewal metadata is not a Drive write/readback or sync receipt. After renewal, run the existing delivery workflow against a completed trusted monitor run and verify its resulting WORK bytes. No live renewal was performed in the cloud workspace: no client/refresh credentials were present.
The sanitized runtime distinguishes allowlisted OAuth error types, while discarding free service descriptions. `HTTP_400` alone does not prove expiration. `invalid_grant` can have several causes; Google consent may need renewal. For external OAuth apps in **Testing**, Google documents a seven-day refresh-token lifetime for non-profile scopes; project publishing status must be inspected separately, never inferred from one error.
Sources: [Google OAuth access and expiration](https://developers.google.com/identity/protocols/oauth2/), [Desktop OAuth and errors](https://developers.google.com/identity/protocols/oauth2/native-app).
