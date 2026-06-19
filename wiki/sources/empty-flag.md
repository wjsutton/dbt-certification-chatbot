---
title: "Source summary — About the --empty flag"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__docs__build__empty-flag.md
source_url: https://docs.getdbt.com/docs/build/empty-flag
---

# About the `--empty` flag — summary

**What it covers:** the `--empty` flag for schema-only dry runs that validate model logic/schema without reading input data.

## Key points
- `--empty` **limits refs and sources to zero rows**. dbt still **executes the model SQL** against the target warehouse but avoids expensive reads of input data — validating dependencies and that models build properly.
- Supported on `run`, `build`, `snapshot`, and `compile`. From dbt Core **v1.12**, `seed` also supports `--empty` (not in 1.11).
- Examples: `dbt run --empty`; `dbt run --select path/to/your_model --empty`. Result: an empty schema is built in the warehouse.
- **Not available for Python models** — if used with a Python model the flag is **ignored**.

## Exam-relevant tokens
`--empty`, zero rows, schema-only dry run, `dbt run --empty`, `dbt build --empty`, `--select`, validate dependencies.

## Gotchas
- `--empty` still executes the SQL (so it validates logic/schema) — it just feeds zero rows from refs/sources.
- Ignored for Python models. Contrast with `--sample` (builds a time-based slice of real rows rather than zero rows).

Source: [About the --empty flag](https://docs.getdbt.com/docs/build/empty-flag) · raw: `docs__docs__build__empty-flag.md`
