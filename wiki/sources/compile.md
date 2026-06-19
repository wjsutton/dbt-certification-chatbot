---
title: "Source summary — About dbt compile command"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "03 — Debugging data modeling errors"
source: ../../raw/docs__reference__commands__compile.md
source_url: https://docs.getdbt.com/reference/commands/compile
---

# About dbt compile command — summary

**What it covers:** what `dbt compile` does, where compiled SQL lands, interactive compile, and how to compile tests.

## Key points

- `dbt compile` generates **executable SQL** from source files for **models, data tests, analyses, and functions** (in core v1.11). Snapshots are added in core v1.12.
- Compiled SQL files are written to the **`target/`** directory.
- Useful for: visually inspecting compiled output (validating complex Jinja/macro logic) and **manually running the underlying `select`** while debugging to find the source of a bug; compiling `analysis` files.
- **Misconceptions:** `dbt compile` is **not** a prerequisite of `dbt run` (build commands compile themselves). To read/validate project code **without connecting to the warehouse**, use **`dbt parse`** instead.
- **Interactive compile** (since v1.5): logs compiled code to the terminal *in addition to* writing to `target/`:
  - `dbt compile --select "stg_orders"` — compile a node by name.
  - `dbt compile --inline "select * from {{ ref('raw_orders') }}"` — compile an arbitrary dbt-SQL query.
- Cache/introspection flags:
  - `dbt --no-populate-cache` — disable initial cache population (a **`dbt` flag**, prefixed `dbt`).
  - `dbt compile --no-introspect` — disable introspective queries; dbt **raises an error** if a resource needs one (a **`dbt compile` flag**).
- **Compiling tests:** `dbt compile --select "resource_type:test"` (all tests), `"test_type:generic"`, `"test_type:singular"`. If you get `selection does not match any nodes`, the selector matched nothing — list tests with `dbt ls --resource-type test --select "MODEL_NAME"`, then compile a returned test node name.

## Exam-relevant tokens

`dbt compile`, `target/`, `dbt parse`, `--select`, `--inline`, `--no-populate-cache`, `--no-introspect`, `resource_type:test`, `test_type:generic`, `test_type:singular`, `dbt ls --resource-type test`, `selection does not match any nodes`

## Gotchas

- `--no-populate-cache` is a **top-level `dbt` flag** (`dbt --no-populate-cache`); `--no-introspect` is a **`dbt compile` flag** (`dbt compile --no-introspect`) — the prefix matters.
- Compiled SQL for resources using introspective queries may be **incomplete or differ** depending on warehouse metadata state.
- For pure parse/validation without warehouse access, reach for `dbt parse`, not `dbt compile`.

Source: [About dbt compile command](https://docs.getdbt.com/reference/commands/compile) · raw: `docs__reference__commands__compile.md`
