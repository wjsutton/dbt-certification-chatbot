---
title: "Test smarter not harder: Where should tests go in your pipeline?"
source_url: https://docs.getdbt.com/blog/test-smarter-where-tests-should-go
retrieved_via: html-extract
fetched: 2026-06-12
---

# Test smarter not harder: Where should tests go in your pipeline?

A follow-up to "add the right tests": *where* specific tests belong, layer by layer (based on dbt Labs' staging → intermediate → marts structure).

**At a glance:**
- **Source tests** → *fixable-at-the-source* data quality concerns.
- **Staging tests** → business-focused anomalies specific to individual tables (e.g. accepted ranges, sequential values). Staging also cleans nulls/duplicates/outliers you can't fix at source — don't test your own cleanup.
- **Intermediate & marts tests** → business-focused anomalies arising from joins/calculations, plus primary-key/not-null tests where protecting the grain matters.

## Sources
Apply tests that flag **fixable-at-the-source-system** issues (you can fix it, or know who will). If a source issue isn't fixable, remove the test and mitigate in staging instead.
- **Source freshness:** for sources critical to your pipelines. If a source feeds a top-3 priority category, run [`dbt source freshness`](https://docs.getdbt.com/docs/deploy/source-freshness) in job commands at severity **`error`** (so the job fails on stale data). Otherwise set severity **`warn`** and still run it.
- **Data hygiene** fixable at source: removable duplicate customer records, enterable null names/emails, primary-key tests where duplicates are removable at source.

## Staging
Models clean up / mitigate issues that can't be fixed at source; **tests focus on business anomaly detection**.
- Don't add tests to your cleanup (filtering nulls then adding `not_null` is repetitive).
- Business-anomaly examples: values outside an acceptable **range** (e.g. selling more limited-edition items than were stocked); values that should always be **positive** (a negative non-return transaction); an unexpected **volume** uptick beyond a pre-defined percentage.

## Intermediate (if applicable)
Focus on **data hygiene + anomaly tests for new columns**; don't re-test passthrough columns.
- Re-grained models → add a **primary key** test (also on same-grain-but-enriched models, to signal intent).
- First joins/aggregations → simple anomaly tests: [`accepted_values`](https://docs.getdbt.com/reference/resource-properties/data-tests#accepted_values) on a new categorical column, `mutually_exclusive_ranges` (dbt_utils) on related columns, `not_constant` (dbt_utils) on a column that should keep changing.
- Complex SQL → consider [unit tests](https://docs.getdbt.com/docs/build/unit-tests).

## Marts
Same hygiene-or-anomaly pattern, focused on **net-new columns**:
- **Unit tests** for especially complex transformation logic (date/forecasting math, CASE-WHEN-heavy customer segmentation).
- **Primary key** tests where the mart's grain changed (or enriched-same-grain models, to communicate intent).
- **Business-anomaly** tests on new calculated fields (singular tests on high-impact tables; fields that shouldn't vary > X% per week; ledger rules like "today's running total ≥ yesterday's").

## CI/CD & Advanced CI
Automate the framework: run a **[Slim CI](https://docs.getdbt.com/best-practices/best-practice-workflows#run-only-modified-models-to-test-changes-slim-ci)** to optimise resource use. Start with dbt Cloud's **Advanced CI** "compare changes" flags (modified / added / removed) for confidence before peer review.

**Takeaway:** judicious testing needs a *plan* (like marathon training); place tests deliberately by layer, and revise the strategy as needs evolve.
