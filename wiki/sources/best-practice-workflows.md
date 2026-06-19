---
title: "Source summary — Best practices for workflows"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "03 — Debugging data modeling errors"
source: ../../raw/docs__best-practices__best-practice-workflows.md
source_url: https://docs.getdbt.com/best-practices/best-practice-workflows
---

# Best practices for workflows — summary

**What it covers:** the recommended dbt workflow — version control, separate environments, testing, and developing/testing a fix before merge ("slim CI").

## Key points

- **Version control everything.** Manage the dbt project in git; create branches for features/bug fixes; **all code changes should be reviewed in a Pull Request before merging** into a production branch such as `main`.
- **Separate dev and prod environments** via **targets within a profile** — use a `dev` target from the CLI and a `prod` target only for production deployment.
- **Use a style guide** (SQL style, field naming) so multiple users write consistent code.
- **Use the `ref` function** when selecting from another model (not direct `my_schema.my_table`) so dbt infers dependencies and builds in the right order and environment.
- **Limit references to raw data**; define raw data as **sources** and select from the source.
- **Rename and recast fields once** in the first transformation layer; **break complex models into smaller pieces** (especially when a CTE is duplicated, changes the grain, or the SQL is long); **group models in directories**; **add tests** (at minimum, every model has a primary key tested **unique** and **not_null**).
- **Develop/test a fix before merge ("slim CI"):** run in a sandboxed environment as an automatic git-workflow check. Compare to artifacts from a previous production run to build only modified models on top of unmodified parents:
  - `dbt run -s state:modified+ --defer --state path/to/prod/artifacts`
  - `dbt test -s state:modified+ --defer --state path/to/prod/artifacts`
- **Result-status selectors** (from a prior run's `run_results.json`): `result:fail`, `result:error`, `result:warn`, `result:success`, `result:skipped`, `result:pass`. Use e.g. `dbt build --select state:modified+ result:error+ --defer --state path/to/prod/artifacts` for smarter reruns. Only supported by **v1.1 or newer**.
- **Source freshness reruns:** compare `sources.json` artifacts and use `source_status:fresher+` (must run `dbt source freshness` to capture previous state first).
- **Pro-tips:** limit data in dev with `{% if target.name == 'dev' %}` filters or the `DBT_CLOUD_INVOCATION_CONTEXT` env var; use **`grants`** resource configs to manage privileges in version control; whitespace from Jinja shows up in `target/compiled`.

## Exam-relevant tokens

Pull Request, `main`, `dev`/`prod` targets, `ref`, `sources`, `unique`, `not_null`, `state:modified+`, `--defer`, `--state`, `result:error`, `result:fail`, `result:warn`, `result:success`, `result:skipped`, `result:pass`, `source_status:fresher+`, `dbt source freshness`, `run_results.json`, `sources.json`, `grants`, `target.name`

## Gotchas

- With `--state target/`, `result:error` and `result:fail` can be selected together in the **same command only with `dbt build`** — `dbt test` overwrites `run_results.json` from a prior `dbt run`.
- `state:modified+` builds modified models **on top of unmodified parents** via `--defer` to prod artifacts — you don't rebuild the whole project.
- Result-status selectors require a previous run's artifacts and v1.1+.

Source: [Best practices for workflows](https://docs.getdbt.com/best-practices/best-practice-workflows) · raw: `docs__best-practices__best-practice-workflows.md`
