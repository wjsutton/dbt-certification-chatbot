---
title: "Source summary — Test smarter not harder: Where should tests go in your pipeline?"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "05 — Implementing dbt tests"
source: ../../raw/docs__blog__test-smarter-where-tests-should-go.md
source_url: https://docs.getdbt.com/blog/test-smarter-where-tests-should-go
---

# Test smarter not harder: where should tests go — summary

**What it covers:** *where* in the staging → intermediate → marts pipeline each kind of test belongs, including source freshness and CI/CD.

## Key points

- **At a glance:** source tests → fixable-at-the-source concerns; staging tests → business anomalies specific to individual tables; intermediate/marts tests → anomalies from joins/calculations + primary-key/not-null where grain matters.
- **Sources:** apply tests that flag **fixable-at-the-source-system** issues (you can fix it or know who will). If a source issue isn't fixable, remove the test and mitigate in staging.
  - **Source freshness:** run `dbt source freshness` in job commands for critical sources. If the source feeds a top-3 priority category, set severity **`error`** (job fails on stale data); otherwise **`warn`** and still run it.
  - Hygiene fixable at source: removable duplicate records, enterable null names/emails, primary-key tests where duplicates are removable at source.
- **Staging:** models clean up what can't be fixed at source; **tests focus on business-anomaly detection** (out-of-range values, values that should always be positive, unexpected volume upticks). **Don't test your own cleanup** (e.g. filtering nulls then re-adding `not_null`).
- **Intermediate:** data hygiene + anomaly tests for **new** columns; don't re-test passthrough columns. Re-grained models → add a **primary key** test; first joins/aggregations → `accepted_values`, `mutually_exclusive_ranges` (dbt_utils), `not_constant` (dbt_utils). Complex SQL → consider **unit tests**.
- **Marts:** same hygiene-or-anomaly pattern on **net-new** columns. **Unit tests** for especially complex transformation logic (date/forecasting math, CASE-WHEN-heavy segmentation); **primary key** tests where grain changed; business-anomaly tests on new calculated fields.
- **CI/CD:** automate with **Slim CI** to optimize resources; use dbt Cloud **Advanced CI** "compare changes" (modified/added/removed) flags for confidence before peer review.

## Exam-relevant tokens

`dbt source freshness`, `severity` (`error` / `warn`), `not_null`, `accepted_values`, `mutually_exclusive_ranges`, `not_constant`, unit tests, primary-key tests, Slim CI, Advanced CI

## Gotchas

- Stale-data should **fail** the job (`error`) only for top-priority sources; otherwise `warn`.
- Don't add `not_null` (or similar) to columns you just cleaned in staging — it's redundant.
- Test **new** columns at each layer; don't re-test passthrough columns carried down from upstream.

Source: [Test smarter not harder: Where should tests go in your pipeline?](https://docs.getdbt.com/blog/test-smarter-where-tests-should-go) · raw: `docs__blog__test-smarter-where-tests-should-go.md`
