---
title: "Source summary — About flags (global configs)"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "03 — Debugging data modeling errors"
source: ../../raw/docs__reference__global-configs__about-global-configs.md
source_url: https://docs.getdbt.com/reference/global-configs/about-global-configs
---

# About flags (global configs) — summary

**What it covers:** what dbt "flags" (global configs) are, the places they can be set, and the available flags including their env-var and project-config support.

## Key points

- **Flags** (a.k.a. **global configs**) fine-tune **_how_** dbt runs the project — distinct from resource-specific configs that say **_what_** to run. They control log output, treating warnings as errors, failing fast, etc., and are **global** (available to all commands).
- Flags can be set in **three places**: `dbt_project.yml` (under a `flags:` dictionary), **environment variables**, and **CLI options**.
  - Some flags **can only** be set in `dbt_project.yml` and **cannot** be overridden per-invocation by a CLI option.
  - A CLI option supported by only specific commands (not all) is generally **not** a "flag".
- **Env-var prefix changed in v1.11:** v1.10 and earlier use the **`DBT_`** prefix; **v1.11+ uses `DBT_ENGINE_`** (e.g. `DBT_FAIL_FAST` → `DBT_ENGINE_FAIL_FAST`).
- Jinja can read flag values via the **`flags` context variable** (e.g. `flags.FAIL_FAST`). Because flag values can differ across invocations, **avoid using `flags` as input to configs or `ref`/`source` resolved during parsing**.
- **`--target`** selects which environment (target, defined in `profiles.yml`) to run against: `dbt run --target dev`, `dbt run --target prod`.
- Selected flags relevant to debugging (with In-project? / CLI):
  - `fail_fast` — CLI `--fail-fast` / `-x` / `--no-fail-fast`; settable in project; env `DBT_ENGINE_FAIL_FAST` (v1.11+).
  - `debug` — CLI `--debug` / `--no-debug`; debug-level logging.
  - `introspect` — CLI `--introspect` / `--no-introspect`; default True; not settable in project.
  - `warn_error` / `warn_error_options` — treat warnings as errors.
  - `log_level` (default info), `log_level_file` (default debug), `log_format`, `log_path`, `quiet`.
  - `use_v2_parser` — v1.11+, CLI `--use-v2-parser`; opt-in v2 parser.
  - `partial_parse`, `populate_cache`, `version_check`, `write_json`, `store_failures`.

## Exam-relevant tokens

`flags:` (in `dbt_project.yml`), `DBT_` (≤v1.10), `DBT_ENGINE_` (v1.11+), `flags` context variable, `flags.FAIL_FAST`, `--fail-fast` / `-x`, `--target`, `--debug`, `--introspect` / `--no-introspect`, `--warn-error`, `--warn-error-options`, `--log-level`, `--quiet`, `--use-v2-parser`

## Gotchas

- The **env-var prefix is version-dependent** — `DBT_` for ≤1.10, `DBT_ENGINE_` for 1.11+. Easy exam trap.
- Some flags are **project-only** (no CLI override); a same-command CLI option isn't always a "flag".
- Don't drive parse-time configs or `ref`/`source` off `flags` — values vary per invocation.

Source: [About flags (global configs)](https://docs.getdbt.com/reference/global-configs/about-global-configs) · raw: `docs__reference__global-configs__about-global-configs.md`
