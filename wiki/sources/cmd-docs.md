---
title: "Source summary — About dbt docs commands"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__reference__commands__cmd-docs.md
source_url: https://docs.getdbt.com/reference/commands/cmd-docs
---

# About dbt docs commands — summary

**What it covers:** the two `dbt docs` subcommands `generate` and `serve`, plus the flags that control catalog generation.

## Key points
- `dbt docs` has two supported subcommands (dbt Core ≤1.11): **`generate`** and **`serve`**.
- **`dbt docs generate`**: (1) copies `index.html` into `target/`, (2) compiles resources so `compiled_code` is in `manifest.json`, (3) queries database metadata to produce `catalog.json`.
- `dbt docs generate --select +orders` limits the nodes in `catalog.json` (restricts step 3 to selected nodes; step 2 unaffected).
- `--no-compile` skips compilation (step 2). `--empty-catalog` skips the warehouse-metadata catalog query (step 3) — faster but no column/table stats; not for production. `--static` embeds `catalog.json` + `manifest.json` into a single shareable `index.html`.
- **`dbt docs serve`**: starts a local webserver on **port 8080** rooted in `target/`. Run `dbt docs generate` first because `serve` depends on the catalog artifact. Change port with `--port`; `--host` is Core-only.

## Exam-relevant tokens
`dbt docs generate`, `dbt docs serve`, `catalog.json`, `manifest.json`, `index.html`, `target/`, `--select +orders`, `--no-compile`, `--empty-catalog`, `--static`, `--port`, port `8080`.

## Gotchas
- `dbt docs serve` requires a prior `dbt docs generate` (it needs `catalog.json`) — otherwise you get a "catalog missing" error.
- `--empty-catalog` produces docs without warehouse metadata (columns/stats) — fine for dev lineage, not production.

Source: [About dbt docs commands](https://docs.getdbt.com/reference/commands/cmd-docs) · raw: `docs__reference__commands__cmd-docs.md`
