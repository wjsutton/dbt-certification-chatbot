---
title: "Source summary — Add Exposures to your DAG"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "06 — External dependencies"
source: ../../raw/docs__docs__build__exposures.md
source_url: https://docs.getdbt.com/docs/build/exposures
---

# Add Exposures to your DAG — summary

**What it covers:** Defining exposures to describe a downstream use (dashboard, app, ML pipeline) of your dbt project and run/test/list the resources feeding them.

## Key points
- Exposures **define and describe a downstream use** of your project. With them you can run, test, and list resources that feed an exposure, and populate a dedicated docs-site page for data consumers.
- Two ways to define: **Manual** (declared explicitly in YAML) and **Automatic** (dbt creates/visualizes downstream exposures for supported integrations; these live in dbt's metadata system, not in YAML files).
- Declared in `.yml` files nested under an `exposures:` key (e.g. in `models/<filename>.yml`).
- **Required** properties: `name` (unique, snake_case), `type` (one of `dashboard`, `notebook`, `analysis`, `ml`, `application`), and `owner` (`name` or `email` required).
- **Expected:** `depends_on` — a list of refable nodes including `metric`, `ref`, and `source`. (Unlikely you'd ever need an exposure to depend on a `source` directly.)
- **Optional:** `label` (may contain spaces/capitals/special chars), `url` (activates the "View this exposure" link in generated docs), and `maturity` (one of `high`, `medium`, `low` — confidence/stability).
- General optional props: `description`, `tags`, `meta`, `enabled` (settable at exposure level or project level in `dbt_project.yml`).
- Reference exposures in commands with the `exposure:` selection method, e.g. `dbt run -s +exposure:weekly_jaffle_report` and `dbt test -s +exposure:weekly_jaffle_report` — the `+` pulls in upstream parents that feed it.

## Exam-relevant tokens
`exposures:`, `name`, `type` (`dashboard`/`notebook`/`analysis`/`ml`/`application`), `owner`, `depends_on`, `ref`, `source`, `metric`, `label`, `url`, `maturity` (`high`/`medium`/`low`), `+exposure:<name>`

## Gotchas
- The YAML `depends_on` property is **not** the same as the `-- depends_on` SQL comment directive at the top of a model file.
- `name` must be snake_case (letters/numbers/underscores only); use `label` for a human-friendly name with spaces.
- `owner` requires at least `name` or `email`; both `type` and `name` are required while `depends_on` is only "expected".

Source: [Add Exposures to your DAG](https://docs.getdbt.com/docs/build/exposures) · raw: `docs__docs__build__exposures.md`
