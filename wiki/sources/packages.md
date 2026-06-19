---
title: "Source summary — Packages"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "01 — Developing & optimizing dbt models"
source: ../../raw/docs__docs__build__packages.md
source_url: https://docs.getdbt.com/docs/build/packages
---

# Packages — summary

**What it covers:** using dbt packages — standalone dbt projects you add as dependencies via `packages.yml`/`dependencies.yml` + `dbt deps`.

## Key points
- A dbt package is a standalone dbt project (models, macros, resources). Adding it makes its resources part of yours: package models materialize on `dbt run`, and you can `ref`/`source`/use its macros.
- **Adding a package:** create `packages.yml` or `dependencies.yml` at the same level as `dbt_project.yml`, specify packages, then run **`dbt deps`** to install. Packages install into the `dbt_packages` directory (default `packages-install-path`), which git ignores by default.
- **Hub packages (recommended):** `package: dbt-labs/snowplow` + `version:` (a version is required); use semantic-version ranges like `version: [">=0.7.0", "<0.8.0"]`. Hub installs let dbt resolve duplicate transitive dependencies.
- **Git packages:** `git: "..."` + optional `revision:` (branch, tag, or full 40-char commit hash). **Local packages:** `local: relative/path` (monorepos, testing changes). **Tarball:** `tarball:` + `name:`. **Private:** `private:` + `provider:` (`github`/`gitlab`/`ado`).
- **Pinning:** `dbt deps` "pins" packages by writing/updating `package-lock.yml`. Subsequent `dbt deps` install from the lockfile unless `packages.yml`/`dependencies.yml` changed; get updates with `dbt deps --upgrade`.
- Updating/uninstalling: changing a version needs `dbt deps` to take effect; remove + `dbt clean` then `dbt deps` to fully uninstall. Configure package vars/models via `dbt_project.yml`; project configs override package configs. Unpinned git packages warn unless `warn-unpinned: false`.
- Note: dbt packages are distinct from Python (PyPI) packages.

## Exam-relevant tokens
`packages.yml`, `dependencies.yml`, `dbt deps`, `dbt deps --upgrade`, `dbt_packages`, `packages-install-path`, `package:`/`version:`, `git:`/`revision:`, `local:`, `tarball:`/`name:`, `private:`/`provider:`, `package-lock.yml`, `dbt clean`, `warn-unpinned`.

## Gotchas
- Hub packages **require** a version; git packages should specify a `revision` or dbt warns "not pinned."
- `dbt deps` pins to `package-lock.yml` — later commits/versions are NOT auto-installed; use `dbt deps --upgrade` to refresh.
- Changing a version in `packages.yml` isn't applied until you re-run `dbt deps`.

Source: [Packages](https://docs.getdbt.com/docs/build/packages) · raw: `docs__docs__build__packages.md`
