---
title: "To defer or to clone, that is the question"
source_url: https://docs.getdbt.com/blog/to-defer-or-to-clone
retrieved_via: html-extract
fetched: 2026-06-12
---

# To defer or to clone, that is the question

Guidance on **when** to use `dbt clone` (shipped in dbt-core v1.6) versus deferral, beyond the docs on *how* to clone. Answers three FAQs: what is `dbt clone`, how it differs from deferral, and which to choose.

## What is `dbt clone`?

`dbt clone` leverages native **zero-copy clone** functionality on supported warehouses to **copy entire schemas for free, almost instantly**. The warehouse "cheats" by copying only **metadata** from the `source` schema to the `target` schema; the underlying data stays at rest. In CS terms, clone copies the *pointer* to the underlying data — afterward two schemas point at the same data. (If zero-copy isn't available, dbt creates pointer views `select * from my_model`.)

## How is cloning different from deferral?

Both save warehouse cost by **bypassing expensive re-computation** — but:
- **clone** *eagerly copies* an entire schema into the target schema;
- **defer** *lazily references* pre-built models in the source schema.

**First-order effects:**
- **How used:** defer is implicit via the `--defer` flag; clone is explicit via the `dbt clone` command.
- **Outputs:** defer creates no objects itself (though dbt may build changed objects in the target); clone copies objects into the target schema, **persisted** after the operation.
- **How it works:** defer compares manifests between source and target runs and overrides `ref` to resolve unbuilt models to the source run's objects; clone uses zero-copy cloning (or pointer views) to copy objects source→target.

**Second-order effects (the real differentiators):**

| Question | defer | clone |
|----------|-------|-------|
| Where can I use the target-schema objects? | only within dbt | any downstream tool (e.g. BI) |
| Can I safely modify target-schema objects? | No (would modify prod data) | Yes (cheap sandbox of prod) |
| Will target data drift from source? | No (always points to latest source) | Yes (point-in-time copy) |
| Multiple source schemas at once? | Yes (mix prod + staging dynamically) | No (one source → one target) |

## Should I defer or should I clone? (cheat sheet)

| Goal | defer | clone |
|------|-------|-------|
| Save time/cost by avoiding re-computation | ✅ | ✅ |
| Create DB objects available in downstream tools (BI) | ❌ | ✅ |
| Safely modify objects in the target schema | ❌ | ✅ |
| Avoid creating new database objects | ✅ | ❌ |
| Avoid data drift | ✅ | ❌ |
| Support multiple dynamic sources | ✅ | ❌ |

## Putting it in practice

- **Testing staging datasets in BI** (copy prod into BI, iterate safely) → **clone**.
- **Slim CI** (reference prod where possible; only run/test changed models; mix prod + staging) → **defer**.
- **Blue/Green deployments** (build entire staging dataset, test it, only promote to prod if all tests pass) → **clone**.

**Rule of thumb:** deferral suits **continuous integration (CI)**; cloning suits **continuous deployment (CD)**. They can be used together in different parts of the deployment lifecycle.
