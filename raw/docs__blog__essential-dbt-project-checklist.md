---
title: "Your Essential dbt Project Checklist"
source_url: https://docs.getdbt.com/blog/essential-dbt-project-checklist
retrieved_via: html-extract
fetched: 2026-06-12
---

# Your Essential dbt Project Checklist

A checklist (from dbt Labs audits) for cleaning up a maturing dbt project across performance, maintainability, and onboarding. Organized by area.

## dbt_project.yml
- **Naming:** name the project after your company (e.g. `fishtown_analytics`), not the `my_new_project` default; suffix by domain for multiple projects.
- **Remove unnecessary configs:** views are the default materialization, so don't declare `materialized: view` everywhere; set folder-level materialization in `dbt_project.yml` rather than per-model when a whole folder shares one.
- Remove placeholder comments from `dbt init`.
- Use **post-hooks to grant permissions** (`grants`) so collaborators and BI users keep access.
- **Tags:** most models should be untagged — tag only the exceptions (e.g. `nightly`); prefer **folder selectors** over tagging every model in a folder; consider a **node selector** or **YAML selector** instead of complex tagging.

## Package management
- Keep `packages.yml` versions current vs the Package Hub.
- Install **`dbt_utils`** (essential macros).

## Code style
- Have a clearly defined style guide and follow it; optimize SQL (window functions, aggregations).

## Project structure
- Use **staging and marts** models with prefixes like `fct_`/`dim_`.
- Keep code **modular**: one transformation per model; modular CTEs (one transformation per CTE).
- **Filter as early as possible** — a common mistake is filtering/transforming too late, causing repeated ("wet") logic downstream.
- Name macro files to reflect their contents.

## dbt
- Stay near the **latest dbt version** (old versions keep old bugs and make upgrades harder).
- On `dbt run`: identify longest-running models (reconsider strategy / make **incremental** / adjust incremental strategy); ensure **every model runs**; no circular references.
- Use **sources** (with **source freshness** tests) and use **`ref`/`source` for everything** — nothing should query raw tables directly.
- Run `dbt test` regularly in dev and production jobs.
- Use **Jinja & macros** for repeated code, but keep readable (set blocks at top, whitespace control like `{{ this }}`, in-line docs `{# … #}`, named macro args).
- Incremental models should use **unique keys** and the **`is_incremental()`** macro.

## Testing & CI
- Aim for high **test coverage**; rule of thumb: at least a `not_null`/`unique` test on every primary key.
- Test core business logic and source assumptions.
- Use **version control**, mandatory **PR reviews**, and a PR template.

## Documentation
- Descriptions for each model; explain complex transformations/business logic; maintain a README; use **doc blocks** for column-level descriptions; make onboarding easy.

## dbt Cloud specifics
- Jobs inherit dbt version from the environment (easier upgrades); organize projects; align run frequency with raw-data update cadence; set up a **CI job**; enable failure notifications (Slack); use the IDE.

## DAG auditing — common pitfalls (what NOT to do)
- A source joining directly into an intermediate model, or **sources joining directly together** — every source should have a corresponding **staging model**.
- **Rejoining of upstream concepts** — may need an expanded model or a new intermediate model.
- **"Bending connections"** — models in the same layer depending on each other (rename or reference further upstream).
- **Model fan-outs** of intermediate/dimension/fact models — push transformations upstream or to the BI layer; the project needs a defined end point.
- **Repeated logic** across models (e.g. complex join logic) — move into upstream/intermediate models to make it reusable.
