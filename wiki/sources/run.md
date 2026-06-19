---
title: "Source summary — About dbt run command"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__reference__commands__run.md
source_url: https://docs.getdbt.com/reference/commands/run
---

# About dbt run command — summary

**What it covers:** `dbt run`, which materializes models only, plus `--full-refresh` and `--empty` behavior.

## Key points
- `dbt run` applies **only to models** — it does NOT run tests, snapshots, or seeds. Use `dbt test`, `dbt snapshot`, `dbt seed`, or `dbt build` for those.
- Executes compiled SQL against the current `target` database, in dependency-graph order, with multi-threading.
- For zero-downtime swaps, dbt builds each model under a temporary name then drops/renames within a single transaction (for adapters that support transactions).
- **`--full-refresh`** (short: **`-f`**) treats incremental models as table models — useful when the incremental schema changes or logic changes and you must reprocess everything. Exposed as `flags.FULL_REFRESH`; with it set, `is_incremental()` returns `false` for **all** models.
- **`--empty`** does a schema-only dry run: limits refs/sources to zero rows, still executes SQL against the warehouse, validating dependencies without expensive input reads.
- Run status codes (list_runs API): Queued=1, Starting=2, Running=3, Success=10, Error=20, Canceled=30, Skipped=40.

## Exam-relevant tokens
`dbt run`, `--full-refresh`, `-f`, `flags.FULL_REFRESH`, `is_incremental()`, `--empty`, `target`, `{{ this }}`.

## Gotchas
- `dbt run` never runs tests/snapshots/seeds — a common distractor.
- `--full-refresh` makes `is_incremental()` return `false`, so the model rebuilds from scratch as a table.

Source: [About dbt run command](https://docs.getdbt.com/reference/commands/run) · raw: `docs__reference__commands__run.md`
