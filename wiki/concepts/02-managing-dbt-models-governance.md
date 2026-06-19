---
title: "02 — Managing dbt models governance"
tags: [exam-domain, concept]
status: done
updated: 2026-06-12
---

# 02 — Managing dbt models governance

<!-- dbtwiki:auto:subtopics -->
## Sub-topics assessed

- **Adding contracts to ensure model shape** — [Model contracts](../sources/model-contracts.md) · [contract (resource config)](../sources/contract.md)
- **Creating model versions & deprecating old ones** — [Model versions](../sources/model-versions.md) · [versions (resource property)](../sources/versions.md)
- **Defining constraints in YAML for data integrity** — [constraints (resource property)](../sources/constraints.md)
- **Model governance overview** — [About model governance](../sources/about-model-governance.md)
- **Data product management (reading)** — [Data product management: Best practices](../sources/data-product-management.md)
<!-- /dbtwiki:auto:subtopics -->

## Synthesis

**Model governance** is dbt's umbrella for controlling who can access a model, what data it contains, how it changes over time, and how it's referenced across projects. The headline features — **model access** (`public`/`private`), **model contracts**, **model versions**, and **model namespaces** (groups/packages) — are all available in **dbt Core** and the dbt platform; only **project dependencies** (cross-project `ref` via the metadata service) is Enterprise-tier. The mental model is that a mature, shared model behaves like an **API**: access governs *who can `ref` it*, contracts govern *its shape*, and versions govern *how it changes*.

A **contract** is a set of upfront guarantees about a model's shape. Setting `contract: {enforced: true}` forces you to declare the `name` and `data_type` of **every** column; at build time dbt runs a **preflight check** that the query returns exactly those columns and types (order-agnostic), and bakes the names, types, and constraints into the **DDL** it submits. If the dataset doesn't match, the model **fails to build** — a *Compilation Error* shown before materialization (e.g. a `TEXT` vs `INT` mismatch). This differs from **data tests**, which validate **content after** the model is built. Watch the type-aliasing default (`string`→`text`, opt out with `alias_types: false`) and the `numeric` precision/scale trap (default scale 0 can fail enforcement — specify e.g. `numeric(38, 6)`). Contracted **incremental** 
<!-- dbtwiki:auto:sources -->
## Source material

- [Model contracts](../raw/docs__docs__mesh__govern__model-contracts.md) · summary: [model-contracts](../sources/model-contracts.md) · [original](https://docs.getdbt.com/docs/mesh/govern/model-contracts) · `Doc`
- [contract (resource config)](../raw/docs__reference__resource-configs__contract.md) · summary: [contract](../sources/contract.md) · [original](https://docs.getdbt.com/reference/resource-configs/contract) · `Doc`
- [Model versions](../raw/docs__docs__mesh__govern__model-versions.md) · summary: [model-versions](../sources/model-versions.md) · [original](https://docs.getdbt.com/docs/mesh/govern/model-versions) · `Doc`
- [versions (resource property)](../raw/docs__reference__resource-properties__versions.md) · summary: [versions](../sources/versions.md) · [original](https://docs.getdbt.com/reference/resource-properties/versions) · `Doc`
- [constraints (resource property)](../raw/docs__reference__resource-properties__constraints.md) · summary: [constraints](../sources/constraints.md) · [original](https://docs.getdbt.com/reference/resource-properties/constraints) · `Doc`
- [About model governance](../raw/docs__docs__mesh__govern__about-model-governance.md) · summary: [about-model-governance](../sources/about-model-governance.md) · [original](https://docs.getdbt.com/docs/mesh/govern/about-model-governance) · `Doc`
- [Data product management: Best practices](../raw/getdbt__blog__data-product-management.md) · summary: [data-product-management](../sources/data-product-management.md) · [original](https://www.getdbt.com/blog/data-product-management) · `Blog`
<!-- /dbtwiki:auto:sources -->
