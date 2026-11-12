#!/usr/bin/env bash
# Sync all mailboxes. Usage: ./run_fetch.sh  [extra fetch_imap.py args]
# Cron example (every 30 min):  */30 * * * * /path/to/mail-harvester/run_fetch.sh >> /path/to/mail-harvester/sync.log 2>&1
set -euo pipefail
cd "$(dirname "$0")"
if [ -f secrets.env ]; then
  set -a; source secrets.env; set +a
fi
python3 fetch_imap.py --config accounts.toml --db mail.db --archive eml "$@"
