---
title: "Source summary — Best practices for materializations"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__best-practices__materializations__5-best-practices.md
source_url: https://docs.getdbt.com/best-practices/materializations/5-best-practices
---

# Best practices for materializations — summary

**What it covers:** which materialization to use per project layer and how to set them DRY at folder level with the Golden Rule.

## Key points
- **Views** return the freshest, real-time state of input data when queried → ideal as **building blocks** for larger models (you don't want inputs at mixed freshness), and for small datasets needing near real-time access.
- **Tables** are the **most performant** (already-transformed, no reprocessing) → good for things end users touch (a mart serving a dashboard) and for frequently used, compute-intensive transformations ("freezing" them).
- **Incremental models** serve the **same purposes as tables** but for **larger datasets** so they can be built *and* accessed performantly.
- **Project-level config:** set materializations at the **folder level** in `dbt_project.yml` under `models:`, override per-model as needed → keeps code DRY.
- Folder-level configs are the same ones passed to `{{ config() }}`, applied to **every model in that directory and any nested subdirectories**.
- Use the **`+` prefix** to distinguish a **config** from a folder name (`+materialized` is a config; `marketing`/`paid_ads`/`google` are folders).
- Configs **cascade** — the **more specific scope wins** (a deeper subfolder's `+materialized` overrides a parent's).
- **Staging → views** (default; the building blocks that stay in sync with sources).
- **Intermediate → ephemeral** (no warehouse object; interpolated as a CTE into referencing models). Caveat: harder to troubleshoot — materialize as views in a restricted custom schema if you need to inspect them.
- **Marts → table or incremental** (frequently accessed by end users, need performance; choose `table` for whole-table or `incremental` for chunked).
- **Golden Rule of Materializations:** start as **views**; when too slow to *query*, make them **tables**; when tables are too slow to *build*, make them **incremental**.

## Exam-relevant tokens
`+materialized`, `models:`, `view`, `table`, `incremental`, `ephemeral`, `+` prefix, cascade / most-specific-wins, staging, intermediate, marts, Golden Rule

## Gotchas
- The `+` prefix is what distinguishes a config key from a folder name in `dbt_project.yml`.
- Cascading means a nested subfolder config overrides a parent folder config.
- Ephemeral intermediate models have no queryable object — inspect by temporarily making them views.

Source: [Best practices for materializations](https://docs.getdbt.com/best-practices/materializations/5-best-practices) · raw: `docs__best-practices__materializations__5-best-practices.md`
