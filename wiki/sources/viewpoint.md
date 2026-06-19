---
title: "Source summary — The dbt Viewpoint"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__community__resources__viewpoint.md
source_url: https://docs.getdbt.com/community/resources/viewpoint
---

# The dbt Viewpoint — summary

**What it covers:** the foundational philosophy behind dbt — applying software-engineering workflow practices to analytics, including modularity.

## Key points
- Mature analytics has shifted from proprietary end-to-end tools to **composable solutions**: data integration tools, high-performance analytic databases, SQL/R/Python, and visualization tools.
- Core thesis: analytics teams have a **workflow problem** (siloed knowledge, rewritten analyses, inconsistent metric definitions); the fix is to borrow software-engineering practices.
- A mature analytics workflow should be **collaborative**, with:
  - **Version Control** — analytic code (SQL/Python/etc.) should be version controlled so you know who changed what, when.
  - **Quality Assurance** — any code that generates data/analysis should be reviewed and tested.
  - **Documentation** — your analysis is a software application; ship it with descriptions of how to interpret it.
  - **Modularity** — don't copy-paste; if a definition changes it must update everywhere. Treat a dataset's **schema as its public interface**; create tables/views that expose a consistent schema and can be modified if business logic changes.
- **Analytic code is an asset**, so the workflow needs: multiple **Environments** (dev vs prod), **Service level guarantees** (stand behind production accuracy; deprecate retired code), and **Design for maintainability** (anticipate schema/data changes).
- Analytics workflows require **automated tooling** — the whole build (download, configure for environment, test, deploy) should run with a **single command**.

## Exam-relevant tokens
modularity, version control, quality assurance, documentation, environments, service level guarantees, maintainability, "schema as public interface", DRY, single-command automation

## Gotchas
- The Viewpoint is the conceptual root of DRY/modularity in dbt: reuse the same input data, treat schema as a public interface, never copy-paste definitions.
- It frames testing, docs, version control, and environments as first-class analytics requirements, not optional extras.

Source: [The dbt Viewpoint](https://docs.getdbt.com/community/resources/viewpoint) · raw: `docs__community__resources__viewpoint.md`
