---
title: "Source summary — About dbt build command"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__reference__commands__build.md
source_url: https://docs.getdbt.com/reference/commands/build
---

# About dbt build command — summary

**What it covers:** the `dbt build` command, which runs models, tests, snapshots, seeds (and functions in v1.11) in DAG order in one pass.

## Key points
- `dbt build` will, in DAG order, **run** models, **test** tests, **snapshot** snapshots, **seed** seeds, and (from dbt Core v1.11) **build** user-defined functions.
- Writes a **single** `manifest.json` and a **single** `run_results.json` covering all selected models, tests, seeds, and snapshots combined.
- **Skipping on failures:** tests on upstream resources block downstream resources; a test failure (severity `error`) causes downstream resources to `SKIP`. Set severity/thresholds to `warn` to avoid skipping.
- Supports standard selection (`--select`, `--exclude`, `--selector`) plus `--resource-type` as a final filter. Supports all the same flags as `run`, `test`, `snapshot`, `seed`; shared flags like `--full-refresh` apply the same value to all selected resource types.
- Indirect test selection: `dbt build -s model_a` runs **and** tests `model_a`.
- Unit + data tests ordering: unit tests run on the SQL model, then the model is materialized, then data tests run — saving warehouse spend (model only materializes if unit tests pass). Select with `--select test_type:unit` / `test_type:data`.
- Build only functions with `dbt build --select "resource_type:function"` (v1.11+).

### The `--empty` flag
- `dbt build --empty` does a schema-only dry run: limits refs/sources to **zero rows**, still executes model SQL against the warehouse, validating dependencies without expensive reads.

## Exam-relevant tokens
`dbt build`, `--select`, `--exclude`, `--selector`, `--resource-type`, `--full-refresh`, `--empty`, `test_type:unit`, `test_type:data`, `resource_type:function`, `manifest.json`, `run_results.json`, `SKIP`, severity `warn`/`error`.

## Gotchas
- A single `build` produces one manifest + one run results file (not per-resource).
- A failing `error`-severity test blocks-and-skips downstream resources; `warn` does not.
- `build` runs ALL resource types by default — to limit, use selection or `--resource-type`.

Source: [About dbt build command](https://docs.getdbt.com/reference/commands/build) · raw: `docs__reference__commands__build.md`
