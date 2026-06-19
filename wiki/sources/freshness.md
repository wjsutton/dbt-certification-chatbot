---
title: "Source summary — freshness (resource property)"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "06 — External dependencies"
source: ../../raw/docs__reference__resource-properties__freshness.md
source_url: https://docs.getdbt.com/reference/resource-properties/freshness
---

# freshness (resource property) — summary

**What it covers:** The `freshness` block on sources — `warn_after`/`error_after`, `loaded_at_field`/`loaded_at_query`, `filter`, hierarchy, and metadata-based freshness.

## Key points
- A `freshness` block defines the acceptable time between the most recent record and now for a table to be "fresh". Provide **one or both** of `warn_after` and `error_after`; **if neither is provided, dbt will not calculate freshness** for those tables.
- `warn_after`: duration after which dbt raises a **warning** if data is older than the threshold. `error_after`: duration after which dbt **fails** the freshness check.
- Each threshold takes `count` (positive integer, required) and `period` (required, one of **`minute` | `hour` | `day`**).
- `loaded_at_field`: a column name or expression returning a timestamp. **Required in most cases**, but optional on adapters that can pull freshness from warehouse metadata tables (Snowflake, Redshift, BigQuery 1.7.3+, Databricks fusion_engine).
  - If `loaded_at_field` is provided → freshness via a select query. If not provided → via warehouse metadata when possible.
- **v1.10+ `loaded_at_query`:** custom SQL to generate `maxLoadedAt`; **must not be used if `loaded_at_field` is defined** (if both are set, dbt uses whichever is closest to the table). `filter` won't work for `loaded_at_query`.
- `filter`: adds a `where` clause to the freshness query to limit scanned data; **only** applies to freshness queries, not other uses of the source. Useful for partitioned BigQuery tables / large Snowflake/Databricks/Spark tables.
- **Hierarchy:** a `freshness`/`loaded_at_field` on a source applies to all its tables; the same on a source **table overrides** the source-level value. Set **`freshness: null`** to exclude a table from freshness.
- `freshness` and `loaded_at_field` **changed to `config`** in v1.9 and v1.10 respectively.

## Exam-relevant tokens
`freshness`, `warn_after`, `error_after`, `count`, `period` (`minute`/`hour`/`day`), `loaded_at_field`, `loaded_at_query`, `filter`, `freshness: null`, `config:`

## Gotchas
- No `warn_after`/`error_after` ⇒ **no freshness calculated**; explicit `freshness: null` ⇒ table excluded.
- `loaded_at_query` (v1.10+) and `loaded_at_field` are mutually exclusive; `filter` does not apply to `loaded_at_query`.
- Table-level `freshness` overrides source-level — they don't merge.
- Metadata-based freshness (no `loaded_at_field`) only works on supported adapters.

Source: [freshness (resource property)](https://docs.getdbt.com/reference/resource-properties/freshness) · raw: `docs__reference__resource-properties__freshness.md`
