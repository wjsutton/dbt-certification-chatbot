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

## [2026-06-29] build | updated 4, 55 changed raw
- updated concepts/01-developing-and-optimizing-dbt-models.md
- updated concepts/05-implementing-dbt-tests.md
- updated overview.md
- updated index.md
- (!) stale: sources/best-practice-workflows.md (raw changed) — re-ingest
- (!) stale: sources/clone-incremental-models.md (raw changed) — re-ingest
- (!) stale: sources/writing-custom-generic-tests.md (raw changed) — re-ingest
- (!) stale: sources/test-smarter-not-harder.md (raw changed) — re-ingest
- (!) stale: sources/test-smarter-where-tests-should-go.md (raw changed) — re-ingest
- (!) stale: sources/to-defer-or-to-clone.md (raw changed) — re-ingest
- (!) stale: sources/viewpoint.md (raw changed) — re-ingest
- (!) stale: sources/data-tests.md (raw changed) — re-ingest
- (!) stale: sources/empty-flag.md (raw changed) — re-ingest
- (!) stale: sources/exposures.md (raw changed) — re-ingest
- (!) stale: sources/incremental-microbatch.md (raw changed) — re-ingest
- (!) stale: sources/incremental-models-overview.md (raw changed) — re-ingest
- (!) stale: sources/incremental-strategy.md (raw changed) — re-ingest
- (!) stale: sources/materializations.md (raw changed) — re-ingest
- (!) stale: sources/packages.md (raw changed) — re-ingest
- (!) stale: sources/python-models.md (raw changed) — re-ingest
- (!) stale: sources/sample-flag.md (raw changed) — re-ingest
- (!) stale: sources/snapshots.md (raw changed) — re-ingest
- (!) stale: sources/sources.md (raw changed) — re-ingest
- (!) stale: sources/unit-tests.md (raw changed) — re-ingest
- (!) stale: sources/source-freshness.md (raw changed) — re-ingest
- (!) stale: sources/about-model-governance.md (raw changed) — re-ingest
- (!) stale: sources/model-contracts.md (raw changed) — re-ingest
- (!) stale: sources/model-versions.md (raw changed) — re-ingest
- (!) stale: sources/debug-errors.md (raw changed) — re-ingest
- (!) stale: sources/refactoring-legacy-sql.md (raw changed) — re-ingest
- (!) stale: sources/build.md (raw changed) — re-ingest
- (!) stale: sources/clone.md (raw changed) — re-ingest
- (!) stale: sources/cmd-docs.md (raw changed) — re-ingest
- (!) stale: sources/compile.md (raw changed) — re-ingest
- (!) stale: sources/retry.md (raw changed) — re-ingest
- (!) stale: sources/run.md (raw changed) — re-ingest
- (!) stale: sources/seed.md (raw changed) — re-ingest
- (!) stale: sources/snapshot.md (raw changed) — re-ingest
- (!) stale: sources/source.md (raw changed) — re-ingest
- (!) stale: sources/test.md (raw changed) — re-ingest
- (!) stale: sources/data-test-configs.md (raw changed) — re-ingest
- (!) stale: sources/dbt-commands.md (raw changed) — re-ingest
- (!) stale: sources/dbt_project.yml.md (raw changed) — re-ingest
- (!) stale: sources/exposure-properties.md (raw changed) — re-ingest
- (!) stale: sources/about-global-configs.md (raw changed) — re-ingest
- (!) stale: sources/behavior-changes.md (raw changed) — re-ingest
- (!) stale: sources/defer.md (raw changed) — re-ingest
- (!) stale: sources/methods.md (raw changed) — re-ingest
- (!) stale: sources/state-selection.md (raw changed) — re-ingest
- (!) stale: sources/syntax.md (raw changed) — re-ingest
- (!) stale: sources/contract.md (raw changed) — re-ingest
- (!) stale: sources/grants.md (raw changed) — re-ingest
- (!) stale: sources/constraints.md (raw changed) — re-ingest
- (!) stale: sources/freshness.md (raw changed) — re-ingest
- (!) stale: sources/versions.md (raw changed) — re-ingest
- (!) stale: sources/source-configs.md (raw changed) — re-ingest
- (!) stale: sources/data-product-management.md (raw changed) — re-ingest
