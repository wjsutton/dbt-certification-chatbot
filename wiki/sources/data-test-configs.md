---
title: "Source summary — Data test configurations"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "05 — Implementing dbt tests"
source: ../../raw/docs__reference__data-test-configs.md
source_url: https://docs.getdbt.com/reference/data-test-configs
---

# Data test configurations — summary

**What it covers:** the three places data tests can be configured, their precedence order, and the available config keys (`severity`, `where`, `store_failures`, etc.).

## Key points

- Data tests can be configured in **three** ways, applied **hierarchically by specificity**:
  1. `.yml` properties (generic tests only)
  2. a `config()` block inside the test's SQL
  3. `dbt_project.yml`
- **Precedence for a generic test instance:** `.yml` properties > the generic SQL definition's `config()` > `dbt_project.yml`. **For a singular test:** the SQL `config()` block beats `dbt_project.yml`.
- **Test-specific configs:** `fail_calc`, `limit`, `severity` (`error | warn`), `error_if`, `warn_if`, `store_failures`, `where`. (v1.12+: `sql_header`, gated behind the `require_sql_header_in_test_configs` behavior flag.)
- **General configs:** `enabled`, `tags`, `meta`, and (for `store_failures` only) `database`, `schema`, `alias`.
- The `.yml` config mechanism is supported for **specific instances of generic tests only**; to configure a **singular** test, use the `config()` macro in its SQL.
- `severity` sets `error` vs `warn`; `error_if` / `warn_if` let you set thresholds (e.g. fail only beyond N failing rows). `where` filters the rows a test evaluates; `limit` caps returned rows; `fail_calc` customizes the failure calculation.
- Examples: tag one test via `config: { tags: ['my_tag'] }`; disable all tests from a package with `data_tests: { package_name: { +enabled: false } }`. From v1.9 you can use **any custom config key** (e.g. `snowflake_warehouse`) to run a test on a different warehouse.
- Descriptions on both generic and singular tests are available from v1.9.

## Exam-relevant tokens

`severity`, `error_if`, `warn_if`, `where`, `limit`, `fail_calc`, `store_failures`, `enabled`, `tags`, `meta`, `+enabled: false`, `config()`, `dbt_project.yml`, `sql_header`, `require_sql_header_in_test_configs`

## Gotchas

- `.yml` config blocks only apply to **generic** test instances; singular tests must use the `config()` macro in their `.sql`.
- Config precedence: most specific wins — instance `.yml` > generic `config()` > project YAML.
- `database`/`schema`/`alias` configs only matter when `store_failures` is enabled.

Source: [Data test configurations](https://docs.getdbt.com/reference/data-test-configs) · raw: `docs__reference__data-test-configs.md`
