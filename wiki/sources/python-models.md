---
title: "Source summary — Python models"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__docs__build__python-models.md
source_url: https://docs.getdbt.com/docs/build/python-models
---

# Python models — summary

**What it covers:** authoring dbt Python (`dbt-py`) models that return a DataFrame, referencing upstream resources, and configuring them.

## Key points
- Each Python model lives in a **`.py`** file in `models/` and defines a function **`def model(dbt, session)`** that must **return a single DataFrame**.
  - `dbt`: a class compiled by dbt Core unique to each model (project/DAG context).
  - `session`: the data platform's connection to the Python backend (used to read/write tables as DataFrames).
- Reference upstream resources with **`dbt.ref("model_name")`** (SQL or Python models) and **`dbt.source("source_name", "table_name")`**; these return DataFrames. You can `ref()` a Python model in downstream SQL too.
- Only specific platforms support `dbt-py` (e.g. Snowflake/Snowpark, BigQuery, Databricks/PySpark). All Python code runs **remotely on the platform**, not locally by dbt.
- Configure three ways: in `dbt_project.yml`, a dedicated `.yml`, or in-file via **`dbt.config(...)`** (literal values + dynamic config only). Access config with `dbt.config.get(...)`; check incremental with `dbt.is_incremental`; current relation via `dbt.this`; custom meta via `dbt.config.meta_get()`.
- Python models don't use Jinja to render compiled code; they have limited project context via the `dbt` class.
- Referencing ephemeral models is not supported.

## Exam-relevant tokens
`def model(dbt, session)`, `return final_df`, `dbt.ref(...)`, `dbt.source(...)`, `dbt.config(...)`, `dbt.config.get(...)`, `dbt.is_incremental`, `dbt.this`, `dbt.config.meta_get()`, `.py` in `models/`, DataFrame.

## Gotchas
- The function must be named `model` and take exactly `(dbt, session)`, returning one DataFrame.
- `dbt.config()` accepts only literal/dynamic values — not functions or complex structures (set those in a YAML config).
- The `--empty` and `--sample` flags are ignored for Python models; ephemeral refs are unsupported.

Source: [Python models](https://docs.getdbt.com/docs/build/python-models) · raw: `docs__docs__build__python-models.md`
