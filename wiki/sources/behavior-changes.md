---
title: "Source summary — Behavior changes"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "03 — Debugging data modeling errors"
source: ../../raw/docs__reference__global-configs__behavior-changes.md
source_url: https://docs.getdbt.com/reference/global-configs/behavior-changes
---

# Behavior changes — summary

**What it covers:** behavior-change flags — what a behavior change is, the three phases of a flag's life, and how to set them in `dbt_project.yml`.

## Key points

- A **behavior change** = the same project code and same commands return a **different result** before vs. after the change (e.g. dbt begins raising a validation **error** it didn't before, changes a built-in macro signature, makes a breaking change to artifacts, or removes a structured-log field).
- **Not** behavior changes: fixing a defective/undocumented bug; dbt beginning to raise a **_warning_** (not error); rewording log messages; non-breaking artifact changes.
- **Three phases of a behavior-change flag:**
  1. **Introduction (disabled by default):** new behavior gated behind a flag defaulting to `false`; old behavior preserved.
  2. **Maturity (enabled by default):** default flips `false` → `true`; opt out by setting `false` (you'll see deprecation warnings).
  3. **Removal (generally enabled):** flag and old behavior removed from the codebase, with advance notice.
- **Behavior-change flags must be set in the `flags:` dictionary in `dbt_project.yml`** (not CLI/env) — they're tied to project code and should go through version control and PR/peer review.
- To **opt out** of a behavior change, set its flag to `false`. You'll keep seeing warnings until you either fix the issue (set `true`) or silence with **`warn_error_options.silence`**.
- A maturity date of `-` means the flip date isn't set yet; affected users see deprecation warnings and get advance-warning emails.
- **core v1.11 milestones:** `require_unique_project_resource_names` and `require_ref_searches_node_package_before_root` are **introduced** in core 1.11.0 (disabled by default). `require_resource_names_without_spaces` and `source_freshness_run_project_hooks` reached **maturity** in core 1.10.0. `validate_macro_args` and `require_all_warnings_handled_by_warn_error` were introduced in core 1.10.0.
- Upgrading to **dbt Fusion / core_v2** removes a subset of behavior-change flags and enables their new behavior permanently.

## Exam-relevant tokens

`flags:` dictionary in `dbt_project.yml`, behavior-change flag, Introduction / Maturity / Removal phases, `false` → `true`, `warn_error_options.silence`, deprecation warning, `require_unique_project_resource_names` (core 1.11), `require_ref_searches_node_package_before_root` (core 1.11), `source_freshness_run_project_hooks`, `require_resource_names_without_spaces`, `validate_macro_args`

## Gotchas

- Behavior-change flags are **`dbt_project.yml`-only** — unlike many global configs they are *not* set via CLI or env var.
- A new **warning** is not a behavior change; a new **error** is. The phase determines whether the new behavior is on by default.
- Setting a matured flag back to `false` keeps the legacy behavior but keeps the warnings — silence them only via `warn_error_options.silence`.

Source: [Behavior changes](https://docs.getdbt.com/reference/global-configs/behavior-changes) · raw: `docs__reference__global-configs__behavior-changes.md`
