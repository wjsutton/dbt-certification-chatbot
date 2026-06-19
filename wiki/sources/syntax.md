---
title: "Source summary — Node selection syntax overview"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__reference__node-selection__syntax.md
source_url: https://docs.getdbt.com/reference/node-selection/syntax
---

# Node selection syntax overview — summary

**What it covers:** how `--select`/`--exclude` choose a subset of DAG nodes, and the graph-operator shorthand for traversing the DAG.

## Key points
- Node selection runs subsets of resources for: `run`, `test`, `seed`, `snapshot`, `ls`/`list`, `compile`, `freshness`, `build`, `docs generate`.
- Nodes / resources = models, tests, sources, seeds, snapshots, exposures, analyses — the objects making up dbt's **DAG (directed acyclic graph)**.
- In dbt Core **1.11** the relevant flags include `--select`, `--exclude`, `--selector` (and `--defer` on run/test/build). `--select` shorthand is `-s`.
- By default `dbt run` executes **all** models; `--select` runs a subset. Use quotes around selectors for POSIX safety.
- Selection order: **selection methods** (e.g. `tag:`) → **graph operators** (e.g. `+`) → **set operators** (unions = space, intersections = comma, exclusions).
- A `--select` argument can be a package name, model name, path to a directory of models, or a selection method (`path:`, `tag:`, `config:`, `test_type:`, `test_name:`, `selector:`).
- **Graph operators** (DAG traversal shorthand):
  - **plus `+`** — `my_model+` selects the model **and all its children (descendants)**; `+my_model` selects the model **and all its parents (ancestors)**. A number limits depth, e.g. `1+model` / `model+1`.
  - **at `@`** — `@my_model` selects the model, its children, **and the parents of its children**.
  - **asterisk `*`** — wildcard (e.g. `finance.base.*`).
  - **comma `,`** — intersection (e.g. `path:marts/finance,tag:nightly,config.materialized:table`).
- `dbt ls`/`list` previews what a selector will match (e.g. `dbt ls --select state:modified+`, `source_status:fresher+`).

## Exam-relevant tokens
`--select`, `-s`, `--exclude`, `--selector`, `--defer`, `+` (children/parents), `1+model`, `@`, `*`, `,` (intersection), space (union), `path:`, `tag:`, `config.materialized:table`, `source_status:fresher+`, `state:modified+`, `dbt ls`, DAG

## Gotchas
- `+` placement matters: trailing `model+` = descendants, leading `+model` = ancestors; a number caps the hops (`2+model`).
- `@model` adds the parents of the model's children (useful so children build cleanly).
- Use quotes around `--select` args for reliable cross-platform behavior; `--selector` ignores `--select`/`--exclude`.

Source: [Syntax overview](https://docs.getdbt.com/reference/node-selection/syntax) · raw: `docs__reference__node-selection__syntax.md`
