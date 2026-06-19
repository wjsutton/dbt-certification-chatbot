---
title: "Source summary — grants config"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__reference__resource-configs__grants.md
source_url: https://docs.getdbt.com/reference/resource-configs/grants
---

# grants config — summary

**What it covers:** the `grants` resource config that applies database permissions (GRANT/REVOKE) at build time to models, seeds, and snapshots.

## Key points
- Define `grants` as a resource config on each **model, seed, or snapshot**, project-wide in `dbt_project.yml`, or model-specific in SQL/YAML. When a resource finishes building, dbt ensures the object's grants match exactly what you configured.
- When you `run`/`seed`/`snapshot`, dbt runs `grant`/`revoke` statements so DB permissions match the config. Two parts: **privilege** (e.g. `select`) and **grantees** (users/groups/roles/service accounts).
- YAML config form (a list of grantees per privilege):
  ```yml
  config:
    grants:
      select: ['reporter', 'bi']
  ```
  In `dbt_project.yml` use the `+` prefix: `+grants:` then `select: [...]` (the `+` is required there for the project to parse).
- **Inheritance (merge & clobber):** more-specific grants **replace** less-specific grantees by default. Prefix a privilege with `+` (e.g. `'+select'`) to **add** rather than clobber: `{{ config(grants = {'+select': ['user_c']}) }}` adds `user_c` to existing grantees. Each privilege controls this independently.
- **Revoking:** dbt only modifies grants when a `grants` config is attached. Deleting the whole `+grants` section means dbt stops managing grants (changes nothing). To revoke all, give an **empty list**: `select: []`.
- Can be set in `.sql` via `{{ config(grants = {...}) }}` and varied with Jinja (e.g. different grantees in prod vs dev). DB-specific: BigQuery uses `roles/...` and prefixed grantees (`user:`); Redshift uses `group:`/`role:` prefixes; OSS Spark/Delta don't support grants.

## Exam-relevant tokens
`grants`, `+grants`, `select`, privilege, grantees, `'+select'` (add vs clobber), `select: []` (revoke all), `{{ config(grants = {...}) }}`, `dbt_project.yml`.

## Gotchas
- Default behavior is "merge and clobber" — a more-specific grant replaces the broader grantee list; use `+privilege` to add instead.
- In `dbt_project.yml` the `+` on `+grants` is mandatory; the `+` on `+select` (inside grants) toggles add-vs-clobber.
- To revoke all grants use an empty list `[]`; deleting the section entirely makes dbt stop managing grants (no change).

Source: [grants](https://docs.getdbt.com/reference/resource-configs/grants) · raw: `docs__reference__resource-configs__grants.md`
