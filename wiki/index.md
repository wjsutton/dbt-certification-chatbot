---
title: "Index"
tags: [index]
updated: 2026-06-29
---


# Index

Catalog of the wiki. Read this first when answering a query.

## Start here
- [Overview](overview.md)
- [Change log](log.md)

## Contents (by exam domain, sub-topic & source)

### [01 — Developing & optimizing dbt models](concepts/01-developing-and-optimizing-dbt-models.md)

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

### [02 — Managing dbt models governance](concepts/02-managing-dbt-models-governance.md)

- **Adding contracts to ensure model shape** — [Model contracts](../sources/model-contracts.md) · [contract (resource config)](../sources/contract.md)
- **Creating model versions & deprecating old ones** — [Model versions](../sources/model-versions.md) · [versions (resource property)](../sources/versions.md)
- **Defining constraints in YAML for data integrity** — [constraints (resource property)](../sources/constraints.md)
- **Model governance overview** — [About model governance](../sources/about-model-governance.md)
- **Data product management (reading)** — [Data product management: Best practices](../sources/data-product-management.md)

### [03 — Debugging data modeling errors](concepts/03-debugging-data-modeling-errors.md)

- **Understanding logged error messages** — [Debug errors](../sources/debug-errors.md)
- **Troubleshooting using compiled code** — [About dbt compile command](../sources/compile.md)
- **Troubleshooting .yml compilation errors** — [Debug errors](../sources/debug-errors.md)
- **Developing, implementing & testing a fix before merge** — [Best practices for workflows](../sources/best-practice-workflows.md)
- **Managing dbt behavior with flags** — [About flags (global configs)](../sources/about-global-configs.md) · [Behavior changes](../sources/behavior-changes.md)

### [04 — Troubleshooting & optimizing pipelines](concepts/04-troubleshooting-and-optimizing-pipelines.md)

- **Troubleshooting & managing failure points in the DAG** — [Syntax overview](../sources/syntax.md) · [About dbt retry command](../sources/retry.md)
- **Using dbt clone** — [About dbt clone command](../sources/clone.md) · [Clone incremental models as the first step of your CI job](../sources/clone-incremental-models.md) · [To defer or to clone, that is the question](../sources/to-defer-or-to-clone.md)

### [05 — Implementing dbt tests](concepts/05-implementing-dbt-tests.md)

- **Generic, singular, custom, custom generic & unit tests** — [Add data tests to your DAG](../sources/data-tests.md) · [Unit tests](../sources/unit-tests.md) · [Writing custom generic data tests](../sources/writing-custom-generic-tests.md) · [Data test configurations](../sources/data-test-configs.md)
- **Testing assumptions for models and sources** — [Add data tests to your DAG](../sources/data-tests.md)
- **Implementing testing steps in the workflow** — [Test smarter not harder: add the right tests](../sources/test-smarter-not-harder.md) · [Test smarter: Where should tests go in your pipeline?](../sources/test-smarter-where-tests-should-go.md)

### [06 — External dependencies](concepts/06-external-dependencies.md)

- **Implementing dbt exposures** — [Add Exposures to your DAG](../sources/exposures.md) · [Exposure properties](../sources/exposure-properties.md)
- **Implementing source freshness** — [Source freshness](../sources/source-freshness.md) · [About dbt source command](../sources/source.md) · [freshness (resource property)](../sources/freshness.md)

### [07 — Leveraging the dbt state](concepts/07-leveraging-the-dbt-state.md)

- **Understanding state & state selection** — [About local state in dbt](../sources/state-selection.md) · [Node selector methods](../sources/methods.md) · [Defer](../sources/defer.md)
- **Using dbt retry** — [About dbt retry command](../sources/retry.md)

## Source summaries (ingested)

- [Source summary — About flags (global configs)](sources/about-global-configs.md) — `done`
- [Source summary — About model governance](sources/about-model-governance.md) — `done`
- [Source summary — Behavior changes](sources/behavior-changes.md) — `done`
- [Source summary — Best practices for workflows](sources/best-practice-workflows.md) — `done`
- [Source summary — About dbt build command](sources/build.md) — `done`
- [Source summary — Clone incremental models as the first step of your CI job](sources/clone-incremental-models.md) — `done`
- [Source summary — About dbt clone command](sources/clone.md) — `done`
- [Source summary — About dbt docs commands](sources/cmd-docs.md) — `done`
- [Source summary — About dbt compile command](sources/compile.md) — `done`
- [Source summary — constraints (resource property)](sources/constraints.md) — `done`
- [Source summary — contract (resource config)](sources/contract.md) — `done`
- [Source summary — Data product management: Best practices](sources/data-product-management.md) — `done`
- [Source summary — Data test configurations](sources/data-test-configs.md) — `done`
- [Source summary — Add data tests to your DAG](sources/data-tests.md) — `done`
- [Source summary — dbt Command reference](sources/dbt-commands.md) — `done`
- [Source summary — dbt_project.yml reference](sources/dbt_project.yml.md) — `done`
- [Source summary — Debug errors](sources/debug-errors.md) — `done`
- [Source summary — Defer](sources/defer.md) — `done`
- [Source summary — About the --empty flag](sources/empty-flag.md) — `done`
- [Source summary — Exposure properties](sources/exposure-properties.md) — `done`
- [Source summary — Add Exposures to your DAG](sources/exposures.md) — `done`
- [Source summary — freshness (resource property)](sources/freshness.md) — `done`
- [Source summary — grants config](sources/grants.md) — `done`
- [Source summary — How we structure our dbt projects](sources/how-we-structure-1-guide-overview.md) — `done`
- [Source summary — About microbatch incremental models](sources/incremental-microbatch.md) — `done`
- [Source summary — About incremental models](sources/incremental-models-overview.md) — `done`
- [Source summary — About incremental strategy](sources/incremental-strategy.md) — `done`
- [Source summary — Materializations best practices](sources/materializations-1-guide-overview.md) — `done`
- [Source summary — Best practices for materializations](sources/materializations-5-best-practices.md) — `done`
- [Source summary — Materializations](sources/materializations.md) — `done`
- [Source summary — Node selector methods](sources/methods.md) — `done`
- [Source summary — Model contracts](sources/model-contracts.md) — `done`
- [Source summary — Model versions](sources/model-versions.md) — `done`
- [Source summary — Packages](sources/packages.md) — `done`
- [Source summary — Python models](sources/python-models.md) — `done`
- [Source summary — Refactoring legacy SQL to dbt](sources/refactoring-legacy-sql.md) — `done`
- [Source summary — About dbt retry command](sources/retry.md) — `done`
- [Source summary — About dbt run command](sources/run.md) — `done`
- [Source summary — About the --sample flag](sources/sample-flag.md) — `done`
- [Source summary — About dbt seed command](sources/seed.md) — `done`
- [Source summary — About dbt snapshot command](sources/snapshot.md) — `done`
- [Source summary — Add snapshots to your DAG](sources/snapshots.md) — `done`
- [Source summary — Source configurations](sources/source-configs.md) — `done`
- [Source summary — Source freshness](sources/source-freshness.md) — `done`
- [Source summary — About dbt source command](sources/source.md) — `done`
- [Source summary — Add sources to your DAG](sources/sources.md) — `done`
- [Source summary — About local state in dbt](sources/state-selection.md) — `done`
- [Source summary — Node selection syntax overview](sources/syntax.md) — `done`
- [Source summary — Test smarter not harder: add the right tests to your dbt project](sources/test-smarter-not-harder.md) — `done`
- [Source summary — Test smarter not harder: Where should tests go in your pipeline?](sources/test-smarter-where-tests-should-go.md) — `done`
- [Source summary — About dbt test command](sources/test.md) — `done`
- [Source summary — To defer or to clone, that is the question](sources/to-defer-or-to-clone.md) — `done`
- [Source summary — Unit tests](sources/unit-tests.md) — `done`
- [Source summary — versions (resource property)](sources/versions.md) — `done`
- [Source summary — The dbt Viewpoint](sources/viewpoint.md) — `done`
- [Source summary — Writing custom generic data tests](sources/writing-custom-generic-tests.md) — `done`

## Raw sources (56)

- [Best practices for workflows](../raw/docs__best-practices__best-practice-workflows.md) · `Doc` · [source](https://docs.getdbt.com/best-practices/best-practice-workflows)
- [Clone incremental models as the first step of your CI job](../raw/docs__best-practices__clone-incremental-models.md) · `Doc` · [source](https://docs.getdbt.com/best-practices/clone-incremental-models)
- [How we structure our dbt projects](../raw/docs__best-practices__how-we-structure__1-guide-overview.md) · `Doc` · [source](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)
- [Materialization best practices (guide)](../raw/docs__best-practices__materializations__1-guide-overview.md) · `Guide` · [source](https://docs.getdbt.com/best-practices/materializations/1-guide-overview)
- [Best practices for materializations](../raw/docs__best-practices__materializations__5-best-practices.md) · `Doc` · [source](https://docs.getdbt.com/best-practices/materializations/5-best-practices)
- [Writing custom generic data tests](../raw/docs__best-practices__writing-custom-generic-tests.md) · `Guide` · [source](https://docs.getdbt.com/best-practices/writing-custom-generic-tests)
- [Test smarter not harder: add the right tests](../raw/docs__blog__test-smarter-not-harder.md) · `Blog` · [source](https://docs.getdbt.com/blog/test-smarter-not-harder)
- [Test smarter: Where should tests go in your pipeline?](../raw/docs__blog__test-smarter-where-tests-should-go.md) · `Blog` · [source](https://docs.getdbt.com/blog/test-smarter-where-tests-should-go)
- [To defer or to clone, that is the question](../raw/docs__blog__to-defer-or-to-clone.md) · `Blog` · [source](https://docs.getdbt.com/blog/to-defer-or-to-clone)
- [The dbt Viewpoint](../raw/docs__community__resources__viewpoint.md) · `Doc` · [source](https://docs.getdbt.com/community/resources/viewpoint)
- [Add data tests to your DAG](../raw/docs__docs__build__data-tests.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/data-tests)
- [About the `--empty` flag](../raw/docs__docs__build__empty-flag.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/empty-flag)
- [Add Exposures to your DAG](../raw/docs__docs__build__exposures.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/exposures)
- [About microbatch incremental models](../raw/docs__docs__build__incremental-microbatch.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/incremental-microbatch)
- [About incremental models](../raw/docs__docs__build__incremental-models-overview.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/incremental-models-overview)
- [About incremental strategy](../raw/docs__docs__build__incremental-strategy.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/incremental-strategy)
- [Materializations](../raw/docs__docs__build__materializations.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/materializations)
- [Packages](../raw/docs__docs__build__packages.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/packages)
- [Python models](../raw/docs__docs__build__python-models.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/python-models)
- [About the `--sample` flag](../raw/docs__docs__build__sample-flag.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/sample-flag)
- [Add snapshots to your DAG](../raw/docs__docs__build__snapshots.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/snapshots)
- [Add sources to your DAG](../raw/docs__docs__build__sources.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/sources)
- [Unit tests](../raw/docs__docs__build__unit-tests.md) · `Doc` · [source](https://docs.getdbt.com/docs/build/unit-tests)
- [Source freshness](../raw/docs__docs__deploy__source-freshness.md) · `Doc` · [source](https://docs.getdbt.com/docs/deploy/source-freshness)
- [About model governance](../raw/docs__docs__mesh__govern__about-model-governance.md) · `Doc` · [source](https://docs.getdbt.com/docs/mesh/govern/about-model-governance)
- [Model contracts](../raw/docs__docs__mesh__govern__model-contracts.md) · `Doc` · [source](https://docs.getdbt.com/docs/mesh/govern/model-contracts)
- [Model versions](../raw/docs__docs__mesh__govern__model-versions.md) · `Doc` · [source](https://docs.getdbt.com/docs/mesh/govern/model-versions)
- [Debug errors](../raw/docs__guides__debug-errors.md) · `Guide` · [source](https://docs.getdbt.com/guides/debug-errors)
- [Refactoring legacy SQL to dbt](../raw/docs__guides__refactoring-legacy-sql.md) · `Guide` · [source](https://docs.getdbt.com/guides/refactoring-legacy-sql)
- [About dbt build command](../raw/docs__reference__commands__build.md) · `Doc` · [source](https://docs.getdbt.com/reference/commands/build)
- [About dbt clone command](../raw/docs__reference__commands__clone.md) · `Doc` · [source](https://docs.getdbt.com/reference/commands/clone)
- [About dbt docs commands](../raw/docs__reference__commands__cmd-docs.md) · `Doc` · [source](https://docs.getdbt.com/reference/commands/cmd-docs)
- [About dbt compile command](../raw/docs__reference__commands__compile.md) · `Doc` · [source](https://docs.getdbt.com/reference/commands/compile)
- [About dbt retry command](../raw/docs__reference__commands__retry.md) · `Doc` · [source](https://docs.getdbt.com/reference/commands/retry)
- [About dbt run command](../raw/docs__reference__commands__run.md) · `Doc` · [source](https://docs.getdbt.com/reference/commands/run)
- [About dbt seed command](../raw/docs__reference__commands__seed.md) · `Doc` · [source](https://docs.getdbt.com/reference/commands/seed)
- [About dbt snapshot command](../raw/docs__reference__commands__snapshot.md) · `Doc` · [source](https://docs.getdbt.com/reference/commands/snapshot)
- [About dbt source command](../raw/docs__reference__commands__source.md) · `Doc` · [source](https://docs.getdbt.com/reference/commands/source)
- [About dbt test command](../raw/docs__reference__commands__test.md) · `Doc` · [source](https://docs.getdbt.com/reference/commands/test)
- [Data test configurations](../raw/docs__reference__data-test-configs.md) · `Doc` · [source](https://docs.getdbt.com/reference/data-test-configs)
- [dbt Command reference](../raw/docs__reference__dbt-commands.md) · `Doc` · [source](https://docs.getdbt.com/reference/dbt-commands)
- [dbt_project.yml reference](../raw/docs__reference__dbt_project.yml.md) · `Doc` · [source](https://docs.getdbt.com/reference/dbt_project.yml)
- [Exposure properties](../raw/docs__reference__exposure-properties.md) · `Doc` · [source](https://docs.getdbt.com/reference/exposure-properties)
- [About flags (global configs)](../raw/docs__reference__global-configs__about-global-configs.md) · `Doc` · [source](https://docs.getdbt.com/reference/global-configs/about-global-configs)
- [Behavior changes](../raw/docs__reference__global-configs__behavior-changes.md) · `Doc` · [source](https://docs.getdbt.com/reference/global-configs/behavior-changes)
- [Defer](../raw/docs__reference__node-selection__defer.md) · `Doc` · [source](https://docs.getdbt.com/reference/node-selection/defer)
- [Node selector methods](../raw/docs__reference__node-selection__methods.md) · `Doc` · [source](https://docs.getdbt.com/reference/node-selection/methods)
- [About local state in dbt](../raw/docs__reference__node-selection__state-selection.md) · `Doc` · [source](https://docs.getdbt.com/reference/node-selection/state-selection)
- [Syntax overview](../raw/docs__reference__node-selection__syntax.md) · `Doc` · [source](https://docs.getdbt.com/reference/node-selection/syntax)
- [contract (resource config)](../raw/docs__reference__resource-configs__contract.md) · `Doc` · [source](https://docs.getdbt.com/reference/resource-configs/contract)
- [grants (resource config)](../raw/docs__reference__resource-configs__grants.md) · `Doc` · [source](https://docs.getdbt.com/reference/resource-configs/grants)
- [constraints (resource property)](../raw/docs__reference__resource-properties__constraints.md) · `Doc` · [source](https://docs.getdbt.com/reference/resource-properties/constraints)
- [freshness (resource property)](../raw/docs__reference__resource-properties__freshness.md) · `Doc` · [source](https://docs.getdbt.com/reference/resource-properties/freshness)
- [versions (resource property)](../raw/docs__reference__resource-properties__versions.md) · `Doc` · [source](https://docs.getdbt.com/reference/resource-properties/versions)
- [Source configurations](../raw/docs__reference__source-configs.md) · `Doc` · [source](https://docs.getdbt.com/reference/source-configs)
- [Data product management: Best practices](../raw/getdbt__blog__data-product-management.md) · `Blog` · [source](https://www.getdbt.com/blog/data-product-management)
