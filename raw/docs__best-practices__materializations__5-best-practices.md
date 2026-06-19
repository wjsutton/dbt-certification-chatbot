---
title: "Best practices for materializations"
source_url: https://docs.getdbt.com/best-practices/materializations/5-best-practices
retrieved_via: html-extract
fetched: 2026-06-12
---

# Best practices for materializations

Properties of the materializations across the layers of a dbt project:

- **Views** return the freshest, real-time state of their input data when queried, which makes them ideal as **building blocks** for larger models (you don't want inputs at different freshness states). They're also great for **small datasets** with light logic where you want **near real-time** access.
- **Tables** are the **most performant** materialization — they return already-transformed data with no reprocessing. Great for **things end users touch** (e.g. a mart serving a popular dashboard) and for **frequently used, compute-intensive** transformations ("freezing" them in place).
- **Incremental models** serve the **same purposes as tables**, but let you build them on **larger datasets** so they can be built *and* accessed performantly.

## Project-level configuration

Set materializations at the **folder level** in `dbt_project.yml` (under `models:`) and override with individual model configs as needed, to keep code DRY.

- These are the same configs passed to a `{{ config() }}` block, but applied to **every model in that directory and any nested subdirectories**.
- Use a `+` prefix to distinguish a **config** from a folder name (e.g. `+materialized` is a config; `marketing`/`paid_ads`/`google` are folders).
- Configs **cascade**: the **more specific scope wins**.

```yaml
models:
  jaffle_shop:
    marketing:
      +materialized: view
      paid_ads:
        google:
          +materialized: table
```

## Staging → views
Staging models are rarely accessed directly and must stay in sync with source data as building blocks → keep them **views** (the default). Specify it explicitly for clarity:

```yaml
models:
  jaffle_shop:
    staging:
      +materialized: view
```

## Intermediate → ephemeral
Intermediate models sit between staging and marts and aren't accessed directly → good candidates for **ephemeral** materialization, which creates **no warehouse object** and is interpolated as a **CTE** into referencing models.

```yaml
models:
  jaffle_shop:
    staging:
      +materialized: view
    intermediate:
      +materialized: ephemeral
```

Caveat: ephemeral models are harder to troubleshoot (no queryable object); if you need to inspect them, materialize as views in a restricted custom schema instead.

## Marts → table or incremental
Marts are **frequently accessed by end users** and need to be **performant**; they can often run on **intermittently refreshed** (hourly/daily) data → build the **data itself** into the warehouse (a **table**). The only remaining decision: process the whole table at once (`table`) or in chunks (`incremental`).

> **Golden Rule of Materializations** — Start with models as **views**; when they take too long to *query*, make them **tables**; when the tables take too long to *build*, make them **incremental**.
