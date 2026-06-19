---
title: "07 — Leveraging the dbt state"
tags: [exam-domain, concept]
status: done
updated: 2026-06-12
---

# 07 — Leveraging the dbt state

<!-- dbtwiki:auto:subtopics -->
## Sub-topics assessed

- **Understanding state & state selection** — [About local state in dbt](../sources/state-selection.md) · [Node selector methods](../sources/methods.md) · [Defer](../sources/defer.md)
- **Using dbt retry** — [About dbt retry command](../sources/retry.md)
<!-- /dbtwiki:auto:subtopics -->

## Synthesis

dbt is deliberately **stateless and idempotent** — a run only needs the project code and the current database to produce a deterministic result. "State" is therefore not required for correctness; it's an **optimization**. dbt records a point-in-time view of every node and result in its **artifacts** (chiefly `manifest.json` and `run_results.json`), and you can feed a *previous* run's artifacts back in with the **`--state`** flag to unlock four state-aware capabilities:

1. **State selection** — the `state:` method (`state:modified`, `state:new`, `state:old`, `state:unmodified`) compares the current project against the state manifest to select only what changed. `modified` has subselectors (`state:modified.body`, `.configs`, `.contract`, `.macros`, …); `state:modified.contract` flags breaking column changes. Related: `result:fail`/`result:error` (select by prior-run outcome) and `source_status:fresher`.
2. **Deferral** — `--defer` resolves an unbuilt upstream `ref` to the state environment (e.g. production) instead of failing, so you can build/test a handful of nodes in a sandbox.
3. **Cloning** — `dbt clone` uses the state manifest to decide what to zero-copy clone (covered in Domain 04).
4. **Retry** — `dbt retry` reads `run_results.json` to resume the last command **from its point of failure**, skipping work that already succeeded.

The first two combine into **"Slim CI"**: compare against production state to find modified models (`state:modified`), then `--defer` their unbuilt parents to production — so CI builds and tests only what changed instead of the whole DAG. The key mental model for the exam: `--state` is a **prerequisite flag** that points at a prior manifest; the *selectors and flags* (`state:`, `--defer`, `--favor-state`) are what act on it. Deferral is **lazy** (no new objects; reference prebuilt models), which makes it ideal for CI, whereas cloning is **eager** (real copied objects), which suits CD — a contrast worth memorising (see the *To defer or to clone* note once ingested).

`dbt retry` rounds out the domain as the recovery tool: after a partial failure, fix the offending model and `dbt retry` resumes only the failed/skipped nodes (inheriting the original selection in dbt Core). It's a no-op after a clean run and idempotent if you retry without fixing anything.

## Key tokens to know

`--state`, `manifest.json`, `run_results.json`, `state:modified` / `state:new` / `state:old`, `--defer`, `--defer-state`, `--favor-state`, `DBT_ENGINE_STATE`, `dbt retry`, "Slim CI", stateless, idempotent.

## Related pages

- **Domain 04 — Troubleshooting & optimizing pipelines**: `dbt clone` is the third `--state` consumer; defer-vs-clone is the recurring comparison.
- **Domain 01**: `state:modified` selection builds on node-selection syntax.
- [Node selector methods](../sources/methods.md) — the full `state:` reference (incl. `state:modified` subselectors), now ingested. **Domain 07 complete.**

<!-- dbtwiki:auto:sources -->
## Source material

- [About local state in dbt](../raw/docs__reference__node-selection__state-selection.md) · summary: [state-selection](../sources/state-selection.md) · [original](https://docs.getdbt.com/reference/node-selection/state-selection) · `Doc`
- [Node selector methods](../raw/docs__reference__node-selection__methods.md) · summary: [methods](../sources/methods.md) · [original](https://docs.getdbt.com/reference/node-selection/methods) · `Doc`
- [Defer](../raw/docs__reference__node-selection__defer.md) · summary: [defer](../sources/defer.md) · [original](https://docs.getdbt.com/reference/node-selection/defer) · `Doc`
- [About dbt retry command](../raw/docs__reference__commands__retry.md) · summary: [retry](../sources/retry.md) · [original](https://docs.getdbt.com/reference/commands/retry) · `Doc`
<!-- /dbtwiki:auto:sources -->
