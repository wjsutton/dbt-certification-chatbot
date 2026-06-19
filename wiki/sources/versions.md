---
title: "Source summary — versions (resource property)"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "02 — Managing dbt models governance"
source: ../../raw/docs__reference__resource-properties__versions.md
source_url: https://docs.getdbt.com/reference/resource-properties/versions
---

# versions (resource property) — summary

**What it covers:** the `versions` YAML property reference — `v`, `defined_in`, `alias`, `include`/`exclude`, and breaking-change detection.

## Key points

- Each entry under `versions:` needs a **`v`** (required version identifier). Optional per-version `defined_in`, `columns`, `config`.
- **`v`**: numeric (int/float) or any string. Used to **order** versions. If `latest_version` is unset, the **highest** value is latest. Recommend simple major versioning (`1`, `2`, `3`). Do **not** include the letter `v` in the identifier — dbt adds it.
- **`defined_in`**: model file name (no extension) where the version lives. Default search is `<model_name>_v<v>`; the latest may also be `<model_name>` (no suffix). File names must be **globally unique**.
- **`alias`**: default resolved alias is `<model_name>_v<v>` (via `generate_alias_name`). Override in version YAML or by reimplementing the macro. `defined_in` and `alias` are independent.
- **`include` / `exclude`** (which top-level `columns` a version uses):
  - `include`: list of column names, or `'*'` / `'all'` for all top-level columns.
  - `exclude`: list of columns to drop — **only** allowed when `include` is `'*'`/`'all'`.
  - At most **one** `include`/`exclude` element in a version's `columns` list. Default is `include: all`, `exclude: []`.
  - If no version specifies columns, you can omit `columns` entirely and all top-level columns apply.
  - A version-specific column whose `name` matches a top-level one **overrides** it for that version.

## Detecting breaking changes

- With `state:modified` in Slim CI, dbt detects changes to **versioned/contracted** model contracts and errors on potentially breaking changes.
- Breaking examples: removing contract enforcement, removed columns, removed enforced constraints, materialization change with enforced constraints, `data_type` changes.
- **Additive (non-breaking):** adding a new column to a contracted model; adding new `constraints` to an existing column.

## Exam-relevant tokens

`versions`, `v`, `defined_in`, `alias`, `include`, `exclude`, `'*'`/`'all'`, `latest_version`, `state:modified`, `generate_alias_name`

## Gotchas

- `exclude` requires `include: '*'`/`'all'` — you can't `exclude` from a hand-listed include.
- A version with `include: []` includes **none** of the top-level columns (must then declare its own).
- Without `latest_version`, the highest `v` wins as latest.

Source: [versions (resource property)](https://docs.getdbt.com/reference/resource-properties/versions) · raw: `docs__reference__resource-properties__versions.md`
