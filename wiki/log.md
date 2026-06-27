---
title: "Log"
tags: [log]
---


# Log

Append-only timeline. Prefix entries `## [YYYY-MM-DD] <op> | <subject>` so they stay greppable (`grep '^## \[' log.md`).

## [2026-06-11] scaffold | Initialized wiki

- Built structure from the certification mapping: 7 concept pages, 56 raw sources catalogued.
- Next: run Ingest on each raw source to populate summaries.

## [2026-06-11] ingest | Domain 07 (state-selection, defer, retry) + sample-flag
- Wrote raw/ files + _manifest.tsv for 4 pages (state-selection, defer, retry, sample-flag).
- Added source summaries: sources/state-selection.md, sources/defer.md, sources/retry.md, sources/sample-flag.md.
- Concept 07 "Leveraging the dbt state": full synthesis (status draft); methods page still pending.
- Concept 01: synthesised the --sample / --empty sub-topic; remainder still stub.

## [2026-06-12] build | updated 9, 4 new raw
- updated concepts/01-developing-and-optimizing-dbt-models.md
- updated concepts/02-managing-dbt-models-governance.md (upgraded)
- updated concepts/03-debugging-data-modeling-errors.md (upgraded)
- updated concepts/04-troubleshooting-and-optimizing-pipelines.md (upgraded)
- updated concepts/05-implementing-dbt-tests.md (upgraded)
- updated concepts/06-external-dependencies.md (upgraded)
- updated concepts/07-leveraging-the-dbt-state.md
- updated overview.md
- updated index.md

## [2026-06-12] build | 1 changed raw
- (!) stale: sources/retry.md (raw changed) — re-ingest

## [2026-06-12] build | 1 changed raw
- (!) stale: sources/retry.md (raw changed) — re-ingest

## [2026-06-12] build | updated 2, 1 new raw
- updated concepts/07-leveraging-the-dbt-state.md
- updated index.md

## [2026-06-12] build | updated 7, 50 new raw, 5 changed raw
- updated concepts/01-developing-and-optimizing-dbt-models.md
- updated concepts/02-managing-dbt-models-governance.md
- updated concepts/03-debugging-data-modeling-errors.md
- updated concepts/04-troubleshooting-and-optimizing-pipelines.md
- updated concepts/05-implementing-dbt-tests.md
- updated concepts/06-external-dependencies.md
- updated index.md
- (!) stale: sources/sample-flag.md (raw changed) — re-ingest
- (!) stale: sources/retry.md (raw changed) — re-ingest
- (!) stale: sources/defer.md (raw changed) — re-ingest
- (!) stale: sources/methods.md (raw changed) — re-ingest
- (!) stale: sources/state-selection.md (raw changed) — re-ingest

## [2026-06-12] build | updated 5, 2 new raw, 4 changed raw
- updated concepts/01-developing-and-optimizing-dbt-models.md
- updated concepts/02-managing-dbt-models-governance.md
- updated concepts/05-implementing-dbt-tests.md
- updated concepts/06-external-dependencies.md
- updated index.md

## [2026-06-12] build | updated 4
- updated concepts/01-developing-and-optimizing-dbt-models.md
- updated concepts/02-managing-dbt-models-governance.md
- updated concepts/06-external-dependencies.md
- updated index.md

## [2026-06-12] build | updated 1
- updated index.md

## [2026-06-12] build | updated 6
- updated concepts/01-developing-and-optimizing-dbt-models.md
- updated concepts/02-managing-dbt-models-governance.md
- updated concepts/03-debugging-data-modeling-errors.md
- updated concepts/04-troubleshooting-and-optimizing-pipelines.md
- updated concepts/05-implementing-dbt-tests.md
- updated concepts/06-external-dependencies.md

## [2026-06-12] ingest | Domains 01-06 fully ingested + questions
- Added ~50 source summaries (sources/), filled all concept syntheses (status: done).
- Question bank grown to 66 items across all 7 domains and 5 formats.

## [2026-06-27] note | What's new in 1.11
- Created wiki/notes/whats-new-in-1.11.md: version-tagged feature diff (v1.9–v1.11)
  distinguishing in-scope 1.11 content from out-of-scope v1.12 items.
- Linked from index.md (new Notes section).

## [2026-06-27] note | Interview prompt — microbatch
- Created wiki/notes/interview-prompt-microbatch.md: self-contained copy-paste
  prompt that turns a fresh Claude chat into an adaptive interviewer on the
  microbatch incremental strategy. Grounded in incremental-microbatch/-strategy/
  -models-overview. Linked from index.md.

## [2026-06-27] note | Interview prompt — unit tests
- Created wiki/notes/interview-prompt-unit-tests.md: self-contained copy-paste
  interviewer prompt for unit tests, emphasising the unit-vs-data-test contrast.
  Grounded in unit-tests/data-tests. Linked from index.md.
