---
title: "Source summary — Refactoring legacy SQL to dbt"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__guides__refactoring-legacy-sql.md
source_url: https://docs.getdbt.com/guides/refactoring-legacy-sql
---

# Refactoring legacy SQL to dbt — summary

**What it covers:** the 6-step process for turning legacy SQL/stored procedures into modular dbt models.

## Key points
- Two parts: **migration** (get it running in dbt) then **refactoring** (make it modular). The six steps:
  1. **Migrate code 1:1 into dbt** — copy the legacy query into a `.sql` file under `/models`, then `dbt run`. Move logic around, but don't change it (more changes = more auditing).
  2. **Implement sources** rather than referencing raw DB tables — use `{{ source('my_source','my_table') }}` instead of `my_database.my_schema.my_table`. This unlocks source freshness reporting, easy dependency tracing (see which queries share raw tables), and the analytics-as-code habit.
  3. **Choose a refactoring strategy** — **in-place** (edit the ported model directly) or **alongside** (copy into `/marts` and edit the copy). dbt Labs generally recommends **alongside**: less end-user impact, smaller PRs, easier auditing (run old vs new side-by-side).
  4. **Implement CTE groupings + cosmetic cleanup** — restructure into a 4-part layout: **Import CTEs** (simple `select * from {{ source() }}`, filters allowed), **Logical CTEs** (unique transformations, one per block, no nesting), a **Final CTE**, then a simple `select * from final`. CTE = Common Table Expression (a temp result set, introduced with `with`).
  5. **Separate transformations into standardized layers** — port CTEs into modular models: identify **staging models** from import CTEs; promote complex/reusable logical CTEs to **intermediate models** (optional); the **final model** produces the result set.
  6. **Audit output of dbt models vs legacy SQL** — use the dbt **`audit_helper`** package to generate before/after comparison queries.
- Sources also let you remap schemas (e.g. after switching ETL tools) in a single config file via one PR.

## Exam-relevant tokens
`{{ source() }}`, `/models`, `/marts`, in-place vs alongside, CTE, `with`, Import CTEs, Logical CTEs, Final CTE, `select * from final`, staging models, intermediate models, `audit_helper`, `dbt run`

## Gotchas
- Migrate logic unchanged first — don't fix bugs during the move; card them for later to minimize auditing.
- **Alongside** is the recommended refactoring strategy (easier to audit / less risk than in-place).
- Import CTEs should be `select *` (filters optional); avoid nested subqueries — each becomes its own CTE.

Source: [Refactoring legacy SQL to dbt](https://docs.getdbt.com/guides/refactoring-legacy-sql) · raw: `docs__guides__refactoring-legacy-sql.md`
