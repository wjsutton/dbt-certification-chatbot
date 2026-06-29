---
title: "01 — Developing & optimizing dbt models"
tags: [exam-domain, concept]
status: done
updated: 2026-06-29
---


# 01 — Developing & optimizing dbt models

<!-- dbtwiki:auto:subtopics -->
## Sub-topics assessed

- **Identifying & verifying raw object dependencies** — [Add sources to your DAG](../sources/sources.md) · [Source configurations](../sources/source-configs.md) · [Source freshness](../sources/source-freshness.md)
- **Understanding core dbt materializations** — [Materializations](../sources/materializations.md) · [Materialization best practices (guide)](../sources/materializations-1-guide-overview.md) · [Best practices for materializations](../sources/materializations-5-best-practices.md)
- **Modularity & DRY principles** — [How we structure our dbt projects](../sources/how-we-structure-1-guide-overview.md) · [Refactoring legacy SQL to dbt](../sources/refactoring-legacy-sql.md) · [The dbt Viewpoint](../sources/viewpoint.md)
- **Commands: build, run, test, docs, show, snapshot, seed** — [About dbt build command](../sources/build.md) · [About dbt run command](../sources/run.md) · [About dbt test command](../sources/test.md) · [About dbt docs commands](../sources/cmd-docs.md) · [dbt Command reference](../sources/dbt-commands.md) · [About dbt snapshot command](../sources/snapshot.md) · [About dbt seed command](../sources/seed.md)
- **Logical flow of models & clean DAGs** — [Syntax overview](../sources/syntax.md) · [How we structure our dbt projects](../sources/how-we-structure-1-guide-overview.md)
- **Defining configurations in dbt_project.yml** — [dbt_project.yml reference](../sources/dbt_project.yml.md)
- **Using dbt Packages** — [Packages](../sources/packages.md)
- **Creating Python Models** — [Python models](../sources/python-models.md)
- **Providing access with the grants config** — [grants (resource config)](../sources/grants.md)
- **Creating snapshots in YAML** — [Add snapshots to your DAG](../sources/snapshots.md)
- **Selecting the optimal incremental strategy** — [About incremental strategy](../sources/incremental-strategy.md) · [About incremental models](../sources/incremental-models-overview.md)
- **Validating logic/schema in dry-runs (--empty flag)** — [About the `--empty` flag](../sources/empty-flag.md)
- **Running models in sample mode (--sample flag)** — [About the `--sample` flag](../sources/sample-flag.md)
- **Advanced materializations such as microbatch** — [About microbatch incremental models](../sources/incremental-microbatch.md)
<!-- /dbtwiki:auto:subtopics -->

## Synthesis

**Development-speed flags (`--empty` and `--sample`).** Both let you build models without paying for the full dataset, and they form a natural pair on the exam. `--empty` limits all refs and sources to **zero rows**: dbt still executes the model SQL against the warehouse, so it validates dependencies and that models build (a schema-only dry run), but tests against the result pass trivially because there's no data. `--sample` goes one step further — it builds against a **time-based slice** of real data, so you can validate actual outputs while keeping build time and warehouse spend low. Because sampling is time-based, every sampled `ref`/source needs an **`event_time`** config; samples can be **relative** (`--sample="3 days"`) or **static** (`{'start': ..., 'end': ...}`), and an individual ref can opt out with `.render()`. Both flags are available on `run`/`build`; `--sample` is ignored for Python models. See [sample-flag](../sources/sample-flag.md).

**Sources & raw object dependencies.** Raw warehouse tables loaded by EL tools are declared as **sources** in `.yml` files under a `sources:` key (`name`, `database`, `schema`, `tables:`). You then select from them with the `{{ source('jaffle_shop', 'orders') }}` Jinja function, which dbt compiles to the fully-qualified `database.schema.table` and — crucially — **registers a dependency** between the model and the source in the DAG. This is how you identify and verify raw object dependencies: every `{{ source() }}` (and `{{ ref() }}`) call is an edge in the graph. Sources can also carry data tests and a `freshness` block (`warn_after`/`error_after`, each `{count, period}`, plus a `loaded_at_field`); `dbt source freshness` evaluates them and `dbt build --select source_status:fresher+` builds only what's downstream of freshly-loaded sources. Source configs (`enabled`, `event_time`, `meta`, `freshness`) can be set inline or in `dbt_project.yml` under `sources:`, using the `+` prefix and a resource path — handy for disabling package-imported sources. See [sources](../sources/sources.md), [source-configs](../sources/source-configs.md).

**The three core materializations + the Golden Rule.** A materialization is the strategy dbt uses to persist a model; it makes transformation declarative by abstracting away DDL/DML. dbt ships five (`table`, `view`, `incremental`, `ephemeral`, `materialized_view`) but three are core: **view** (default — `create view as` each run, freshest data, slow to query when heavy), **table** (`create table as`, fast to query, slow to build), and **incremental** (insert/update only new records, fast builds for event-style data). **Ephemeral** models build no warehouse object — dbt interpolates them as a **CTE** (`__dbt__cte__`) into dependents, so you can't select from them or `ref()` them in operations. The exam-critical **Golden Rule of Materializations**: *start with a **view**; when it's too slow to **query**, make it a **table**; when the table is too slow to **build**, make it **incremental**.* By layer: staging → views, intermediate → ephemeral, marts → table/incremental. Python models support only `table` and `incremental`. See [materializations](../sources/materializations.md), [materializations-1-guide-overview](../sources/materializations-1-guide-overview.md), [materializations-5-best-practices](../sources/materializations-5-best-practices.md).

**Modularity, DRY & the logical flow of models.** dbt's foundational philosophy (the **Viewpoint**) borrows software-engineering practice: version control, testing, documentation, and above all **modularity** — never copy-paste a definition; treat a dataset's schema as its public interface and reuse the same inputs. In practice this is realised by the staging → intermediate → marts layering, which moves data from **source-conformed** to **business-conformed** while applying each transformation **in only one place**. **Staging** models (`stg_<source>__<entity>`) are the atomic building blocks (kept as views); **intermediate** (`int_*`) models stack purposeful logic (often ephemeral); **marts** assemble wide business entities (tables/incremental). When porting legacy SQL you migrate it 1:1, swap raw table references for `{{ source() }}`, refactor into the 4-part CTE layout (Import CTEs → Logical CTEs → Final CTE → `select * from final`), split CTEs into modular staging/intermediate/final models, and audit old-vs-new with the `audit_helper` package. The recommended refactoring strategy is **alongside** (copy into `/marts` and edit the copy) rather than in-place. See [viewpoint](../sources/viewpoint.md), [how-we-structure-1-guide-overview](../sources/how-we-structure-1-guide-overview.md), [refactoring-legacy-sql](../sources/refactoring-legacy-sql.md).

**Node selection & clean DAGs.** dbt's selection syntax (`--select`/`-s`, `--exclude`, `--selector`) runs subsets of the DAG for `run`, `test`, `build`, `seed`, `snapshot`, `ls`, `compile`, etc. Selection resolves in the order: selection methods (`tag:`, `path:`, `config.materialized:table`, `source:`, `state:`…) → **graph operators** → set operators (space = union, comma = intersection, exclude). The graph operators are how you reason about a clean DAG: trailing **`+`** (`my_model+`) selects a node and **all descendants**, leading **`+`** (`+my_model`) selects a node and **all ancestors**, a number caps depth (`1+model`, `model+2`), **`@my_model`** adds the model, its children, *and the parents of those children*, and **`*`** is a wildcard. Use `dbt ls --select ...` to preview a selection before running it. See [syntax](../sources/syntax.md).

**Folder-level configuration in `dbt_proj
<!-- dbtwiki:auto:sources -->
## Source material

- [Add sources to your DAG](../raw/docs__docs__build__sources.md) · summary: [sources](../sources/sources.md) · [original](https://docs.getdbt.com/docs/build/sources) · `Doc`
- [Source configurations](../raw/docs__reference__source-configs.md) · summary: [source-configs](../sources/source-configs.md) · [original](https://docs.getdbt.com/reference/source-configs) · `Doc`
- [Source freshness](../raw/docs__docs__deploy__source-freshness.md) · summary: [source-freshness](../sources/source-freshness.md) · [original](https://docs.getdbt.com/docs/deploy/source-freshness) · `Doc`
- [Materializations](../raw/docs__docs__build__materializations.md) · summary: [materializations](../sources/materializations.md) · [original](https://docs.getdbt.com/docs/build/materializations) · `Doc`
- [Materialization best practices (guide)](../raw/docs__best-practices__materializations__1-guide-overview.md) · summary: [materializations-1-guide-overview](../sources/materializations-1-guide-overview.md) · [original](https://docs.getdbt.com/best-practices/materializations/1-guide-overview) · `Guide`
- [Best practices for materializations](../raw/docs__best-practices__materializations__5-best-practices.md) · summary: [materializations-5-best-practices](../sources/materializations-5-best-practices.md) · [original](https://docs.getdbt.com/best-practices/materializations/5-best-practices) · `Doc`
- [How we structure our dbt projects](../raw/docs__best-practices__how-we-structure__1-guide-overview.md) · summary: [how-we-structure-1-guide-overview](../sources/how-we-structure-1-guide-overview.md) · [original](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview) · `Doc`
- [Refactoring legacy SQL to dbt](../raw/docs__guides__refactoring-legacy-sql.md) · summary: [refactoring-legacy-sql](../sources/refactoring-legacy-sql.md) · [original](https://docs.getdbt.com/guides/refactoring-legacy-sql) · `Guide`
- [The dbt Viewpoint](../raw/docs__community__resources__viewpoint.md) · summary: [viewpoint](../sources/viewpoint.md) · [original](https://docs.getdbt.com/community/resources/viewpoint) · `Doc`
- [About dbt build command](../raw/docs__reference__commands__build.md) · summary: [build](../sources/build.md) · [original](https://docs.getdbt.com/reference/commands/build) · `Doc`
- [About dbt run command](../raw/docs__reference__commands__run.md) · summary: [run](../sources/run.md) · [original](https://docs.getdbt.com/reference/commands/run) · `Doc`
- [About dbt test command](../raw/docs__reference__commands__test.md) · summary: [test](../sources/test.md) · [original](https://docs.getdbt.com/reference/commands/test) · `Doc`
- [About dbt docs commands](../raw/docs__reference__commands__cmd-docs.md) · summary: [cmd-docs](../sources/cmd-docs.md) · [original](https://docs.getdbt.com/reference/commands/cmd-docs) · `Doc`
- [dbt Command reference](../raw/docs__reference__dbt-commands.md) · summary: [dbt-commands](../sources/dbt-commands.md) · [original](https://docs.getdbt.com/reference/dbt-commands) · `Doc`
- [About dbt snapshot command](../raw/docs__reference__commands__snapshot.md) · summary: [snapshot](../sources/snapshot.md) · [original](https://docs.getdbt.com/reference/commands/snapshot) · `Doc`
- [About dbt seed command](../raw/docs__reference__commands__seed.md) · summary: [seed](../sources/seed.md) · [original](https://docs.getdbt.com/reference/commands/seed) · `Doc`
- [Syntax overview](../raw/docs__reference__node-selection__syntax.md) · summary: [syntax](../sources/syntax.md) · [original](https://docs.getdbt.com/reference/node-selection/syntax) · `Doc`
- [dbt_project.yml reference](../raw/docs__reference__dbt_project.yml.md) · summary: [dbt_project.yml](../sources/dbt_project.yml.md) · [original](https://docs.getdbt.com/reference/dbt_project.yml) · `Doc`
- [Packages](../raw/docs__docs__build__packages.md) · summary: [packages](../sources/packages.md) · [original](https://docs.getdbt.com/docs/build/packages) · `Doc`
- [Python models](../raw/docs__docs__build__python-models.md) · summary: [python-models](../sources/python-models.md) · [original](https://docs.getdbt.com/docs/build/python-models) · `Doc`
- [grants (resource config)](../raw/docs__reference__resource-configs__grants.md) · summary: [grants](../sources/grants.md) · [original](https://docs.getdbt.com/reference/resource-configs/grants) · `Doc`
- [Add snapshots to your DAG](../raw/docs__docs__build__snapshots.md) · summary: [snapshots](../sources/snapshots.md) · [original](https://docs.getdbt.com/docs/build/snapshots) · `Doc`
- [About incremental strategy](../raw/docs__docs__build__incremental-strategy.md) · summary: [incremental-strategy](../sources/incremental-strategy.md) · [original](https://docs.getdbt.com/docs/build/incremental-strategy) · `Doc`
- [About incremental models](../raw/docs__docs__build__incremental-models-overview.md) · summary: [incremental-models-overview](../sources/incremental-models-overview.md) · [original](https://docs.getdbt.com/docs/build/incremental-models-overview) · `Doc`
- [About the `--empty` flag](../raw/docs__docs__build__empty-flag.md) · summary: [empty-flag](../sources/empty-flag.md) · [original](https://docs.getdbt.com/docs/build/empty-flag) · `Doc`
- [About the `--sample` flag](../raw/docs__docs__build__sample-flag.md) · summary: [sample-flag](../sources/sample-flag.md) · [original](https://docs.getdbt.com/docs/build/sample-flag) · `Doc`
- [About microbatch incremental models](../raw/docs__docs__build__incremental-microbatch.md) · summary: [incremental-microbatch](../sources/incremental-microbatch.md) · [original](https://docs.getdbt.com/docs/build/incremental-microbatch) · `Doc`
<!-- /dbtwiki:auto:sources -->
