---
title: "Source summary — About the --sample flag"
tags: [source-summary, development, sampling]
status: done
updated: 2026-06-11
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__docs__build__sample-flag.md
source_url: https://docs.getdbt.com/docs/build/sample-flag
---

# The `--sample` flag — summary

**What it covers:** running dbt in *sample mode* to cut build time and warehouse spend by building models on a time-filtered slice of input data.

## Key points

- `--sample` is available on the **`run`** and **`build`** commands.
- It builds models against a **time-based sample** of refs and sources — a step beyond `--empty` (which builds zero rows): `--sample` includes *some* real data so you can validate outputs, not just dependencies.
- Sampling is **time-based**, so every sampled `ref`/source must have an **`event_time`** config set to the timestamp column.
- Two spec forms:
  - **Relative:** `--sample="3 days"` (granularities: hours, days, months, years).
  - **Static:** `--sample="{'start': '2024-07-01', 'end': '2024-07-08 18:00:00'}"`.
- Opt a specific ref **out** of sampling with `.render()`: `{{ ref('stg_customers').render() }}`.
- Not available for **Python models** (ignored); seeds build normally but are sampled when referenced downstream.

## `--empty` vs `--sample` (exam contrast)

- `--empty` → **zero rows**; validates refs/sources and that models build (schema-only dry run).
- `--sample` → **a time slice of rows**; validates outputs with real-but-small data. Not all joins will necessarily populate.

## Exam-relevant tokens

`--sample`, `--empty`, `event_time`, `.render()`, relative vs static time spec, `run`/`build` only.

Source: [About the --sample flag](https://docs.getdbt.com/docs/build/sample-flag) · raw: [`sample-flag.md`](../../raw/docs__docs__build__sample-flag.md)
