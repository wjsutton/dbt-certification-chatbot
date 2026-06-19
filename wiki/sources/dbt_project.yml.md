---
title: "Source summary — dbt_project.yml reference"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__reference__dbt_project.yml.md
source_url: https://docs.getdbt.com/reference/dbt_project.yml
---

# dbt_project.yml reference — summary

**What it covers:** the project configuration file — what it is, the available top-level keys, the `+` prefix, and YAML naming conventions.

## Key points
- Every dbt project needs a `dbt_project.yml` — it is how dbt knows a directory is a dbt project and tells dbt how to operate it.
- By default dbt looks for it in the current working directory and parents; override with `--project-dir` or, in **1.11**, the `DBT_ENGINE_PROJECT_DIR` env var (was `DBT_PROJECT_DIR` ≤1.10).
- Core top-level keys: `name`, `config-version: 2`, `version`, `profile`, the `*-paths` keys (`model-paths`, `seed-paths`, `test-paths`, `analysis-paths`, `macro-paths`, `snapshot-paths`, `docs-paths`, etc.), `clean-targets`, `require-dbt-version`, `flags`, `vars`, `on-run-start`, `on-run-end`, `dispatch`, `restrict-access`, `quoting`.
- Resource-config keys (folder-scoped configs go here): `models:`, `seeds:`, `snapshots:`, `sources:`, `data_tests:`, `exposures:`, `metrics:`, `semantic-models:`, `saved-queries:`, `analyses:`, `functions:`.
- **The `+` prefix** marks a **config** (vs. a resource/folder name) when set in `dbt_project.yml`, e.g. `+materialized`, `+enabled`. Configs set under a folder path **cascade** to all models in that directory and nested subdirectories, most-specific scope winning.
- **Naming convention:** use **dashes** (`-`) for multi-word resource types **inside `dbt_project.yml`** (e.g. `saved-queries:`), but **underscores** (`_`) for the same resource types in **other YAML files** (e.g. `saved_queries:` in a semantic-models YAML).

## Exam-relevant tokens
`dbt_project.yml`, `name`, `config-version: 2`, `profile`, `model-paths`, `models:`, `seeds:`, `snapshots:`, `sources:`, `vars:`, `on-run-start`, `on-run-end`, `+` prefix, `+materialized`, `--project-dir`, `DBT_ENGINE_PROJECT_DIR`, dashes vs underscores

## Gotchas
- You can only set a **config** in `dbt_project.yml`, not a "property" (e.g. macro properties can't go here).
- Inside `dbt_project.yml` use dashes for multi-word resource keys; everywhere else use underscores.
- `+`-prefixed configs cascade folder → subfolder, with the more specific scope overriding.

Source: [dbt_project.yml reference](https://docs.getdbt.com/reference/dbt_project.yml) · raw: `docs__reference__dbt_project.yml.md`
