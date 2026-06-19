---
title: "Source summary — Writing custom generic data tests"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "05 — Implementing dbt tests"
source: ../../raw/docs__best-practices__writing-custom-generic-tests.md
source_url: https://docs.getdbt.com/best-practices/writing-custom-generic-tests
---

# Writing custom generic data tests — summary

**What it covers:** how to author your own generic ("schema") tests as `{% test %}` blocks, standard vs extra arguments, default configs, and overriding built-ins.

## Key points

- The four built-ins (`not_null`, `unique`, `relationships`, `accepted_values`) are themselves `test` blocks (formerly "schema tests"). You can write your own.
- Custom generic tests are SQL files that live in **`tests/generic/`** (a `generic` subfolder of your `test-paths`) **or** in **`macros/`** (handy when the test depends on complex macro logic).
- Define with `{% test <test_name>(model, column_name) %} ... {% endtest %}`. Standard arguments: `model` (always named `model`, even for sources/seeds/snapshots — templated to the relation) and `column_name` (only if the test is column-level). The test passes when the `select` returns **zero rows**.
- Use it by name in a resource's `data_tests:` property; dbt passes the resource as `model` and the column as `column_name`.
- **Additional arguments:** add them to the signature (e.g. `relationships(model, column_name, field, to)`) and supply them from YAML under `arguments:` (v1.10.5+; older versions set them as top-level properties).
- **Default config values:** put a `{{ config(...) }}` block inside the test block (e.g. `{{ config(severity = 'warn') }}`) to set defaults for every instance; a specific instance's `.yml` config overrides it.
- **Override a built-in:** add a `test` block with the same name (e.g. `{% test unique(model, column_name) %}`) in your project and dbt favors yours over the global one.
- **Documenting the test macro:** add a `description` under `macros:` in a `schema.yml`; prefix the macro name with `test_` (a block named `not_empty_string` → macro `test_not_empty_string`). You can describe each argument.

## Exam-relevant tokens

`{% test %}`, `{% endtest %}`, `model`, `column_name`, `field`, `to`, `arguments:`, `tests/generic/`, `macros/`, `config(severity='warn')`, `test_` prefix, override built-in tests

## Gotchas

- The `model` argument is **always** called `model` even when the tested resource is a source, seed, or snapshot.
- To document the macro logic, the macro name needs the `test_` prefix; the test block name does not.
- A generic test's `{{ config() }}` defaults are overridden by the specific instance's YAML config.

Source: [Writing custom generic data tests](https://docs.getdbt.com/best-practices/writing-custom-generic-tests) · raw: `docs__best-practices__writing-custom-generic-tests.md`
