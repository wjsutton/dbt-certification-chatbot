---
title: "Source summary — Source freshness"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "06 — External dependencies"
source: ../../raw/docs__docs__deploy__source-freshness.md
source_url: https://docs.getdbt.com/docs/deploy/source-freshness
---

# Source freshness — summary

**What it covers:** The interface and job patterns for snapshotting source data freshness against an SLA, and how freshness fits into deploy jobs.

## Key points
- dbt provides an interface around source data freshness calculations; when a job snapshots freshness, dbt renders a UI showing the most recent snapshot state — used to judge whether sources meet your SLA.
- **`dbt build` does _not_ include source freshness checks.** You must run freshness separately.
- Job patterns: add `dbt build` for models/tests; optionally enable **Generate docs on run**; optionally enable the **Run source freshness** checkbox to run freshness as the **first** step.
- **Run source freshness checkbox:** runs `dbt source freshness` as the first step and **won't break subsequent steps if it fails**. A freshness-only job still needs at least one placeholder step such as `dbt compile`.
- **Add as a run step:** if source data is out of date, the step **"fails" and subsequent steps will not run**; dbt triggers email notifications based on the step's end state. Run it first if you don't want models to run on stale data, otherwise run it last or in a separate job.
- **Snapshot frequency:** run freshness jobs at least **double the frequency of your lowest SLA** (e.g. 1 hour SLA → snapshot every 30 mins; 1 day → 12 hours; 1 week → about daily).
- Source freshness for Snowflake is calculated using the `LAST_ALTERED` column.

## Exam-relevant tokens
`dbt source freshness`, `dbt build` (excludes freshness), `dbt compile` (placeholder step), Run source freshness checkbox, SLA, `LAST_ALTERED`

## Gotchas
- A common exam trap: **`dbt build` does not run source freshness** — you need `dbt source freshness` explicitly.
- Checkbox vs run-step differ: the checkbox won't break later steps on failure; a freshness command added as a run step **will** stop the job if sources are stale.
- A freshness-only job still requires a placeholder step (e.g. `dbt compile`).

Source: [Source freshness](https://docs.getdbt.com/docs/deploy/source-freshness) · raw: `docs__docs__deploy__source-freshness.md`
