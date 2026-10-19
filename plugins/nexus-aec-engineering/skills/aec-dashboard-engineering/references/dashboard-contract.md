# Dashboard envelope v0.1.0
Normalize adapter output to schema_version, mode, run_id, source,
model_fingerprint, calculation_id, combination_id, converged, units, values,
result_sha256 and observed_at. Use LIVE only for real adapter data, DEMO for
fixtures. source=RFEM requires an authenticated runtime receipt retained in audit.
Units: force=N, length=m, moment=N*m. Values must be nonempty named finite
numbers with quantity units/sign convention recorded in the manifest.
result_sha256 is SHA-256 of UTF-8 JSON of values with sorted keys, separators
(',', ':'), ensure_ascii=False and allow_nan=False. Also preserve the raw
adapter-response hash separately. Include solver version, input SHA-256,
normative edition/annex and source pointers in the associated run manifest.
UI states UNKNOWN/CONNECTING/AUTHENTICATED/READY/RUNNING/FAILED/STALE/
REVIEW_CANDIDATE are separate from DEMO/LIVE mode and human acceptance.
Any geometry, material, load, support, combination or solver-setting change
invalidates results. Only a real current adapter receipt may restore them.
Acceptance: current inputs reproduce results; change invalidates them; adapter
failure remains visible; demo results cannot pass live validation; mobile and
keyboard interactions work; exports preserve topology, IDs, units and provenance.
