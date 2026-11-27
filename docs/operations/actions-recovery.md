# Actions recovery

| Workflow | Check first | Recovery and verification |
| --- | --- | --- |
| CI | The failed job and exact commit | Fix the failed check on a branch. Verify the new commit in the pull request. |
| NEXUS Monitor | Repository checks, then operational evidence gate | Inspect the monitor report and CI for the same commit. After correction, run the existing Monitor workflow and verify its report, source commit and conclusion. |
| NEXUS Drive to GitHub | Poll status and checkpoint gate | For `OAUTH_HTTP_400_INVALID_GRANT`, the credential owner renews authorization using the existing OAuth procedure. Run the existing poll workflow and verify live-poll evidence and its checkpoint. An initialization receipt only proves initialization. |
| NEXUS GitHub to WORK | Credential preflight, source run and delivery receipt | Check write authorization after OAuth renewal. Before replay, review the source run and any existing delivery journal. Use the existing dispatch inputs for the source run and, if applicable, the earlier delivery journal. Verify raw-byte readback and the registration result in the receipt. |

Use the existing workflow schedules and the existing WORK writer. Keep delivery evidence separate from a role's receipt and ACK. Put private source material, recipient routing and operational handoffs in the authorized private channel. For public job summaries, use failure classifications and links to public runbooks.
