---
title: "Source summary — About incremental models"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__docs__build__incremental-models-overview.md
source_url: https://docs.getdbt.com/docs/build/incremental-models-overview
---

# About incremental models — summary

**What it covers:** what incremental materialization is, when to use it, and how dbt implements it across databases.

## Key points
- Incremental models are a **materialization** that only transforms/loads **new or changed data** since the last run, instead of reprocessing the whole dataset — reducing build time and resources.
- **When to use:** large datasets (millions/billions of rows) or expensive/complex transforms (Regex, UDFs) where `table` materialization is too costly. Recommended when dbt runs become too slow; they require extra configuration (an advanced usage).
- **How it works across databases:** where supported, a **`merge`** statement inserts new records and updates existing ones. On warehouses without `merge`, dbt implements it with a `delete` (rows to update) followed by an `insert`.
- Transaction management (on supporting platforms) treats actions as one unit of work; on failure dbt rolls back open transactions to restore a good state.

## Exam-relevant tokens
incremental materialization, new/changed data, `merge`, `delete`+`insert`, `table`/`view`, transaction rollback, `unique_key`.

## Gotchas
- Incremental models trade extra configuration complexity for performance — only reach for them when runs are slow / datasets are large.
- On platforms without `merge`, dbt emulates it via delete-then-insert.

Source: [About incremental models](https://docs.getdbt.com/docs/build/incremental-models-overview) · raw: `docs__docs__build__incremental-models-overview.md`
