---
title: "Source summary — Materializations"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__docs__build__materializations.md
source_url: https://docs.getdbt.com/docs/build/materializations
---

# Materializations — summary

**What it covers:** the five built-in materialization strategies, how to configure them, and their pros/cons.

## Key points
- Five built-in materializations: `table`, `view`, `incremental`, `ephemeral`, `materialized_view` (plus custom materializations).
- **Default materialization is `view`.** Set a different one with the `materialized` config.
- Three ways to configure: in `dbt_project.yml` under `models:` with `+materialized:` (folder-level, cascades to subfolders); inline in the model SQL via `{{ config(materialized='table', ...) }}`; or in the model's properties `.yml` under `config: { materialized: ... }`.
- **View** — rebuilt as a view each run via `create view as`. Pro: no extra storage, always latest records. Con: slow to query if heavy transformation or stacked views. Advice: start here, switch only on performance problems.
- **Table** — rebuilt as a table each run via `create table as`. Pro: fast to query. Con: slow to rebuild; new source records aren't added until next run. Advice: use for BI-queried models and slow transformations reused downstream.
- **Incremental** — inserts/updates records since the model last ran. Pro: big reduction in build time (only new records). Con: extra config, advanced usage. Advice: best for event-style data; adopt when `dbt run`s get too slow (don't start here).
- **Ephemeral** — not built into the DB; dbt interpolates the model's code into dependents as a **CTE** (identifier prefixed with `__dbt__cte__`). Pro: reusable logic, keeps warehouse clean. Con: can't `select` from it directly; can't be `ref()`'d by operations/run-operation; harder to debug; no model contracts. Advice: light early-DAG transformations used in one or two downstream models.
- **Materialized view** — `materialized_view`; a view/table hybrid, similar use cases to incremental; uses `on_configuration_change`; `dbt run` acts as a deploy (like a view), with the platform handling data refresh. Not supported on every platform (dbt-snowflake uses Dynamic Tables instead).
- **Python models** support only `table` and `incremental` (not `view`/`ephemeral`); Python isn't allowed for tests/snapshots.

## Exam-relevant tokens
`table`, `view`, `incremental`, `ephemeral`, `materialized_view`, `materialized`, `+materialized`, `{{ config(materialized='table') }}`, `create view as`, `create table as`, `__dbt__cte__`, `on_configuration_change`

## Gotchas
- View is the default — an unspecified model is a view.
- Ephemeral models can't be selected from directly and can't be `ref()`'d in operations; ephemeral doesn't support model contracts.
- Python models can't be `view` or `ephemeral`.

Source: [Materializations](https://docs.getdbt.com/docs/build/materializations) · raw: `docs__docs__build__materializations.md`
