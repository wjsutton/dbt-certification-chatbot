---
title: "Source summary — Model contracts"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "02 — Managing dbt models governance"
source: ../../raw/docs__docs__mesh__govern__model-contracts.md
source_url: https://docs.getdbt.com/docs/mesh/govern/model-contracts
---

# Model contracts — summary

**What it covers:** what a model contract is and how dbt enforces the *shape* (column names + data types) of a model before it builds.

## Key points

- A **contract** is a set of upfront "guarantees" about the shape of a model's returned dataset. dbt verifies the model produces a dataset matching its contract, or it **fails to build**.
- Enable enforcement with `enforced: true` under the `contract` config.
- When enforced, the contract **must** include every column's `name` and `data_type` (where `data_type` matches one your platform understands).
- If materialized as `table` or `incremental`, you may optionally add [`constraints`](constraints.md) such as `not_null`. (Not available on `view`/`ephemeral`.)
- Building a contracted model, dbt does two things differently:
  1. Runs a **"preflight" check** that the query returns columns with names + data types matching the YAML — **agnostic to column order**.
  2. Includes column names, data types, and constraints in the **DDL** it submits, and orders columns per the contract.
- Recommended for **"public" models** relied on downstream (other groups/teams/projects; reports/dashboards/exposures).

## Contracts vs tests

- A **contract** defines the **shape** of the dataset; if logic/input doesn't conform, the model **does not build** (build-time guarantee).
- **Data tests** validate the **content** *after* the model is built; more flexible/configurable (custom severity, `store_failures`), easier to debug.
- You can sometimes replace a data test with an equivalent **constraint** — prerequisites: platform supports/enforces it (most only enforce `not_null`), model is `table`/`incremental`, and a **full contract** (`name` + `data_type` for every column) is defined.

## Exam-relevant tokens

`contract`, `enforced: true`, `name`, `data_type`, `constraints`, `not_null`, preflight check, `table`/`incremental`, `on_schema_change`

## Gotchas

- You **must** define every column — contracts apply to **all** columns and require explicit expectations for all of them.
- A subtle type change (e.g. `boolean`→`integer`) can break downstream queries — contracts catch this.
- Breaking changes vs a previous project state surface a **contract error**; a backwards-incompatible change requires a major version bump.

Source: [Model contracts](https://docs.getdbt.com/docs/mesh/govern/model-contracts) · raw: `docs__docs__mesh__govern__model-contracts.md`
