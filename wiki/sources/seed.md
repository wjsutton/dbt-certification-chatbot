---
title: "Source summary — About dbt seed command"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__reference__commands__seed.md
source_url: https://docs.getdbt.com/reference/commands/seed
---

# About dbt seed command — summary

**What it covers:** `dbt seed`, which loads static CSV files from `seed-paths` into the warehouse as tables.

## Key points
- `dbt seed` loads static CSV files from your project's `seed-paths` into the warehouse as tables. Use for small, version-controlled reference data (country codes, mappings, categories).
- Seeds are configured in `dbt_project.yml` (directories, column interpretation). Reference loaded seeds in downstream models; rerun `dbt seed` when CSVs change.
- Select specific seeds: `dbt seed --select "country_codes"`; multiple: `dbt seed --select "country_codes state_codes"`.
- **`--full-refresh`** forces a clean, full reload of seed data (rather than incremental update) — use when you changed the seed structure (column names/types) or need consistent behavior across environments. E.g. `dbt seed --full-refresh`.
- **`--empty`** (from dbt Core v1.12) creates seed tables with the correct inferred schema but **zero rows** — a schema-only dry run so downstream models/unit tests can compile/run without loading data. E.g. `dbt seed --empty`. (Not present in 1.11.)

## Exam-relevant tokens
`dbt seed`, `seed-paths`, `--select`, `--full-refresh`, `--empty` (v1.12+), `dbt_project.yml`, `run_results.json`.

## Gotchas
- `--full-refresh` rebuilds seed tables from scratch — needed after seed column name/type changes.
- The `--empty` flag for `seed` is a v1.12 addition; on dbt Core 1.11 use `--empty` on `run`/`build`/`snapshot`/`compile`.

Source: [About dbt seed command](https://docs.getdbt.com/reference/commands/seed) · raw: `docs__reference__commands__seed.md`
