---
title: "Source summary — Exposure properties"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "06 — External dependencies"
source: ../../raw/docs__reference__exposure-properties.md
source_url: https://docs.getdbt.com/reference/exposure-properties
---

# Exposure properties — summary

**What it covers:** The full YAML property reference for declaring exposures, including naming rules, the config block, and project-level configs.

## Key points
- Exposures are defined in `properties.yml` files under an `exposures:` key; you may define them in YAML files that also define `sources` or `models`. Files can be named anything `.yml` and nested in subfolders under `models/`.
- Exposure **names must contain only letters, numbers, and underscores** (no spaces/special chars). Use `label` for a human-friendly title-cased name.
- Property schema: `name`, `description`, `type` (`{dashboard, notebook, analysis, ml, application}`), `url`, `maturity` (`{high, medium, low}`), `enabled` (`true | false`), `config:` block, `owner:` (supports `name` and `email` only), `depends_on:` (list of `ref()`, `source()`, `metric()`), and `label`.
- **In v1.10, `tags` and `meta` moved under the `config:` block** (e.g. `config: { tags: [...], meta: {...}, enabled: ... }`).
- `owner` supports **`name` and `email` only**.
- **Project-level configs:** define under the `exposures:` key in `dbt_project.yml` with the `+` prefix; currently **only the `enabled` config is supported** (e.g. `exposures:\n  +enabled: true`).

## Exam-relevant tokens
`exposures:`, `name`, `type`, `url`, `maturity`, `enabled`, `config:`, `tags`, `meta`, `owner` (`name`/`email`), `depends_on`, `ref`, `source`, `metric`, `label`, `+enabled`

## Gotchas
- `tags`/`meta` changed to be nested under `config` in **v1.10** — declaring them at the top level is the older style.
- Only `enabled` is configurable at the project level via the `+` prefix in `dbt_project.yml`; all other exposure properties must be set directly in the YAML definition.
- `owner` accepts only `name` and `email` (per this reference page) — at least one is required.

Source: [Exposure properties](https://docs.getdbt.com/reference/exposure-properties) · raw: `docs__reference__exposure-properties.md`
