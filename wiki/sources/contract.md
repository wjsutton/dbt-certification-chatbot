---
title: "Source summary — contract (resource config)"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "02 — Managing dbt models governance"
source: ../../raw/docs__reference__resource-configs__contract.md
source_url: https://docs.getdbt.com/reference/resource-configs/contract
---

# contract (resource config) — summary

**What it covers:** the `contract` config reference — enforcement behavior, type aliasing, precision/scale, where to set it, and incremental rules.

## Key points

- When `contract` is enforced, dbt ensures the returned dataset **exactly matches** the YAML: `name` and `data_type` for every column, plus any supported `constraints`.
- Even subtle type changes (e.g. `boolean` → `integer`) could break downstream queries.
- **Data type aliasing:** dbt applies built-in aliasing for `data_type` (e.g. `string` → `text` on Postgres/Redshift). Opt out with `alias_types: false` (default `true`). Unknown types pass through as-is.
- **Size/precision/scale:** dbt does **not** compare size/precision/scale (e.g. `varchar(256)` vs `varchar(257)`). But specify scale for `numeric` — a default `numeric` is precision 38, scale 0 (whole numbers only), which can fail enforcement. Use e.g. `numeric(38, 6)`. Core 1.7+ warns if precision/scale omitted.
- Where to set: `dbt_project.yml` (`+contract: {enforced: true}` across many models), `properties.yml` (`config: contract: enforced: true`), or in-model `{{ config(contract = {"enforced": true}) }}`.
- **Preflight failure** is a *Compilation Error* shown **before** materialization, with a column / definition_type / contract_type / mismatch_reason table.

## Incremental models and `on_schema_change`

- Contracted **incremental** models must set `on_schema_change` to `append_new_columns` or `fail`.
- **Not** `sync_all_columns`: it removes deleted columns, and removing existing columns is a **breaking change** for contracted models.
- With `ignore` (or unset), a new YAML/SQL column isn't added to the existing table, creating a drift between the contract and the real table.

## Exam-relevant tokens

`enforced: true`, `alias_types: false`, `numeric(38, 6)`, `data_type`, `on_schema_change`, `append_new_columns`, `fail`, `sync_all_columns`, `+contract`

## Gotchas

- Aliasing is on by default — `string` may materialize as `text`.
- Default `numeric` scale of 0 can silently fail a contract; always specify nonzero scale.
- Additive changes (adding a column, adding constraints) are **not** breaking.

Source: [contract (resource config)](https://docs.getdbt.com/reference/resource-configs/contract) · raw: `docs__reference__resource-configs__contract.md`
