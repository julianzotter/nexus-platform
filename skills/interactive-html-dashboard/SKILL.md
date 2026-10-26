---
name: interactive-html-dashboard
description: Build a self-contained, browser-openable HTML dashboard with KPI cards, animated charts, filters, a sortable table, file import/export and an optional rule-based text/voice data dialog. Use for executive overviews, team monitoring snapshots, or turning query results into a shareable report in one file.
---

# Interactive HTML dashboard
Version: 0.1.0. Owner: Julian Zotter. Reference implementation: `prototypes/data-dashboard/`. A dashboard is a review artifact, not a release or an approval.

## Data preparation
Produce data with a deterministic script from an identified source (git revision, file hash, query text and time). Embed it as `window.DASHBOARD_DATA` between `/*DATA:BEGIN*/` and `/*DATA:END*/`; escape `</` in the payload. Declare every column with key, label, type (`number`, `category`, `date`, `text`) and search aliases. Unknown or unmeasured values stay `null`, never zero. Show the source and revision in the header and every export.

## Layout (semantic HTML5)
`header` with dataset switch and file I/O → one filter row (date presets first) → KPI cards → `figure`/`figcaption` charts → `table` with `caption` and `th scope` → `aside` dialog. Grid collapses to one column on narrow screens; no horizontal page scroll.

## Charts and animation
Follow the dataviz skill: fixed categorical slot order, colour follows the entity and never the filtered rank, at most five categories plus "Other", no dual axes, single-series charts in one colour. Animate value changes with a `requestAnimationFrame` tween (about 650 ms, ease-out) and disable motion under `prefers-reduced-motion`. Every mark has a hover/focus tooltip; labels from data go through `textContent`, never `innerHTML`. Clicking a mark sets a filter; filters scope every KPI, chart and table.

## Interaction and file I/O
Import CSV/TSV/JSON/JSONL by button and drag & drop with type inference and a size limit. Export filtered CSV (with BOM), JSON with filters and source, a Markdown report, and per-chart SVG. Live file watching uses the File System Access API with feature detection; label it as live only while polling actually runs.

## Data dialog
Use a deterministic grammar that maps questions to filters, grouping, sorting, top-N, aggregates, dataset switch and export, and report unparsed input as not understood. A second voice ("Prüfer") states the data basis and active filters. Speech recognition via Web Speech API sends audio to the browser vendor in Chrome/Edge: show this before first use. Do not claim LLM understanding, live external data or real-time feeds the page does not have. A model-backed dialog needs a server-side key and is a separate component.

## Verification
Test the data builder (rebuild at the embedded revision equals the embedded payload), row/column conformance, absence of external script sources, and the query grammar via Node. Render in a real browser, inspect screenshots and drive at least one query, one filter and one import end-to-end. Report what was and was not executed.
