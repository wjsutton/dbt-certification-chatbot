---
title: "Cram sheet — missed tokens (dbt Core 1.11)"
tags: [notes, exam-prep, cram-sheet]
updated: 2026-06-27
status: done
---

# Cram sheet — the tokens I keep missing

One-page review built from five practice rounds. These are the *exact-name* items
that tripped me up — concepts were solid, recall of specific tokens was the leak.
Read top to bottom Monday morning. Each section links the doc to skim if it's
still fuzzy.

---

## 1. Microbatch incremental models
→ https://docs.getdbt.com/docs/build/incremental-microbatch

- **Required trio:** `event_time` · `begin` · `batch_size` (NOT `unique_key`).
- `batch_size` values: `hour` / `day` / `month` / `year`.
- `lookback` default = **1 batch** (reprocesses prior batches for late data).
- `--full-refresh` does **nothing** unless **`begin`** is set (or use `--event-time-start`).
- Set `event_time` on **direct parents** too, or they get a full scan each batch.

## 2. Dry-run flags: `--empty` vs `--sample`
→ https://docs.getdbt.com/docs/build/empty-flag · https://docs.getdbt.com/docs/build/sample-flag

- `--empty` = **0 rows**, still executes SQL. Works on **`run`/`build`/`snapshot`/`compile`**.
- `--sample` = real **time-based slice**; needs **`event_time`**; **`run`/`build` only**.
- Opt a ref OUT of sampling with **`.render()`** → `{{ ref('x').render() }}`.
- Both are **ignored for Python models**.

## 3. Behavior-change flags
→ https://docs.getdbt.com/reference/global-configs/behavior-changes

- Three phases (in order): **Introduction → Maturity → Removal**.
- In **Maturity** the new behavior is **ON** by default (opt out with `false`).
- A new **warning** is NOT a behavior change; a new **error** IS.
- Set **only** in the `flags:` dict in `dbt_project.yml` (not CLI/env).
- Introduced in **1.11.0**: `require_unique_project_resource_names`,
  `require_ref_searches_node_package_before_root`.
- `validate_macro_args` was introduced in **1.10** (not 1.11).

## 4. Global configs / env vars
→ https://docs.getdbt.com/reference/global-configs/about-global-configs

- Env-var prefix: **`DBT_`** (≤1.10) → **`DBT_ENGINE_`** (1.11+).
- Three places to set flags: `dbt_project.yml` (`flags:`), env vars, CLI.

## 5. Snapshots (v1.9 rework)
→ https://docs.getdbt.com/docs/build/snapshots

- Two **strategies**: **`timestamp`** (needs **`updated_at`**) · **`check`** (needs **`check_cols`**).
- `hard_deletes` **replaces** the old `invalidate_hard_deletes`.
- `target_schema` became **optional** in v1.9.
- Defined in **YAML** now (not legacy Jinja `{% snapshot %}` blocks).

## 6. Contracts & versions (governance)
→ https://docs.getdbt.com/reference/resource-configs/contract · https://docs.getdbt.com/docs/mesh/govern/model-versions

- Turn contract on: **`contract: { enforced: true }`** (NOT "enabled").
- Contracted **incremental** `on_schema_change` must be **`append_new_columns`** or **`fail`**
  (never `sync_all_columns` — dropping a column is breaking).
- Adding a column = **non-breaking**; removing/renaming/retyping = breaking → new version.
- Versions YAML: **`versions:`** key; canonical = **`latest_version:`** sub-key.
- Pin a version: **`ref('model', v=2)`**; no pin → resolves to **latest**.

## 7. State, defer & clone
→ https://docs.getdbt.com/reference/node-selection/state-selection · https://docs.getdbt.com/reference/node-selection/defer · https://docs.getdbt.com/reference/commands/clone

- `--state` unlocks three things: **`state:` selector**, **`--defer`**, **`dbt clone`**.
- `--defer` needs **`--state`** too; **`--favor-state`** prefers the state node over a local one.
- **Ephemeral models are never deferred.**
- `dbt clone` → recreate existing relations with **`--full-refresh`**; falls back to a
  **pointer view** when zero-copy cloning isn't available.
- `state:modified` **includes** `state:new` (modified = new + changed).

## 8. Node selection & retry
→ https://docs.getdbt.com/reference/node-selection/methods · https://docs.getdbt.com/reference/commands/retry

- Select by prior-run outcome: **`result:`** (`result:error`, `result:fail`).
- Graph operator: **`+model`** = parents, **`model+`** = children.
- `dbt retry` reads **`run_results.json`**; resumes from point of failure.
- On a previously **successful** run, retry is a **no-op** ("Nothing to do").
- Retry **inherits** the original `--select` — you can't override it.

## 9. Exposures
→ https://docs.getdbt.com/docs/build/exposures

- **Required:** `name` · `type` · `owner` (`depends_on` is only "expected").
- `type` values: **`dashboard` / `notebook` / `analysis` / `ml` / `application`**
  (NOT BI-tool brand names).
- `owner` needs at least **one of** `name` **or** `email`.
- Select with `+exposure:<name>` to pull in upstream parents.

## 10. Grants
→ https://docs.getdbt.com/reference/resource-configs/grants

- **Add** a grantee (don't clobber): prefix the privilege → **`'+select': ['user_c']`**.
- **Revoke all** for a privilege: empty list → **`select: []`**.
- Deleting the whole grants section = dbt stops managing grants (no change).

## 11. Python models
→ https://docs.getdbt.com/docs/build/python-models

- Signature: **`def model(dbt, session)`**, must **return a single DataFrame**.
- Refs: `dbt.ref(...)`, `dbt.source(...)`; `.py` file in `models/`.
- Only `table` and `incremental` materializations (no view/ephemeral).
- `--empty` / `--sample` are **ignored**.

---

### 30-second self-test before you walk in
event_time/begin/batch_size · `--empty`=compile, `--sample`=event_time+.render() ·
Maturity=on · warning≠behavior change · DBT_ENGINE_ · timestamp↔updated_at, check↔check_cols ·
enforced:true · append_new_columns/fail · latest_version · --favor-state · ephemeral-never-deferred ·
result: · run_results.json · retry-no-op · exposure=name/type/owner · '+select' / select:[] ·
Python ignores --empty/--sample.
