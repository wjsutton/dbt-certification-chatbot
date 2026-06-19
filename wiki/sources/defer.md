---
title: "Source summary — Defer"
tags: [source-summary, state, defer]
status: done
updated: 2026-06-11
domain: "07 — Leveraging the dbt state"
source: ../../raw/docs__reference__node-selection__defer.md
source_url: https://docs.getdbt.com/reference/node-selection/defer
---

# Defer — summary

**What it covers:** running a subset of models/tests/functions without first building their upstream parents, by pointing unresolved `ref`s at another environment's state.

## Key points

- `--defer` lets you build/test a few nodes in a sandbox; unbuilt parents resolve to the **state** environment instead of erroring.
- Requires **both** `--defer` **and** `--state path/` (or env vars `DBT_ENGINE_DEFER` + `DBT_ENGINE_STATE` in 1.11).
- Resolution rule — when `--defer` is on, dbt resolves a `ref` (or `function`) from the **state manifest** only if: (1) the node isn't in the selected set, **and** (2) it doesn't exist in the target database (or `--favor-state` is passed).
- **`--favor-state`** flips the priority to prefer the state node even if it exists locally (unless it's selected).
- **Ephemeral models are never deferred** (they're passthroughs for other refs).
- You can split state: `--state` (for `state:modified` comparison) vs `--defer-state` (the environment to defer to). If `--defer-state` is omitted, defer reuses `--state`.

## Worked example (from the doc)

Working on `model_b` locally (schema `dev_alice`) with no parents built:
- `dbt run --select "model_b"` → compiles `from dev_alice.model_a` → **fails**, parent doesn't exist.
- `dbt run --select "model_b" --defer --state prod-run-artifacts` → compiles `from prod.model_a` → **succeeds**. The same applies to `dbt test` (e.g. a `relationships` test resolves the unbuilt parent to `prod.model_a`).

## Defer vs clone (one-liner)

Defer **lazily references** prebuilt models in the source schema (no new objects; CI). Clone **eagerly copies** a schema via zero-copy clone (real objects usable in BI; CD). See concept page and the *To defer or to clone* note.

## Exam-relevant tokens

`--defer`, `--state`, `--defer-state`, `--favor-state`, `DBT_ENGINE_STATE`, "Slim CI", ephemeral-never-deferred.

Source: [Defer](https://docs.getdbt.com/reference/node-selection/defer) · raw: [`defer.md`](../../raw/docs__reference__node-selection__defer.md)
