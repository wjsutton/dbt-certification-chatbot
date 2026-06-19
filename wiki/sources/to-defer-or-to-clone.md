---
title: "Source summary — To defer or to clone, that is the question"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "04 — Troubleshooting & optimizing pipelines"
source: ../../raw/docs__blog__to-defer-or-to-clone.md
source_url: https://docs.getdbt.com/blog/to-defer-or-to-clone
---

# To defer or to clone, that is the question — summary

**What it covers:** guidance on **when** to use `dbt clone` (shipped in dbt-core v1.6) versus **deferral**, beyond the docs on how to clone.

## Key points
- `dbt clone` leverages native **zero-copy clone** to copy entire schemas almost instantly for free: the warehouse copies only **metadata** (the pointer) source→target; the underlying data stays at rest. If zero-copy isn't available, dbt creates **pointer views** (`select * from my_model`).
- Both clone and defer save cost by **bypassing expensive re-computation**, but:
  - **clone** *eagerly copies* an entire schema into the target;
  - **defer** *lazily references* pre-built models in the source schema.
- First-order differences:
  - **How used:** defer is implicit via the `--defer` flag; clone is explicit via the `dbt clone` command.
  - **Outputs:** defer creates no objects itself; clone copies objects into the target schema, **persisted** afterward.
  - **How it works:** defer compares manifests and overrides `ref` to resolve unbuilt models to the source run's objects; clone copies objects via zero-copy (or pointer views).
- Second-order differentiators: clone's target objects are usable in **any downstream tool (BI)** and can be **safely modified** (sandbox of prod), but they **drift** from source (point-in-time) and support only **one source → one target**. Defer's objects are usable **only within dbt**, must **not** be modified (would touch prod data), **never drift** (always latest source), and can mix **multiple dynamic sources** (prod + staging).
- Rule of thumb: **deferral suits CI; cloning suits CD**. They can be combined across the deployment lifecycle.

## Exam-relevant tokens
`dbt clone`, `--defer`, zero-copy clone, pointer view, metadata copy, `ref` override, manifest comparison, data drift, point-in-time copy, CI vs CD

## Gotchas
- Defer never drifts (always points at latest source) but clone is a **point-in-time** copy that **will** drift.
- Defer can dynamically mix multiple source schemas; clone is strictly one source → one target.
- Modifying defer's target objects would alter **prod data**; clone gives a safe, cheap sandbox copy you can modify.

Source: [To defer or to clone, that is the question](https://docs.getdbt.com/blog/to-defer-or-to-clone) · raw: `docs__blog__to-defer-or-to-clone.md`
