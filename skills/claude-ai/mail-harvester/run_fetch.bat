@echo off
REM Sync all mailboxes on Windows. Double-click or schedule via Task Scheduler.
REM Task Scheduler: Action = Start a program -> this .bat ; "Start in" = this folder.
cd /d "%~dp0"
if exist secrets.cmd call secrets.cmd
python fetch_imap.py --config accounts.toml --db mail.db --archive eml %*
