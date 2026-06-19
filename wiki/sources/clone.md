---
title: "Source summary — About dbt clone command"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "04 — Troubleshooting & optimizing pipelines"
source: ../../raw/docs__reference__commands__clone.md
source_url: https://docs.getdbt.com/reference/commands/clone
---

# About dbt clone command — summary

**What it covers:** the `dbt clone` command — cloning selected nodes from a specified state into the target schema(s) using the `clone` materialization.

## Key points
- `dbt clone` clones selected nodes from the **specified state** (via `--state path/to/artifacts`) to the target schema(s); it uses the `clone` materialization.
- On warehouses that support **zero-copy cloning** of tables (Snowflake, Databricks, BigQuery) — and where the model exists as a **table** in the source environment — dbt creates it in the target as a clone.
- Otherwise dbt creates a simple **pointer view** (`select * from` the source object).
- By default `dbt clone` will **not** recreate pre-existing relations in the current target; use the **`--full-refresh`** flag to override and recreate them.
- Clone statements are independent, so you can raise **`--threads`** (e.g. `--threads 50`) to decrease execution time.
- Useful for: blue/green continuous deployment, cloning prod state into dev schemas, handling incremental models in CI jobs, and testing code changes on downstream BI dependencies.
- Compared to deferral: deferral is often the **cheaper, simpler** alternative; but `dbt clone` requires compute and creates **additional objects**, enabling use cases deferral can't (e.g. testing changes in a BI tool _outside of dbt_).
- In the platform CLI, `dbt clone` **automatically includes `--defer`**; in Studio IDE you must set up a Production environment and enable **Defer to production** first.

## Exam-relevant tokens
`dbt clone`, `--state`, `--select`, `--full-refresh`, `--threads`, `clone` materialization, zero-copy cloning, pointer view, `--defer`

## Gotchas
- Zero-copy cloning only applies when the source object is a **table** on a supporting warehouse; tables not meeting this fall back to pointer views.
- `--full-refresh` is required to overwrite pre-existing relations — without it, existing target relations are left as-is.
- Clone creates persisted objects (unlike defer), so it consumes compute and warehouse object inventory.

Source: [About dbt clone command](https://docs.getdbt.com/reference/commands/clone) · raw: `docs__reference__commands__clone.md`
