# Provider settings (verified)

## World4You (office@zotterconsult.at, zt-office@zotter-litschauer.at, j.zotter@spline-zt.at)

All three custom domains are hosted at World4You. DNS confirms each
`imap.<domain>` is a CNAME to `imap.world4you.com` (81.19.149.211).

| Setting   | Value                    |
|-----------|--------------------------|
| IMAP host | `imap.world4you.com`     |
| IMAP port | `993` (SSL/TLS)          |
| Username  | full e-mail address      |
| Password  | mailbox password (set in the World4You customer area / webmail) |
| SMTP      | `smtp.world4you.com:587` (STARTTLS) — only needed if you also *send* |

Source: World4You FAQ (faq.world4you.com, articles 4616 / 4618 / 4620, retrieved 2026).

Notes:
- The correct second domain has a hyphen: `zotter-litschauer.at`. The
  non-hyphen form `zotterlitschauer.at` has no MX record and is not a mailbox.
- IMAP must be enabled on the package (it is on all but "Domain Server Basic").
- If login fails, verify the password by signing in at webmail.world4you.com;
  you can reset the mailbox password there at any time.

## Gmail (julian.zotter@gmail.com)

| Setting   | Value                |
|-----------|----------------------|
| IMAP host | `imap.gmail.com`     |
| IMAP port | `993` (SSL/TLS)      |
| Username  | full Gmail address   |
| Password  | **App Password** (16 chars) |

App Password setup:
1. Enable 2-Step Verification: myaccount.google.com -> Security.
2. Security -> "App passwords" -> create one (e.g. name it "mail-harvester").
3. Use the 16-character value (spaces optional) as `MAIL_PASS_GMAIL`.
4. In Gmail settings, ensure IMAP is enabled (Settings -> Forwarding and POP/IMAP).

A normal Google account password will be rejected for IMAP; an App Password is
required because Google disabled "less secure app" basic auth. (For a fully
OAuth2 flow instead of App Passwords, the Gmail API is the alternative — heavier
to set up and not needed for a personal archive.)
