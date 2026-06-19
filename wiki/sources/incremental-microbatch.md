---
title: "Source summary — About microbatch incremental models"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__docs__build__incremental-microbatch.md
source_url: https://docs.getdbt.com/docs/build/incremental-microbatch
---

# About microbatch incremental models — summary

**What it covers:** the `microbatch` incremental strategy for large time-series data — its configs (event_time, batch_size, begin, lookback) and batch behavior.

## Key points
- Available for dbt **Latest** and dbt Core **v1.9+**. Designed for **large time-series datasets**; processes the model in multiple time-bounded **batches** instead of one query.
- Relies solely on an **`event_time`** column to define time ranges for filtering. Set `event_time` on the microbatch model **and on any direct parents** you want filtered (this differs from `partition_by`). Each batch is **independent and idempotent**, enabling backfills, parallel batch execution, and per-batch retry.
- **Configs:**
  - **`event_time`** (Required) — the column indicating when the row occurred. Required on the model and on direct parents to be filtered.
  - **`begin`** (Required) — the "beginning of time" / start point for initial or full-refresh builds.
  - **`batch_size`** (Required) — granularity of batches: `hour`, `day`, `month`, or `year`.
  - **`lookback`** (Optional, default `1`) — process X batches prior to the latest bookmark to capture late-arriving records.
  - **`concurrent_batches`** (Optional, default `None`) — `true` runs batches in parallel, `false` sequentially; otherwise auto-detected.
- Configure with `incremental_strategy='microbatch'` alongside `materialized='incremental'`. dbt auto-filters upstream `ref`/`source` that define `event_time` based on `lookback` and `batch_size`.
- `dbt run --full-refresh` on a microbatch model only reloads data if a `begin` config is set. To process from the dataset start you must set `begin` (or use the `--event-time-start` flag).
- Adapter-specific full-batch replacement: postgres→`merge`; redshift/snowflake→`delete+insert`; bigquery/spark→`insert_overwrite`; databricks→`replace_where`.

## Exam-relevant tokens
`incremental_strategy='microbatch'`, `event_time`, `begin`, `batch_size` (`hour`/`day`/`month`/`year`), `lookback`, `concurrent_batches`, `--event-time-start`, `materialized='incremental'`.

## Gotchas
- `event_time`, `begin`, and `batch_size` are all **required**; `lookback`/`concurrent_batches` are optional.
- Set `event_time` on upstream parents too, or they won't be filtered per batch (e.g. dimension tables get a full scan).
- `--full-refresh` won't reset/reload a microbatch model unless `begin` is configured.

Source: [About microbatch incremental models](https://docs.getdbt.com/docs/build/incremental-microbatch) · raw: `docs__docs__build__incremental-microbatch.md`
