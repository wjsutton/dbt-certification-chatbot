---
title: "Source summary — Clone incremental models as the first step of your CI job"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "04 — Troubleshooting & optimizing pipelines"
source: ../../raw/docs__best-practices__clone-incremental-models.md
source_url: https://docs.getdbt.com/best-practices/clone-incremental-models
---

# Clone incremental models as the first step of your CI job — summary

**What it covers:** a best practice that zero-copy clones pre-existing incremental models into the PR schema as the first CI step so they build in **incremental** (not full-refresh) mode.

## Key points
- Conditions: `dbt clone` requires dbt **1.6+**; the strategy only works on warehouses that support **zero copy cloning** (otherwise clone just creates pointer views).
- In a **Slim CI** job that defers to prod and runs `dbt build --select state:modified+`, modified models build into a temporary, PR-specific schema.
- Problem: an incremental model that doesn't yet exist in the PR schema has **`is_incremental`** = false, so it builds in `full-refresh` mode — slow, costly, and it can mask failures that an incremental build in prod would hit (e.g. schema drift with `on_schema_change: fail`).
- Fix — two CI commands, clone first:
  1. `dbt clone --select state:modified+,config.materialized:incremental,state:old`
  2. `dbt build --select state:modified+`
- After the clone step the incremental models already exist in the PR schema, so `is_incremental` is **true** and the `dbt build` runs them in incremental mode — faster CI that more accurately mimics post-merge behavior.
- `state:old` restricts the clone to models that already exist in the prior state, i.e. it **excludes brand-new** incremental models (which should full-refresh in CI just as they will in prod).
- `config.materialized:incremental` restricts the clone selection to incremental models.

## Exam-relevant tokens
`dbt clone`, `state:modified+`, `config.materialized:incremental`, `state:old`, `is_incremental`, `on_schema_change: fail`, `--full-refresh`, Slim CI, zero copy cloning, dbt 1.6+

## Gotchas
- Without `state:old` you don't get an error, just a benign "No relation found in state manifest for…" message for brand-new models; adding `state:old` is more **explicit** and avoids trying to clone them.
- A new column on an `on_schema_change: fail` incremental model: an **incremental** build fails but a **full-refresh** succeeds — choose whether CI should surface that failure or pass.
- The clone strategy only helps where zero-copy cloning exists; elsewhere pointer views are created.

Source: [Clone incremental models as the first step of your CI job](https://docs.getdbt.com/best-practices/clone-incremental-models) · raw: `docs__best-practices__clone-incremental-models.md`
