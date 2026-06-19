---
title: "Source summary — About dbt test command"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__reference__commands__test.md
source_url: https://docs.getdbt.com/reference/commands/test
---

# About dbt test command — summary

**What it covers:** `dbt test`, which runs data tests and unit tests against already-built resources.

## Key points
- `dbt test` runs **data tests** defined on models, sources, snapshots, and seeds, plus **unit tests** defined on SQL models. It expects those resources to already exist (built via other commands).
- Select tests with `--select`:
  - `dbt test` — runs data and unit tests.
  - `dbt test --select test_type:data` — only data tests.
  - `dbt test --select test_type:unit` — only unit tests.
  - `dbt test --select "test_type:singular"` — singular data tests.
  - `dbt test --select "test_type:generic"` — generic data tests.
  - `dbt test --select "one_specific_model"` / `"some_package.*"` — scope to a model or package.
  - Combine, e.g. `dbt test --select "one_specific_model,test_type:data"`.

## Exam-relevant tokens
`dbt test`, `--select`, `test_type:data`, `test_type:unit`, `test_type:singular`, `test_type:generic`, `some_package.*`.

## Gotchas
- `dbt test` does not build models/seeds/snapshots — it tests existing resources. Use `dbt build` to build-and-test in one DAG pass.

Source: [About dbt test command](https://docs.getdbt.com/reference/commands/test) · raw: `docs__reference__commands__test.md`
