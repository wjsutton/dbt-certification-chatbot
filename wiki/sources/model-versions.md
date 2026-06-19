---
title: "Source summary — Model versions"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "02 — Managing dbt models governance"
source: ../../raw/docs__docs__mesh__govern__model-versions.md
source_url: https://docs.getdbt.com/docs/mesh/govern/model-versions
---

# Model versions — summary

**What it covers:** versioning a final dbt model like an API — supporting breaking changes with a migration window and deprecation.

## Key points

- A final shared model behaves like an **API**: producers need to change it; consumers need stability. **Model versions** give a migration path for breaking changes.
- dbt Core **1.6** introduced first-class **deprecating models** via [`deprecation_date`](versions.md). Versions + deprecation let producers *sunset* old models and consumers *migrate*.
- **When to version:** make a new version for a **breaking change** (removing/renaming a column, changing data type or nullability). For **non-breaking** changes (adding a column, fixing a bug) you do **not** need a new version. Prefer non-breaking changes; bump "latest" on a predictable cadence.
- All versions **preserve the model's original name** and are `ref`'d by that name. By default `ref('dim_customers')` resolves to the **latest** version; pin a version with `ref('dim_customers', v=2)`.
- Naming convention: file `<model_name>_v<v>` (e.g. `dim_customers_v2.sql`); the **latest** may live in `<model_name>.sql` (no suffix). DB relation alias defaults to `<model_name>_v<v>`.
- Declare versions under `versions:` with `latest_version:` controlling which is canonical. If `latest_version` is unset, the **numerically/alphabetically highest** version is latest.
- Versions can be `latest`, `prerelease` (above latest), or `old`. `version`-based selection + YAML selectors can exclude old versions in dev.

## Run / select

- `dbt run --select dim_customers` runs **all** versions.
- `dbt run --select dim_customers.v2` (or `dim_customers_v2`) runs a specific version.
- `dbt run -s dim_customers,version:latest` runs only the latest.

## Exam-relevant tokens

`versions`, `latest_version`, `deprecation_date`, `v`, `ref('model', v=2)`, `version:latest`, `version:old`, `<model_name>_v<v>`, `latest_version_pointer` (1.12+)

## Gotchas

- Differs from version control: multiple model versions live **simultaneously** in the same repo/environment (like web APIs), whereas only one project state deploys at a time.
- `ref` resolves to latest only if no `v` pin; a prerelease version above `latest_version` does **not** auto-resolve.
- `latest_version_pointer` config (auto view to latest) is **1.12+**; in 1.11 use a custom macro/post-hook or `alias`.

Source: [Model versions](https://docs.getdbt.com/docs/mesh/govern/model-versions) · raw: `docs__docs__mesh__govern__model-versions.md`
