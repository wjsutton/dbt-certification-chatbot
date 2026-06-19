---
title: "Source summary — Debug errors"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "03 — Debugging data modeling errors"
source: ../../raw/docs__guides__debug-errors.md
source_url: https://docs.getdbt.com/guides/debug-errors
---

# Debug errors — summary

**What it covers:** the general debugging process, the four error types dbt raises, and how to use compiled files and logs to fix them.

## Key points

- **General process:** (1) read the error message — it normally contains the **error type** and the **file** where the error occurred; (2) inspect that file; (3) isolate the problem (run one model at a time, or undo the breaking change); (4) get comfortable with compiled files and logs; (5) ask for help.
- The error type maps to the **step** dbt was on:
  - **Initialize** (is this a dbt project / can dbt connect to the warehouse) → `Runtime Error`
  - **Parsing** (Jinja in `.sql` valid, `.yml` valid) → `Compilation Error`
  - **Graph validation** (dependencies compiled into an acyclic graph) → `Dependency Error`
  - **SQL execution** (run the models) → `Database Error`
- Three places to look when stuck:
  - `target/compiled` — `select` statements you can run in any query editor.
  - `target/run` — the SQL dbt actually executes to build models.
  - `logs/dbt.log` — **all** queries dbt runs plus extra logging; **recent errors are at the bottom**.
- **Runtime Errors:** "Not a dbt project" (missing `dbt_project.yml`); "Could not find profile" (the `profile:` key in `dbt_project.yml` must match a profile name in `profiles.yml`); "Failed to connect" (fix credentials, then `dbt debug`); invalid `dbt_project.yml` key ("Additional properties are not allowed").
- **Compilation Errors:** invalid `ref` (depends on a node "which was not found" — fix the model name); invalid Jinja ("Reached EOF without finding a close tag" — e.g. missing `{% endmacro %}`); **invalid YAML** ("Syntax error near line X" / "mapping values are not allowed in this context" — usually **indentation**); incorrect YAML spec (valid YAML but an unrecognized key — "Additional properties are not allowed").
- **Dependency Error:** "Found a cycle:" — the DAG isn't acyclic; fix `ref`s, or use `{{ this }}` to reference the current model.
- **Database Errors:** come from the warehouse; the message points at the compiled SQL (e.g. `target/run/jaffle_shop/models/customers.sql`). Re-run the compiled `select` in a query runner to isolate, fix, rerun. Behind-the-scenes queries (introspection, `create` schema, pre/post/on-run hooks, incremental merge/update/insert) show up only in `logs/dbt.log`.
- **Isolating in logs:** clear `logs/dbt.log`, then re-run `dbt run` for just the problem model so the log holds only that output.

## Exam-relevant tokens

`Runtime Error`, `Compilation Error`, `Dependency Error`, `Database Error`, `target/compiled`, `target/run`, `logs/dbt.log`, `dbt_project.yml`, `profiles.yml`, `profile:`, `dbt debug`, `dbt debug --config-dir`, `{{ this }}`, `{% endmacro %}`, `dbt --version`

## Gotchas

- "Could not find profile" is about the **`profile:` key** matching a profile name — singular vs plural mismatches are a classic trap.
- Invalid-YAML compilation errors are almost always **indentation**; an unrecognized-key error ("Additional properties are not allowed") is a different, valid-YAML-but-wrong-key problem.
- dbt uses the **last-saved** version of a file — unsaved edits won't run. Don't accidentally edit files in `target/`.

Source: [Debug errors](https://docs.getdbt.com/guides/debug-errors) · raw: `docs__guides__debug-errors.md`
