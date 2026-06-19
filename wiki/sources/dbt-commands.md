---
title: "Source summary — dbt Command reference"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__reference__dbt-commands.md
source_url: https://docs.getdbt.com/reference/dbt-commands
---

# dbt Command reference — summary

**What it covers:** the catalog of dbt commands, which are read vs write, and parallel-execution rules.

## Key points
- Commands are invoked by prefixing with `dbt` (e.g. `dbt test`); also callable programmatically via `dbtRunner.invoke`.
- **Write commands** change data/metadata and are limited to **one invocation at a time** (no parallel write+write). Examples: `dbt build`, `dbt run`, `dbt seed`, `dbt snapshot`, `dbt run-operation`.
- **Read commands** fetch/read without changes and **can run in parallel** with other reads and a single write. Examples: `dbt compile`, `dbt parse`, `dbt test`, `dbt list`, `dbt show`, `dbt docs`, `dbt source`, `dbt clean`, `dbt deps`, `dbt debug`, `dbt retry`.
- `dbt-core` does **not** support safe parallel execution for multiple invocations in the same process; dbt platform does.
- Selected commands relevant to this domain: `build`, `run`, `test`, `seed`, `snapshot`, `docs` (generate documentation), `show` (previews table rows post-transformation), `deps` (downloads dependencies). Use `--version` to show the installed version.

## Exam-relevant tokens
`dbt build`, `dbt run`, `dbt test`, `dbt seed`, `dbt snapshot`, `dbt docs`, `dbt show`, `dbt deps`, write vs read, parallel execution, `dbtRunner.invoke`, `--version`.

## Gotchas
- `build`/`run`/`seed`/`snapshot`/`run-operation` are write commands (one at a time); `compile`/`parse`/`test`/`show`/`list`/`docs` are read commands (parallelizable).
- You cannot run two write commands (e.g. `dbt build` and `dbt run`) in parallel.

Source: [dbt Command reference](https://docs.getdbt.com/reference/dbt-commands) · raw: `docs__reference__dbt-commands.md`
