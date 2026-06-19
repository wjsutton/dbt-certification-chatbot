---
title: "Source summary — Add data tests to your DAG"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "05 — Implementing dbt tests"
source: ../../raw/docs__docs__build__data-tests.md
source_url: https://docs.getdbt.com/docs/build/data-tests
---

# Add data tests to your DAG — summary

**What it covers:** what data tests are, the two ways to define them (singular vs generic), the four built-in generics, running and storing failures.

## Key points

- Data tests are assertions about models, sources, seeds, and snapshots; `dbt test` reports pass/fail. They are `select` statements that grab **failing** records — **zero rows returned = the test passes**.
- **Singular** data test: a one-off `.sql` file with a single `select` in your `tests/` directory (the `test-paths` config). Test name = the file name. Can use Jinja, `ref`, and `source`.
- **Generic** data test: a parameterized query in a `{% test ... %}` block (like a macro) referenced by name in `.yml` on models/columns/sources/snapshots/seeds.
- dbt ships **four** built-in generics: `unique`, `not_null`, `accepted_values`, `relationships`. Apply under the `data_tests:` property; `accepted_values` takes `values:` (under `arguments:` in v1.10.5+), `relationships` takes `to:` and `field:`.
- The YAML key is now `data_tests:`; the old `tests:` key is still supported as an alias (you can't use both on the same resource). The rename disambiguates from **unit tests**.
- **Run only data tests** (excluding unit tests): `dbt test --select "test_type:data"` (works in core and fusion). Core v1.9+ also allows `dbt test --resource-type test`.
- **Store failures:** the `--store-failures` flag, or `store_failures` / `store_failures_as` configs, write failing rows to a table first, then count. Failure tables land in a schema named/suffixed `dbt_test__audit` by default (changeable via `schema` config). A test's results always **replace** the previous failures for that test.

## Exam-relevant tokens

`data_tests:`, `tests:`, `unique`, `not_null`, `accepted_values`, `relationships`, `{% test %}`, `dbt test`, `test-paths`, `test_type:data`, `--resource-type test`, `--store-failures`, `store_failures`, `store_failures_as`, `dbt_test__audit`, `severity`, `tags`

## Gotchas

- Singular tests must **omit trailing semicolons** (`;`) — they cause the test to fail.
- Don't reference singular tests in `model_name.yml`; they aren't generics/macros and it errors.
- The `tests/` (`test-paths`) directory is **only** for singular/generic SQL tests; **unit test YAML must live under `model-paths`** (e.g. `models/`), not `tests/`.

Source: [Add data tests to your DAG](https://docs.getdbt.com/docs/build/data-tests) · raw: `docs__docs__build__data-tests.md`
