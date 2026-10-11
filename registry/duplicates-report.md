# Duplicate candidates

Groups are ordered by SHA-256; canonical records are ordered by root, path, and id.
Candidates cover only indexed records; an empty result does not establish that unavailable sources contain no duplicates.

No duplicate candidates were found in the available registry records.

## Reproducibility

Tool: detect_duplicates.py v1; Python 3.12.3

Command: `/usr/bin/python3 tools/detect_duplicates.py --registry registry/file-registry.jsonl --report registry/duplicates-report.md`
