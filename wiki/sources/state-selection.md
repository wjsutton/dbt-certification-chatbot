---
title: "Source summary — About local state in dbt"
tags: [source-summary, state]
status: done
updated: 2026-06-11
domain: "07 — Leveraging the dbt state"
source: ../../raw/docs__reference__node-selection__state-selection.md
source_url: https://docs.getdbt.com/reference/node-selection/state-selection
---

# About local state in dbt — summary

**What it covers:** what "state" means in dbt, and the `--state` flag that unlocks state-aware operations.

## Key points

- dbt operations are **stateless** and **idempotent**: given the same code, manifest, and raw data, a run produces the same result regardless of history.
- dbt nonetheless *stores* state — a point-in-time view of nodes, database objects, and invocation results — in its **artifacts** (chiefly `manifest.json`).
- You make a prior run's artifacts available by passing their directory to the **`--state`** flag. This is the prerequisite for three features:
  - the **`state:` selector** (`state:modified`, `state:new`) — selects resources that changed vs. the state manifest;
  - **deferral** (`--defer`) — resolve unbuilt upstream `ref`s to another environment;
  - **`dbt clone`** — clone nodes based on their location in the state manifest.
- The `state:` selector + deferral together enable **"Slim CI"** (build/test only modified models against production state).

## Exam-relevant tokens

`--state path/`, `state:modified`, `state:new`, `state:old`, `manifest.json`, "Slim CI", stateless, idempotent.

## Gotchas

- State selection compares against **whatever manifest you point `--state` at** — usually production. Stale or wrong artifacts give misleading "modified" sets.
- State is a *prerequisite flag*, not a command: it modifies `run`/`build`/`test`/`clone`, etc.

Source: [About local state in dbt](https://docs.getdbt.com/reference/node-selection/state-selection) · raw: [`state-selection.md`](../../raw/docs__reference__node-selection__state-selection.md)
