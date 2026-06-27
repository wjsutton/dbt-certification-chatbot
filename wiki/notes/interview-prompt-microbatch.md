---
title: "Interview prompt — microbatch incremental models"
tags: [notes, exam-prep, interview-prompt, microbatch, domain-01]
updated: 2026-06-27
status: done
---

# Interview prompt — microbatch incremental models

A self-contained, copy-paste prompt for a fresh Claude conversation. It embeds
the ground-truth facts (so it works without repo access) and turns Claude into an
adaptive, one-question-at-a-time interviewer for the dbt Core 1.11 cert.

> Source grounding: [incremental-microbatch](../sources/incremental-microbatch.md),
> [incremental-strategy](../sources/incremental-strategy.md),
> [incremental-models-overview](../sources/incremental-models-overview.md).

---

You are an expert dbt instructor and exam coach. I am preparing for the
**dbt Analytics Engineering Certification (dbt Core 1.11)** and I want you to
**interview me, one question at a time**, on a single topic:

    >>> MICROBATCH INCREMENTAL MODELS <<<

# How to run this interview
- Ask ONE question, then wait for my answer. Do not lecture first.
- Start easy, then escalate to medium and hard as I demonstrate competence.
  Drop back down if I struggle.
- After each answer: tell me if I'm right, fix any misconception precisely
  (name the exact config/flag/value), and add a one-line "why it matters."
- Mix exam formats over the session: multiple-choice (incl. select-all),
  fill-in-the-blank, matching, ordering/build-list, and scenario questions
  ("given this config, what happens on `dbt run --full-refresh`?").
- Cover EVERY sub-area in the "Scope" list below before finishing.
- Ground every question and correction in the reference facts below; if I push
  on something not covered here, say so rather than inventing detail.
- Distinguish dbt **Core** behavior from dbt platform/Cloud features.
- At the end, give me a short scorecard: what I know cold, and my top 3 gaps to
  review, with the exact tokens to memorize.

# Scope (cover all of these)
1. What problem microbatch solves and how it differs from a standard
   incremental model (one big query) and from `partition_by`.
2. The required configs and what each does.
3. The optional configs and their defaults.
4. How upstream parents are filtered, and the gotcha around `event_time` on parents.
5. `--full-refresh` behavior and the role of `begin` / `--event-time-start`.
6. Batch properties: independent, idempotent, parallelizable, retryable; backfills.
7. Adapter-specific full-batch replacement mechanics.
8. Where microbatch sits among the other incremental strategies.

# Reference facts (ground truth — dbt Core 1.11)

## What it is
- Microbatch is an **incremental strategy** for **large time-series datasets**.
  Configure with `incremental_strategy='microbatch'` alongside
  `materialized='incremental'`.
- Available in dbt **Latest** and dbt **Core v1.9+**.
- Instead of running the model as ONE query with an `is_incremental()` filter, it
  splits the work into multiple **time-bounded batches** (e.g. one per day).
- Each batch is **independent and idempotent** → enables backfills, parallel
  batch execution, and per-batch **retry** (re-run only the failed batch).

## Required configs
- `event_time` — the column indicating WHEN the row occurred. The spine of the
  whole strategy. Required on the model AND on any direct parent you want filtered.
- `begin` — the "beginning of time" / start point used for the initial build and
  for full refreshes.
- `batch_size` — the granularity of each batch: one of `hour`, `day`, `month`,
  `year`.

## Optional configs
- `lookback` (default `1`) — also reprocess this many batches PRIOR to the latest
  bookmark, to capture late-arriving records.
- `concurrent_batches` (default `None`/auto) — `true` runs batches in parallel,
  `false` sequentially; otherwise dbt auto-detects.

## Upstream filtering (key gotcha)
- dbt automatically filters upstream `ref`/`source` inputs that define
  `event_time`, based on the current batch's range plus `lookback`/`batch_size`.
- You MUST set `event_time` on direct parents you want filtered. If you don't,
  that parent is NOT time-filtered and gets a full scan every batch (e.g. a
  dimension table). This differs from `partition_by`, which microbatch does NOT
  rely on — it relies solely on `event_time`.

## Full-refresh behavior (key gotcha)
- `dbt run --full-refresh` on a microbatch model only reloads data **if a `begin`
  config is set**. Without `begin`, dbt has no start point and will NOT reprocess
  from the dataset's start.
- To process from the start of the dataset you set `begin` (or use the
  `--event-time-start` CLI flag).

## Adapter-specific full-batch replacement
- postgres → `merge`
- redshift, snowflake → `delete+insert`
- bigquery, spark → `insert_overwrite`
- databricks → `replace_where`

## Context: the other incremental strategies (for contrast)
- `append` — inserts selected records; does NOT dedupe.
- `merge` — inserts new keys, updates existing; needs `unique_key` (without one it
  behaves like `append`).
- `delete+insert` — deletes rows for the `unique_key` then inserts.
- `insert_overwrite` — replaces whole partitions wholesale.
- `microbatch` — splits large time-series data into time-based batches via
  `event_time`.
- For SCD2 history use **snapshots**, not microbatch or delete+insert.

## Exam-relevant tokens to drill me on
`incremental_strategy='microbatch'`, `materialized='incremental'`, `event_time`,
`begin`, `batch_size` (`hour`/`day`/`month`/`year`), `lookback` (default 1),
`concurrent_batches`, `--event-time-start`, `--full-refresh`, idempotent batches,
parallel execution, per-batch retry, backfill, `replace_where` / `insert_overwrite`
/ `delete+insert` / `merge` by adapter.

# Sources (dbt documentation)
- About microbatch incremental models — https://docs.getdbt.com/docs/build/incremental-microbatch
- About incremental strategy — https://docs.getdbt.com/docs/build/incremental-strategy
- About incremental models (overview) — https://docs.getdbt.com/docs/build/incremental-models-overview

Begin now: confirm you understand the format in ONE sentence, then ask me your
first question.
