---
title: "Source summary — How we structure our dbt projects"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__best-practices__how-we-structure__1-guide-overview.md
source_url: https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview
---

# How we structure our dbt projects (overview) — summary

**What it covers:** why project structure matters and the three primary model layers (staging → intermediate → marts) that drive modularity.

## Key points
- Structure = files, folders, naming conventions, and programming patterns; consistency frees the team's limited decision bandwidth for hard problems, not for where folders go.
- Foundational principle: build a cohesive arc moving data from **source-conformed** (shaped by external systems we don't control) to **business-conformed** (shaped by our needs, concepts, and definitions).
- Stacking transformations in optimized, **modular layers** means each transformation is applied in **only one place** (DRY).
- The three primary layers live in the `models/` directory and build on each other:
  1. **Staging** — create the atoms / initial modular building blocks from source data (`stg_<source>__<entity>.sql`, with `base/` models where needed).
  2. **Intermediate** — stack layers of logic with clear, specific purposes to prepare staging models to join into entities (`int_*` models).
  3. **Marts** — bring the modular pieces together into wide, rich, business-conformed entities (e.g. `orders`, `customers`).
- Example project (Jaffle Shop) has sources `jaffle_shop` (transactional replica) and `stripe` (payments), organized as `models/staging/<source>/`, `models/intermediate/<domain>/`, `models/marts/<domain>/`.
- Other top-level folders: `seeds/`, `macros/`, `snapshots/`, `tests/`, `analyses/`, plus `dbt_project.yml` and `packages.yml`.
- YAML files are co-located per folder (`_<source>__sources.yml`, `_<domain>__models.yml`).

## Exam-relevant tokens
`models/`, staging, intermediate, marts, source-conformed, business-conformed, `stg_`, `int_`, `base/`, modular layers, DRY, `seeds/`, `macros/`, `snapshots/`, `tests/`, `analyses/`

## Gotchas
- Intermediate models are optional — use them only when logic gets complex or reusable.
- The whole point of layering is "apply each transformation in only one place" — that is the DRY argument for the logical flow staging → intermediate → marts.

Source: [How we structure our dbt projects](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview) · raw: `docs__best-practices__how-we-structure__1-guide-overview.md`
