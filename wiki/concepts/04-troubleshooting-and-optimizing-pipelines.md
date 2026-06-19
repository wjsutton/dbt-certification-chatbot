---
title: "04 — Troubleshooting & optimizing pipelines"
tags: [exam-domain, concept]
status: done
updated: 2026-06-12
---

# 04 — Troubleshooting & optimizing pipelines

<!-- dbtwiki:auto:subtopics -->
## Sub-topics assessed

- **Troubleshooting & managing failure points in the DAG** — [Syntax overview](../sources/syntax.md) · [About dbt retry command](../sources/retry.md)
- **Using dbt clone** — [About dbt clone command](../sources/clone.md) · [Clone incremental models as the first step of your CI job](../sources/clone-incremental-models.md) · [To defer or to clone, that is the question](../sources/to-defer-or-to-clone.md)
<!-- /dbtwiki:auto:subtopics -->

## Synthesis

This domain is about keeping a DAG running and making its builds cheap. The first
sub-topic — **managing failure points in the DAG** — leans on dbt's run artifacts.
When a run fails partway through, [`dbt retry`](../sources/retry.md) reads
**`run_results.json`** to resume the **last invocation from its point of failure**,
re-running only the failed and skipped nodes rather than the whole DAG; it inherits
the prior command's selection and is a no-op when the previous run succeeded. To
re-target failures explicitly you can combine [node selection](../raw/docs__reference__node-selection__syntax.md)
with the `result:` status selector (e.g. `dbt build --select result:fail+`) to
rebuild failed nodes and their downstream dependencies. Together these let you
recover from a broken pipeline without paying to rebuild healthy upstream models.

The second sub-topic — **`dbt clone`** — optimizes builds by avoiding expensive
re-computation. `dbt clone` copies selected nodes from a specified `--state` into the
target schema(s) using the `clone` materialization. On warehouses with **zero-copy
cloning** (Snowflake, Databricks, BigQuery) it copies
<!-- dbtwiki:auto:sources -->
## Source material

- [Syntax overview](../raw/docs__reference__node-selection__syntax.md) · summary: [syntax](../sources/syntax.md) · [original](https://docs.getdbt.com/reference/node-selection/syntax) · `Doc`
- [About dbt retry command](../raw/docs__reference__commands__retry.md) · summary: [retry](../sources/retry.md) · [original](https://docs.getdbt.com/reference/commands/retry) · `Doc`
- [About dbt clone command](../raw/docs__reference__commands__clone.md) · summary: [clone](../sources/clone.md) · [original](https://docs.getdbt.com/reference/commands/clone) · `Doc`
- [Clone incremental models as the first step of your CI job](../raw/docs__best-practices__clone-incremental-models.md) · summary: [clone-incremental-models](../sources/clone-incremental-models.md) · [original](https://docs.getdbt.com/best-practices/clone-incremental-models) · `Doc`
- [To defer or to clone, that is the question](../raw/docs__blog__to-defer-or-to-clone.md) · summary: [to-defer-or-to-clone](../sources/to-defer-or-to-clone.md) · [original](https://docs.getdbt.com/blog/to-defer-or-to-clone) · `Blog`
<!-- /dbtwiki:auto:sources -->
