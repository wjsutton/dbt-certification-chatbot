---
title: "Source summary — Add snapshots to your DAG"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__docs__build__snapshots.md
source_url: https://docs.getdbt.com/docs/build/snapshots
---

# Add snapshots to your DAG — summary

**What it covers:** what snapshots are (type-2 SCD) and how to configure them in YAML with strategy, unique_key, and meta columns.

## Key points
- Snapshots record changes to a mutable source table over time, implementing **type-2 Slowly Changing Dimensions** — preserving history that would otherwise be overwritten.
- dbt adds meta fields `dbt_valid_from` and `dbt_valid_to` (current record has `dbt_valid_to = NULL` by default).
- **From v1.9, configure snapshots in YAML** (place files in `models/` or a `snapshots/` directory):
  ```yaml
  snapshots:
    - name: orders_snapshot
      relation: source('jaffle_shop', 'orders')   # or ref('my_model')
      config:
        strategy: timestamp | check
        unique_key: id
        updated_at: updated_at        # required for timestamp strategy
        check_cols: [status] | all    # required for check strategy
  ```
- **Required configs:** `strategy` (`timestamp` or `check`) and `unique_key`. `updated_at` is required for the `timestamp` strategy; `check_cols` (a list or `all`) is required for the `check` strategy.
- Other configs: `database`, `schema`, `alias`, `dbt_valid_to_current`, `snapshot_meta_column_names`, `hard_deletes` (`ignore` default / `invalidate` / `new_record`).
- Apply transformations by referencing an **ephemeral model** in `relation` instead of `source()` directly.
- Run with `dbt snapshot` (or via `dbt build`); reference downstream with `{{ ref('orders_snapshot') }}`. In v1.9, `target_schema` became optional (snapshots are environment-aware via `generate_schema_name`).

## Exam-relevant tokens
`snapshots:`, `relation`, `strategy: timestamp|check`, `unique_key`, `updated_at`, `check_cols`, `all`, `hard_deletes` (`ignore`/`invalidate`/`new_record`), `dbt_valid_from`, `dbt_valid_to`, `dbt_valid_to_current`, `dbt snapshot`.

## Gotchas
- `timestamp` strategy requires `updated_at`; `check` strategy requires `check_cols`. Timestamp is preferred (handles column add/remove; tracks only one column).
- Snapshots are now defined in YAML (v1.9+), not legacy Jinja `{% snapshot %}` blocks.
- For SCD2 use snapshots — not the `delete+insert` incremental strategy.

Source: [Add snapshots to your DAG](https://docs.getdbt.com/docs/build/snapshots) · raw: `docs__docs__build__snapshots.md`
