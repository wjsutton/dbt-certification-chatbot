---
title: "06 — External dependencies"
tags: [exam-domain, concept]
status: done
updated: 2026-06-12
---

# 06 — External dependencies

<!-- dbtwiki:auto:subtopics -->
## Sub-topics assessed

- **Implementing dbt exposures** — [Add Exposures to your DAG](../sources/exposures.md) · [Exposure properties](../sources/exposure-properties.md)
- **Implementing source freshness** — [Source freshness](../sources/source-freshness.md) · [About dbt source command](../sources/source.md) · [freshness (resource property)](../sources/freshness.md)
<!-- /dbtwiki:auto:subtopics -->

## Synthesis

This domain is about the two boundaries of a dbt project: what feeds *in* (raw sources, monitored for freshness) and what depends *out* (the dashboards, apps, and ML pipelines that consume the project's outputs). **Exposures** describe those downstream uses. You declare them in `.yml` files under an `exposures:` key with a required `name` (snake_case), `type` (`dashboard`, `notebook`, `analysis`, `ml`, or `application`), and `owner` (`name` or `email`), plus an *expected* `depends_on` listing the `ref()`, `source()`, and `metric()` nodes that feed the exposure. Once declared, the `exposure:` selection method lets you operate on everything that feeds a downstream use: `dbt run -s +exposure:weekly_jaffle_report` and `dbt test -s +exposure:weekly_jaffle_report`, where the leading `+` pulls in the upstream parents. Optional `label`, `url`, and `maturity` (`high`/`medium`/`low`) enrich the auto-generated docs page. Note in v1.10 `tags`/`meta` moved under a `config:` block, and only `enabled` can be set at the project level in `dbt_project.yml`.

On t
<!-- dbtwiki:auto:sources -->
## Source material

- [Add Exposures to your DAG](../raw/docs__docs__build__exposures.md) · summary: [exposures](../sources/exposures.md) · [original](https://docs.getdbt.com/docs/build/exposures) · `Doc`
- [Exposure properties](../raw/docs__reference__exposure-properties.md) · summary: [exposure-properties](../sources/exposure-properties.md) · [original](https://docs.getdbt.com/reference/exposure-properties) · `Doc`
- [Source freshness](../raw/docs__docs__deploy__source-freshness.md) · summary: [source-freshness](../sources/source-freshness.md) · [original](https://docs.getdbt.com/docs/deploy/source-freshness) · `Doc`
- [About dbt source command](../raw/docs__reference__commands__source.md) · summary: [source](../sources/source.md) · [original](https://docs.getdbt.com/reference/commands/source) · `Doc`
- [freshness (resource property)](../raw/docs__reference__resource-properties__freshness.md) · summary: [freshness](../sources/freshness.md) · [original](https://docs.getdbt.com/reference/resource-properties/freshness) · `Doc`
<!-- /dbtwiki:auto:sources -->
