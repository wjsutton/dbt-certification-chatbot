---
title: "03 — Debugging data modeling errors"
tags: [exam-domain, concept]
status: done
updated: 2026-06-12
---

# 03 — Debugging data modeling errors

<!-- dbtwiki:auto:subtopics -->
## Sub-topics assessed

- **Understanding logged error messages** — [Debug errors](../sources/debug-errors.md)
- **Troubleshooting using compiled code** — [About dbt compile command](../sources/compile.md)
- **Troubleshooting .yml compilation errors** — [Debug errors](../sources/debug-errors.md)
- **Developing, implementing & testing a fix before merge** — [Best practices for workflows](../sources/best-practice-workflows.md)
- **Managing dbt behavior with flags** — [About flags (global configs)](../sources/about-global-configs.md) · [Behavior changes](../sources/behavior-changes.md)
<!-- /dbtwiki:auto:subtopics -->

## Synthesis

Debugging in dbt starts with **reading the error message**: dbt's messages name both the **error type** and the **file** that caused the problem. The type tells you which step dbt was on. **Initialize** failures (not a dbt project, can't find the profile, can't connect) surface as `Runtime Error`; **parsing** failures (bad Jinja in `.sql`, bad `.yml`) surface as `Compilation Error`; a non-acyclic DAG surfaces as `Dependency Error` ("Found a cycle:"); and warehouse-side SQL failures surface as `Database Error`. Knowing the type narrows where to look before you read a single line of code. See [Debug errors](../sources/debug-errors.md).

When the message isn't enough, **inspect the compiled code**. `target/compiled` holds the plain `select` statements you can paste into a query editor; `target/run` holds the SQL dbt actually executes to build a model (a `Database Error` points you straight at the offending file there); and `logs/dbt.log` records *every* query dbt ran, with the most recent errors at the bottom — the only place to see behind-the-scenes queries like introspection, schema creation, hooks, and incre
<!-- dbtwiki:auto:sources -->
## Source material

- [Debug errors](../raw/docs__guides__debug-errors.md) · summary: [debug-errors](../sources/debug-errors.md) · [original](https://docs.getdbt.com/guides/debug-errors) · `Guide`
- [About dbt compile command](../raw/docs__reference__commands__compile.md) · summary: [compile](../sources/compile.md) · [original](https://docs.getdbt.com/reference/commands/compile) · `Doc`
- [Best practices for workflows](../raw/docs__best-practices__best-practice-workflows.md) · summary: [best-practice-workflows](../sources/best-practice-workflows.md) · [original](https://docs.getdbt.com/best-practices/best-practice-workflows) · `Doc`
- [About flags (global configs)](../raw/docs__reference__global-configs__about-global-configs.md) · summary: [about-global-configs](../sources/about-global-configs.md) · [original](https://docs.getdbt.com/reference/global-configs/about-global-configs) · `Doc`
- [Behavior changes](../raw/docs__reference__global-configs__behavior-changes.md) · summary: [behavior-changes](../sources/behavior-changes.md) · [original](https://docs.getdbt.com/reference/global-configs/behavior-changes) · `Doc`
<!-- /dbtwiki:auto:sources -->
