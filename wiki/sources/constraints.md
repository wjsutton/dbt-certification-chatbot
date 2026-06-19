---
title: "Source summary — constraints (resource property)"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "02 — Managing dbt models governance"
source: ../../raw/docs__reference__resource-properties__constraints.md
source_url: https://docs.getdbt.com/reference/resource-properties/constraints
---

# constraints (resource property) — summary

**What it covers:** defining `constraints` in YAML, the constraint structure, prerequisites, and how enforcement varies by data platform.

## Key points

- Constraints are validated by the **data platform** as data is populated. If validation fails, the table create/update **fails and rolls back** with a clear error.
- **Prerequisites:** materialization must be `table` or `incremental` (never `view`/`ephemeral`), **and** the model must declare and **enforce a contract** (`data_type` for every column).
- **Constraint structure:**
  - `type` (required): one of `not_null`, `unique`, `primary_key`, `foreign_key`, `check`, `custom`.
  - `expression`: free text to qualify the constraint (required for some types).
  - `name` (optional): human-friendly name (platform-dependent).
  - `columns` (model-level only): list of columns the constraint covers.
- **Single-column** constraints are recommended directly on the column. **Multiple `primary_key`** constraints must be defined at the **model level** (column-level multiple PKs unsupported).
- **Foreign keys** (1.9+) accept `to:` (a `ref()`/`source()`) and `to_columns:` — capturing dependencies and working across environments.
- Two optional warning fields on any constraint:
  - `warn_unenforced: False` — skip warnings for constraints supported but **not enforced** (e.g. `primary_key` in Snowflake); still included in DDL.
  - `warn_unsupported: False` — skip warnings for constraints the platform **doesn't support** (e.g. `check` in Redshift); excluded from DDL.

## Platform enforcement (exam-critical)

- **Most analytical platforms enforce only `not_null`**; others are metadata/informational only.
- **Postgres:** enforces all ANSI constraints + `check`.
- **Redshift:** enforces only `not_null`; doesn't allow column `check` at table creation.
- **Snowflake:** only `not_null` (and the not-null part of `primary_key`) is checked; `unique`/`primary_key`/`foreign_key` are metadata; `check` is **not supported** (skipped + warns). Use `rely` in `expression` for query optimization.
- **BigQuery:** enforces `not_null`; defines but does **not** enforce `primary_key`/`foreign_key`; no other constraints.
- **Databricks:** `not_null` and `check`; columns checked by name/order, not type; created without schema then `alter`'d.

## Exam-relevant tokens

`constraints`, `type`, `not_null`, `unique`, `primary_key`, `foreign_key`, `check`, `custom`, `expression`, `to`, `to_columns`, `warn_unenforced`, `warn_unsupported`, `rely`

## Gotchas

- Constraints require a contract — they don't work standalone or on views.
- A `not_null`/`check` may be **definable in YAML but not enforced** depending on platform; only `not_null` is broadly enforced.
- Use a `unique` **data test** alongside a `primary_key` constraint because the constraint isn't enforced on Snowflake/Redshift/BigQuery.

Source: [constraints (resource property)](https://docs.getdbt.com/reference/resource-properties/constraints) · raw: `docs__reference__resource-properties__constraints.md`
