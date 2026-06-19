---
title: "Source summary — About model governance"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "02 — Managing dbt models governance"
source: ../../raw/docs__docs__mesh__govern__about-model-governance.md
source_url: https://docs.getdbt.com/docs/mesh/govern/about-model-governance
---

# About model governance — summary

**What it covers:** the umbrella of dbt model governance features and which are available in dbt Core vs the dbt platform.

## Key points

- Model governance controls **who can access** models, **what data** they contain, **how they change** over time, and how they're **referenced across projects**.
- Available in **both dbt Core and the dbt platform**, with some feature differences across plans.
- The governance features:
  - **Model access** — mark models `public` or `private` to distinguish mature data products from implementation details and control who can `ref` them.
  - **Model contracts** — guarantee a model's shape (column names, data types, constraints) **before it builds**.
  - **Model versions** — provide a smoother upgrade pathway and deprecation window when a breaking change is unavoidable.
  - **Model namespaces** — organize models into **groups** and **packages** to delineate ownership; models in different packages can share a name and `ref` can take a project/package namespace as its first argument.
  - **Project dependencies** — "cross-project ref" to public models in other projects via an always-on stateful **metadata service**.
- **All features are in dbt Core and the platform EXCEPT project dependencies**, which is **dbt Enterprise-tier only** (uses the metadata service + catalog, powering an enterprise data mesh).

## Exam-relevant tokens

`model access` (`public`/`private`), `model contracts`, `model versions`, `model namespaces` (groups/packages), `project dependencies` (cross-project ref), `ref`

## Gotchas

- Cross-project `ref` / project dependencies is the one governance feature **not** in dbt Core — it's Enterprise-tier only.
- Model access (`public`/`private`) governs *who can `ref`*; contracts govern *shape*; versions govern *change over time* — keep these distinct.

Source: [About model governance](https://docs.getdbt.com/docs/mesh/govern/about-model-governance) · raw: `docs__docs__mesh__govern__about-model-governance.md`
