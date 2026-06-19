---
title: "Source summary — Materializations best practices"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__best-practices__materializations__1-guide-overview.md
source_url: https://docs.getdbt.com/best-practices/materializations/1-guide-overview
---

# Materializations best practices (overview) — summary

**What it covers:** what materializations are conceptually and the tiered guiding principle for the three core ones.

## Key points
- Materializations are the configs that tell dbt **how to construct objects** in the warehouse when you `dbt build`.
- They make transformation **declarative** — they abstract away DDL/DML, so you declare what you want and dbt figures out the how given the warehouse.
- The three main/core materializations that ship with dbt are **table**, **view**, and **incremental** — they cover most analytics-engineering situations.
- You can configure materializations at various scopes, from an individual model up to an entire folder.
- **Guiding principle: start as simple as possible**, follow a tiered approach, only moving up a tier when necessary:
  - **Start with a view.** When the view gets too long to *query* for end users →
  - **Make it a table.** When the table gets too long to *build* in your dbt jobs →
  - **Build it incrementally** — layer the data on in chunks as it comes in.

## Exam-relevant tokens
`table`, `view`, `incremental`, materializations, declarative, folder-level config, tiered approach

## Gotchas
- The escalation trigger differs per tier: views escalate on **query** time, tables escalate on **build** time.
- Always start simple (view) and only escalate when there's an actual performance problem.

Source: [Materializations best practices](https://docs.getdbt.com/best-practices/materializations/1-guide-overview) · raw: `docs__best-practices__materializations__1-guide-overview.md`
