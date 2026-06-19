---
title: "Source summary — About incremental strategy"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__docs__build__incremental-strategy.md
source_url: https://docs.getdbt.com/docs/build/incremental-strategy
---

# About incremental strategy — summary

**What it covers:** choosing and configuring an `incremental_strategy` (append, merge, delete+insert, insert_overwrite, microbatch) and their behaviors.

## Key points
- Strategy choice depends on data volume, reliability of your `unique_key`, and adapter feature support. Set via `incremental_strategy` in `dbt_project.yml` (`+incremental_strategy:`) or in the model `config(...)`.
- **Built-in strategies and behavior:**
  - **`append`** — simply inserts selected records; **doesn't check for duplicates** (same source record inserted again ⇒ duplicate rows). Low cost.
  - **`merge`** — inserts new keys and **updates** existing keys (mirrors SCD1). Needs a `unique_key`; **without `unique_key`, `merge` behaves like `append`**. Can resolve duplicates. Scans the whole destination, so best for smaller/incremental tables.
  - **`delete+insert`** — deletes rows for the `unique_key` then inserts; fully replaces matched records. Useful when `unique_key` isn't truly unique or `merge` is unsupported. (Use snapshots for SCD2, not delete+insert.)
  - **`insert_overwrite`** — replaces entire **partitions** wholesale (not row-level); ideal for date-partitioned tables.
  - **`microbatch`** — splits large time-series data into time-based batches via `event_time`.
- Strategy-specific configs (merge): `merge_update_columns` (update only these columns) or `merge_exclude_columns` (exclude these). Built-in strategies map to macros e.g. `get_incremental_merge_sql`, `get_incremental_append_sql`, `get_incremental_microbatch_sql`. Custom strategies = macro `get_incremental_STRATEGY_sql` + `incremental_strategy: STRATEGY`.
- Adapter support varies, e.g. BigQuery supports `merge` + `insert_overwrite` (not `append`/`delete+insert`); Snowflake supports `append`/`merge`/`delete+insert`/`insert_overwrite`/`microbatch`.

## Exam-relevant tokens
`incremental_strategy`, `append`, `merge`, `delete+insert`, `insert_overwrite`, `microbatch`, `unique_key`, `merge_update_columns`, `merge_exclude_columns`, `get_incremental_merge_sql`.

## Gotchas
- `merge` without a `unique_key` behaves like `append`.
- `append` does NOT dedupe — duplicate source rows are inserted again.
- For SCD2 history use snapshots, not `delete+insert`; `insert_overwrite` replaces whole partitions, not individual rows.

Source: [About incremental strategy](https://docs.getdbt.com/docs/build/incremental-strategy) · raw: `docs__docs__build__incremental-strategy.md`
