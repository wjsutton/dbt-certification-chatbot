---
title: "Source summary — About dbt source command"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "06 — External dependencies"
source: ../../raw/docs__reference__commands__source.md
source_url: https://docs.getdbt.com/reference/commands/source
---

# About dbt source command — summary

**What it covers:** The `dbt source` command and its single subcommand `dbt source freshness`, including output artifacts and source selection.

## Key points
- `dbt source` provides one subcommand: **`dbt source freshness`**.
- If the project is configured with sources, `dbt source freshness` **queries all defined source tables** to determine freshness. If a table is stale (per its `freshness` config), dbt reports a **warning or error**, and a stale source causes dbt to **exit with a nonzero exit code**.
- Freshness is configured under `sources:` → `config:` → `freshness:` with `warn_after: {count, period}` and `error_after: {count, period}`, plus `loaded_at_field` (changed to `config` in v1.9 / v1.10). `freshness` can be overridden per `table` and disabled with `freshness: null`.
- **Output artifact:** when it completes, a JSON file is written to **`target/sources.json`** with `max_loaded_at`, `snapshotted_at`, `max_loaded_at_time_ago_in_s`, `state` (e.g. `pass`), and the `criteria` (`warn_after`/`error_after`).
- Override the output path with **`-o` / `--output`**, e.g. `dbt source freshness --output target/source_freshness.json`.
- **Select a subset** with `--select` using the `source:` method: `--select "source:snowplow"` (all tables) or `--select "source:snowplow.event"` (one table). By default it calculates freshness for all sources.
- Recommended to run on a schedule and store snapshots over time so SLA violations can be alerted and trends tracked.

## Exam-relevant tokens
`dbt source freshness`, `--select "source:<name>"`, `source:<name>.<table>`, `-o` / `--output`, `target/sources.json`, `warn_after`, `error_after`, `count`, `period`, `loaded_at_field`, `filter`, `freshness: null`, `state` (`pass`)

## Gotchas
- A stale source makes `dbt source freshness` exit **nonzero** — this is what fails a run-step in a job.
- Default output path is `target/sources.json`; use `--output`/`-o` to redirect.
- `dbt source` has exactly one subcommand (`freshness`) — there is no separate freshness command outside `dbt source`.

Source: [About dbt source command](https://docs.getdbt.com/reference/commands/source) · raw: `docs__reference__commands__source.md`
