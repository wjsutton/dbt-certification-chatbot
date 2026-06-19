---
title: "Source summary — About dbt snapshot command"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__reference__commands__snapshot.md
source_url: https://docs.getdbt.com/reference/commands/snapshot
---

# About dbt snapshot command — summary

**What it covers:** the `dbt snapshot` command, which executes snapshots (type-2 SCD) defined in the project.

## Key points
- `dbt snapshot` executes the snapshots defined in your project, recording changes to source data over time as **type-2 Slowly Changing Dimensions**. Run it on a schedule (e.g. daily) to capture changes.
- Define snapshots in **YAML** with a `strategy` and `unique_key` (see Snapshot configurations). Snapshots can also run as part of `dbt build`.
- dbt looks for snapshots in the directories listed in `snapshot-paths` in `dbt_project.yml`; by default the `snapshots/` directory. Multiple paths supported.
- Use `--select` / `--exclude` to choose which snapshots run; other global flags (`--threads`, `--target`, logging) supported.

## Exam-relevant tokens
`dbt snapshot`, `dbt build`, type-2 SCD, `strategy`, `unique_key`, `snapshot-paths`, `snapshots/`, `--select`, `--exclude`, `--threads`, `--target`.

## Gotchas
- Snapshots are configured in YAML (with `strategy` + `unique_key`), not a standalone Jinja-only block in v1.9+.
- `dbt snapshot` is a write command and runs the same snapshots that `dbt build` would run as part of the DAG.

Source: [About dbt snapshot command](https://docs.getdbt.com/reference/commands/snapshot) · raw: `docs__reference__commands__snapshot.md`
