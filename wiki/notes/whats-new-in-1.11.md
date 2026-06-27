---
title: "What's new for the dbt Core 1.11 certification"
tags: [notes, version, exam-prep, behavior-changes]
updated: 2026-06-27
status: done
---

# What's new in the dbt Core 1.11-era certification

A study note on the features that distinguish the current **dbt Core 1.11**
certification from older exams. Grouped by the version the docs tag them with —
anything tagged ≥ v1.5 is, by definition, content an older exam couldn't cover.

> Scope caveat: this corpus is the dbt **product docs**, not a changelog of the
> *exam*. Differences in exam **format** (question types, passing score, time
> limit) are not in the corpus — ingest a source for those if needed. Everything
> below is grounded in version tags inside `raw/`.

## Net-new capabilities the modern exam leans on

- **Unit tests** — validate SQL logic on static inputs *before* materializing;
  enables test-driven development. Run only in dev/CI, not prod (static inputs =
  no need to spend prod compute). Exclude from prod with `--exclude-resource-type`
  / `DBT_ENGINE_EXCLUDE_RESOURCE_TYPES`. → [unit-tests](../sources/unit-tests.md)
- **Microbatch incremental strategy** (core **v1.9+**) —
  `incremental_strategy='microbatch'` for large time-series data; independent,
  idempotent, retryable batches. Required: `event_time`, `begin`, `batch_size`
  (`hour`/`day`/`month`/`year`); optional: `lookback` (default 1),
  `concurrent_batches`. Set `event_time` on direct parents too, or they aren't
  filtered. → [incremental-microbatch](../sources/incremental-microbatch.md)
- **Model governance suite** — contracts, versions, constraints, `grants`,
  access. Foreign-key constraints can use `ref()` to capture dependencies
  (v1.9+). → [about-model-governance](../sources/about-model-governance.md) ·
  [constraints](../sources/constraints.md) · [contract](../sources/contract.md) ·
  [model-versions](../sources/model-versions.md)
- **Dry-run / cost-saving flags** (own sub-topics on the blueprint):
  - `--empty` — limits refs/sources to **zero rows**; still executes model SQL
    (validates schema/logic). On `run`/`build`/`snapshot`/`compile`. Ignored for
    Python models. → [empty-flag](../sources/empty-flag.md)
  - `--sample` — builds a **time-based slice** of real rows (validates outputs,
    not just deps). On `run`/`build` only; requires `event_time`; opt a ref out
    with `{{ ref('x').render() }}`. → [sample-flag](../sources/sample-flag.md)

## Snapshots, reworked (core v1.9)

- Snapshots defined in **YAML** (not only `.sql` Jinja); `target_schema` became
  **optional**; `hard_deletes` **replaces** `invalidate_hard_deletes`; new
  `dbt_valid_to_current`. → [snapshots](../sources/snapshots.md)

## Config-location migrations (common exam traps)

- Source freshness: `freshness` moved into the source **`config:`** block in
  **v1.9**; `loaded_at_field` moved in **v1.10** (plus new `loaded_at_query`).
  → [freshness](../sources/freshness.md) · [source-configs](../sources/source-configs.md)
- Data tests: `tags` moved to the **`config`** block in **v1.10**; custom config
  keys and test descriptions allowed from v1.9; `arguments:` property for generic
  tests from v1.10.5. → [data-test-configs](../sources/data-test-configs.md)

## Genuinely v1.11-specific (per doc version tags)

- **Behavior-change flags introduced in core 1.11.0** (Introduction phase, default
  `false`): `require_unique_project_resource_names`,
  `require_ref_searches_node_package_before_root`.
- **Env var prefix change**: v1.10-and-earlier use `DBT_`; **v1.11+ uses
  `DBT_ENGINE_`** (e.g. `DBT_ENGINE_EXCLUDE_RESOURCE_TYPES`).
  → [about-global-configs](../sources/about-global-configs.md)
- **UDFs** buildable via `dbt build` from core **v1.11**. → [build](../sources/build.md)
- The **behavior-change framework** itself: three phases
  (Introduction → Maturity → Removal); flags set **only** in the `flags:` dict in
  `dbt_project.yml` (not CLI/env); opt out with `false`, silence warnings via
  `warn_error_options.silence`. → [behavior-changes](../sources/behavior-changes.md)
  - Reached **Maturity in 1.10.0**: `require_resource_names_without_spaces`,
    `source_freshness_run_project_hooks`.
  - Introduced **1.10.0**: `validate_macro_args`,
    `require_all_warnings_handled_by_warn_error`.

## Beyond scope — do NOT over-study (tagged v1.12)

These appear in the docs but are **past the 1.11 target**; don't let them confuse
you on exam day:

- Snapshot `dbt compile` support; `--empty` for `seed`; the beta `selector:`
  node-selection method; `on_error: continue`; `require_sql_header_in_test_configs`
  and other 1.12 behavior flags.

---

Sources: version tags throughout `raw/`, esp.
[behavior-changes](https://docs.getdbt.com/reference/global-configs/behavior-changes),
[about-global-configs](https://docs.getdbt.com/reference/global-configs/about-global-configs),
[incremental-microbatch](https://docs.getdbt.com/docs/build/incremental-microbatch),
[sample-flag](https://docs.getdbt.com/docs/build/sample-flag),
[empty-flag](https://docs.getdbt.com/docs/build/empty-flag),
[snapshots](https://docs.getdbt.com/docs/build/snapshots).
