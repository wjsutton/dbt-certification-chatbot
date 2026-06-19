---
title: "Source summary — Source configurations"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__reference__source-configs.md
source_url: https://docs.getdbt.com/reference/source-configs
---

# Source configurations — summary

**What it covers:** the configs available on sources and how to set them inline or from `dbt_project.yml`.

## Key points
- Source configs (v1.9+) support `enabled`, `event_time`, `meta`, and `freshness`.
- Sources can be configured via a `config:` block inside the `.yml` definition, or under the `sources:` key in `dbt_project.yml`. The `dbt_project.yml` form is most useful for sources imported from a package.
- In `dbt_project.yml` you use the `+` prefix on configs (`+enabled`, `+event_time`, `+freshness`, `+meta`) and a **resource path** (project → subdirectory → source name → table name) to scope them.
- **Disable all package sources:** put `+enabled: false` under the project name in the resource path. This prevents them rendering in docs and stops freshness checks on package source tables.
- **Conditionally enable** a single source/table inline with `config: { enabled: true|false }`; you can use `var()` as input, e.g. `enabled: "{{ var('my_source_table_enabled', false) }}"`.
- **Disable a single source/table from a package** by qualifying the resource path with package name → source name (→ table name) and `+enabled: false`.
- `event_time` marks the column holding the actual event timestamp (not the load date); required for the **incremental microbatch** strategy and used to align CI vs production comparisons.
- `meta` attaches arbitrary metadata (e.g. `source_system`, `data_owner`).
- `freshness` config: provide one or both of `warn_after`/`error_after` (each `count` + `period: minute | hour | day`); if neither is given, dbt won't calculate freshness snapshots.
- You can also override `database`/`schema` on a source via the inline `config`/properties.

## Exam-relevant tokens
`enabled`, `event_time`, `meta`, `freshness`, `config:`, `+enabled`, `+event_time`, `+freshness`, `+meta`, `warn_after`, `error_after`, `count`, `period`, resource path, `var()`

## Gotchas
- To disable a source table nested in a subfolder properties file, the resource path in `dbt_project.yml` must include the subfolder(s) as well as source and table name.
- `event_time` represents the event time, not the loading date — required for microbatch.

Source: [Source configurations](https://docs.getdbt.com/reference/source-configs) · raw: `docs__reference__source-configs.md`
