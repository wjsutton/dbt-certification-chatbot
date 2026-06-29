---
title: "05 — Implementing dbt tests"
tags: [exam-domain, concept]
status: done
updated: 2026-06-29
---

# 05 — Implementing dbt tests

<!-- dbtwiki:auto:subtopics -->
## Sub-topics assessed

- **Generic, singular, custom, custom generic & unit tests** — [Add data tests to your DAG](../sources/data-tests.md) · [Unit tests](../sources/unit-tests.md) · [Writing custom generic data tests](../sources/writing-custom-generic-tests.md) · [Data test configurations](../sources/data-test-configs.md)
- **Testing assumptions for models and sources** — [Add data tests to your DAG](../sources/data-tests.md)
- **Implementing testing steps in the workflow** — [Test smarter not harder: add the right tests](../sources/test-smarter-not-harder.md) · [Test smarter: Where should tests go in your pipeline?](../sources/test-smarter-where-tests-should-go.md)
<!-- /dbtwiki:auto:subtopics -->

## Synthesis

dbt has two families of tests. **Data tests** are assertions that run *after* a model is built; they are `select` statements that return failing rows, so **zero rows = pass**. They come in two flavours: **singular** tests (a one-off `.sql` file with a single `select` in your `tests/` directory, named by its filename) and **generic** tests (a parameterized `{% test %}` block referenced by name in `data_tests:` YAML on a model, column, source, seed, or snapshot). dbt ships four built-in generics — `unique`, `not_null`, `accepted_values`, and `relationships` — which should form the bulk of your suite. You can write your own **custom generic** tests as `{% test name(model, column_name) %}` blocks (in `tests/generic/` or `macros/`), add extra arguments like `relationships`' `field`/`to`, set defaults via an in-block `{{ config(...) }}`, or even override a built-in by redefining a block of the same name. **Unit tests** are the second family: they validate SQL *logic* against static `given` inputs and an `expect`ed output *before* the model materializes (TDD-style), defined under `unit_tests:` in YAML that must live under `model-paths` (not `tests/`). Reserve them for complex logic (regex, window functions, date math, many-branch `case when`) and run them only in dev/CI.

These tests express **assumpti
<!-- dbtwiki:auto:sources -->
## Source material

- [Add data tests to your DAG](../raw/docs__docs__build__data-tests.md) · summary: [data-tests](../sources/data-tests.md) · [original](https://docs.getdbt.com/docs/build/data-tests) · `Doc`
- [Unit tests](../raw/docs__docs__build__unit-tests.md) · summary: [unit-tests](../sources/unit-tests.md) · [original](https://docs.getdbt.com/docs/build/unit-tests) · `Doc`
- [Writing custom generic data tests](../raw/docs__best-practices__writing-custom-generic-tests.md) · summary: [writing-custom-generic-tests](../sources/writing-custom-generic-tests.md) · [original](https://docs.getdbt.com/best-practices/writing-custom-generic-tests) · `Guide`
- [Data test configurations](../raw/docs__reference__data-test-configs.md) · summary: [data-test-configs](../sources/data-test-configs.md) · [original](https://docs.getdbt.com/reference/data-test-configs) · `Doc`
- [Test smarter not harder: add the right tests](../raw/docs__blog__test-smarter-not-harder.md) · summary: [test-smarter-not-harder](../sources/test-smarter-not-harder.md) · [original](https://docs.getdbt.com/blog/test-smarter-not-harder) · `Blog`
- [Test smarter: Where should tests go in your pipeline?](../raw/docs__blog__test-smarter-where-tests-should-go.md) · summary: [test-smarter-where-tests-should-go](../sources/test-smarter-where-tests-should-go.md) · [original](https://docs.getdbt.com/blog/test-smarter-where-tests-should-go) · `Blog`
<!-- /dbtwiki:auto:sources -->
