---
title: "Source summary — Node selector methods"
tags: [source-summary, state, node-selection]
status: done
updated: 2026-06-12
domain: "07 — Leveraging the dbt state"
source: ../../raw/docs__reference__node-selection__methods.md
source_url: https://docs.getdbt.com/reference/node-selection/methods
---

# Node selector methods — summary

**What it covers:** the full set of `method:value` selectors for `--select`/`--exclude`. For Domain 07 the headline method is **`state:`**; the rest are general node-selection knowledge that also appears across Domains 01 and 05.

## The `state:` method (exam-critical for Domain 07)

Requires a comparison manifest via `--state` (or `DBT_ENGINE_STATE` in 1.11).

- `state:new` — no node with the same `unique_id` in the comparison manifest.
- `state:modified` — all new nodes **plus** any changed existing nodes.
- `state:old` — node with the same `unique_id` exists in the comparison manifest.
- `state:unmodified` — existing nodes with no changes.

Subselectors narrow `modified`: `state:modified.body`, `.configs`, `.relation`,
`.persisted_descriptions`, `.macros`, `.contract`. Note `state:modified.contract`
flags column name/data_type changes — removing/retyping a column is a **breaking change** (errors).

Related state-aware methods: **`result:`** (`result:error`, `result:fail`) selects by prior-run outcome (needs `--state`); **`source_status:fresher+`** selects by source freshness vs prior `sources.json`.

## Other methods worth knowing (cross-domain)

`tag:`, `config.<key>:` (e.g. `config.materialized:incremental`), `path:`/`file:`/`fqn:`,
`package:` (and `package:this`), `resource_type:` (model/test/source/exposure/function),
`source:` (`source:snowplow+`), `exposure:`/`metric:` (parents, use `+`),
`test_type:` (unit/data/generic/singular), `test_name:`, `unit_test:`, `version:`,
`group:`, `access:`, `selector:` (beta, references a named YAML selector).

## Exam-relevant tokens

`state:modified`, `state:new`, `state:old`, `state:modified.contract`, `result:fail`,
`source_status:fresher`, `--state`, `+` (graph operator), `config.materialized:incremental`.

## Gotchas

- `state:` needs a prior manifest; it compares logical definition, not warehouse state.
- `result:fail` is test-only; use `result:error` for any resource type.
- Seeds: < 1 MiB modified on content change; ≥ 1 MiB modified only on path change.

Source: [Node selector methods](https://docs.getdbt.com/reference/node-selection/methods) · raw: [`methods.md`](../../raw/docs__reference__node-selection__methods.md)
