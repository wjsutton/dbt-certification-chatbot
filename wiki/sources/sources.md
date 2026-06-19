---
title: "Source summary — Add sources to your DAG"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__docs__build__sources.md
source_url: https://docs.getdbt.com/docs/build/sources
---

# Add sources to your DAG — summary

**What it covers:** declaring raw warehouse tables as dbt sources, selecting from them with `{{ source() }}`, and configuring source freshness.

## Key points
- Sources name/describe data loaded by EL tools so you can select from them, test assumptions, and calculate freshness.
- Defined in `.yml` files under a `sources:` key with `name`, `database`, `schema`, and `tables:`. By default `schema` equals the source `name`; set `schema` only if they differ.
- Select with `{{ source('jaffle_shop', 'orders') }}` — dbt compiles it to the full table name (e.g. `raw.jaffle_shop.orders`) and this creates a dependency between the model and the source table (the raw object dependency in the DAG).
- You can add data tests (e.g. `unique`, `not_null`) and descriptions to sources, just like models.
- **Source freshness:** add a `freshness` block plus `loaded_at_field` to the source/table. One or both of `warn_after` and `error_after` (each `{count, period}`); if neither is given, dbt does not calculate freshness. `loaded_at_field` is required to calculate freshness (unless warehouse metadata can be leveraged).
- Freshness configs apply hierarchically — values set at the `source` level flow down to all its `tables`; a table can override or set `freshness: null` to skip.
- In v1.9 `freshness` moved under `config:`; in v1.10 `loaded_at_field` moved under `config:`.
- Check freshness with `dbt source freshness`; dbt builds a `select max(loaded_at_field) ... as max_loaded_at, current_timestamp as calculated_at` query.
- Build downstream of fresher sources: `dbt build --select source_status:fresher+`.
- A `filter` argument can be added to the freshness config to avoid full table scans (e.g. `filter: _etl_loaded_at >= date_sub(current_date(), interval 1 day)`).

## Exam-relevant tokens
`sources:`, `{{ source() }}`, `source('name','table')`, `database`, `schema`, `tables:`, `freshness`, `loaded_at_field`, `warn_after`, `error_after`, `count`, `period`, `dbt source freshness`, `source_status:fresher+`, `filter`

## Gotchas
- Using `{{ source() }}` (not a hard-coded `db.schema.table`) is what registers the dependency/lineage.
- No `loaded_at_field` (or warehouse-metadata alternative) ⇒ no freshness calculated for that table.
- `freshness: null` on a table opts it out of freshness checks even when the source defines defaults.

Source: [Add sources to your DAG](https://docs.getdbt.com/docs/build/sources) · raw: `docs__docs__build__sources.md`
