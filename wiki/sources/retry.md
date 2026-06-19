---
title: "Source summary — About dbt retry command"
tags: [source-summary, state, retry]
status: done
updated: 2026-06-11
domain: "07 — Leveraging the dbt state"
source: ../../raw/docs__reference__commands__retry.md
source_url: https://docs.getdbt.com/reference/commands/retry
---

# dbt retry — summary

**What it covers:** re-running the **last invocation from its point of failure**, using the previous run's results.

## Key points

- `dbt retry` reads **`run_results.json`** (in the target dir by default) to find where the last command stopped, and resumes from the failed/​skipped nodes — it does **not** re-run already-successful upstream nodes.
- Behavior edge cases:
  - If **no nodes ran** before the failure (e.g. a connection/permission error at startup), retry has nothing to resume — re-run the full job instead.
  - If the previous command **succeeded**, retry is a **no-op** ("Nothing to do").
  - Retrying without fixing the underlying error fails again at the same node.
- **Idempotent:** retrying without changing anything reproduces the same result.
- **Selection is inherited:** with dbt Core, retry reuses the prior command's `--select`/`--exclude`/`--selector`; you **cannot** override them on retry (Core / dbt platform CLI).
- Override flags (Core): `--threads`, `--vars`, `--target`, `--profile`, `--profiles-dir`, `--project-dir`, `--target-path`, `--state`, `--full-refresh`.
- `--state path/` points retry at a different directory containing `run_results.json`.

## Supported commands

`build`, `compile`, `clone`, `docs generate`, `seed`, `snapshot`, `test`, `run`, `run-operation`.

## Exam-relevant tokens

`dbt retry`, `run_results.json`, "from the point of failure", inherited selection, idempotent, no-op on success.

Source: [About dbt retry command](https://docs.getdbt.com/reference/commands/retry) · raw: [`retry.md`](../../raw/docs__reference__commands__retry.md)
