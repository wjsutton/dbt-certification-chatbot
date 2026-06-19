---
title: "Source summary — Unit tests"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "05 — Implementing dbt tests"
source: ../../raw/docs__docs__build__unit-tests.md
source_url: https://docs.getdbt.com/docs/build/unit-tests
---

# Unit tests — summary

**What it covers:** validating SQL modeling logic on small static inputs **before** materializing a model; when/where to use unit tests, their YAML shape, and exit codes.

## Key points

- Unit tests validate modeling **logic** against static `given` inputs and an `expect`ed output **before** the model is built — enabling test-driven development. Contrast: data tests run **after** a model is built.
- Defined under the `unit_tests:` key in YAML, with `name`, `model`, `given` (a list of `input:` + `rows`), and `expect`. Mock data formats: `dict`, `csv`, or `sql` (inline or in a `fixtures/` subdirectory of a test path).
- **Where YAML lives:** unit test definitions live under `model-paths` (e.g. `models/`), not in `tests/`.
- **When to add one:** complex SQL — regex, date math, window functions, many-branch `case when`, truncation; custom function-like logic; previously-buggy logic; edge cases; before a significant refactor; high-criticality (public/contracted/upstream-of-exposure) models. **Don't** unit test warehouse functions like `min()`.
- **When to run:** dev and CI only — inputs are static so running in production wastes compute. Exclude from prod builds with `--exclude-resource-type` or the `DBT_ENGINE_EXCLUDE_RESOURCE_TYPES` env var (1.11; `DBT_EXCLUDE_RESOURCE_TYPES` in ≤1.10).
- **Run only unit tests:** `dbt test --select "test_type:unit"`. Also `dbt test --select "dim_customers,test_type:unit"` or by name `dbt test --select <unit_test_name>`.
- **Direct parents must already exist** in the warehouse before a unit test runs. Use `--empty` to build empty versions cheaply, e.g. `dbt run --select "stg_customers top_level_email_domains" --empty`. `dbt build` runs unit tests → materializes → runs data tests in lineage order.
- **Incremental models:** override `is_incremental` (and macros/vars/env vars) per test to cover full-refresh vs incremental modes. Expected output = the **result of the materialization** (what's merged/inserted), not the final table.
- Models depending on **ephemeral** models must use `format: sql` for that input.

## Exam-relevant tokens

`unit_tests:`, `given`, `input`, `expect`, `format: dict|csv|sql`, `fixtures`, `test_type:unit`, `--empty`, `dbt build`, `overrides`, `is_incremental`, `--exclude-resource-type`, `DBT_ENGINE_EXCLUDE_RESOURCE_TYPES`

## Gotchas

- **Exit codes:** a unit test is one test case → result is always **0 (pass)** or **1 (fail)** regardless of failing-row count. Data tests instead report the **number of failing records**.
- Unit test YAML in `tests/` won't be picked up — it must be under `model-paths`.

Source: [Unit tests](https://docs.getdbt.com/docs/build/unit-tests) · raw: `docs__docs__build__unit-tests.md`
