---
title: "Source summary — Test smarter not harder: add the right tests to your dbt project"
tags: [source-summary]
status: done
updated: 2026-06-12
domain: "05 — Implementing dbt tests"
source: ../../raw/docs__blog__test-smarter-not-harder.md
source_url: https://docs.getdbt.com/blog/test-smarter-not-harder
---

# Test smarter not harder: add the right tests — summary

**What it covers:** a framework for *which* tests to add — first define data quality, then prioritize which failures should fail the pipeline.

## Key points

- Testing is a phase of the **ADLC** (Analytics Development Lifecycle) and should **drive data quality**. Avoid both over-testing (alert fatigue / noise) and under-testing (only primary keys).
- **Define data quality in three buckets:**
  1. **Data hygiene** — formatting, completeness, granularity; addressed in the **staging layer** (e.g. unique+not_null primary keys, columns that should always have text, valid email domains).
  2. **Business-focused anomalies** — data that differs from what's typical for the business; **human-set and fluid**, needing periodic re-tuning (e.g. "sales change > 20% day-over-day"). Identify by starting at the **BI layer**: pick 1–3 dashboards and list expected behaviors.
  3. **Stats-focused anomalies** — volume/dimensional anomalies, values many standard deviations from the mean; more advanced, do after the first two.
- **Prioritize by real-life impact.** Make a test **pipeline-failing (`error` severity)** if the concern is **customer-facing**, **used for financial decisions**, or **executive-facing**. Everything else is a "nice-to-know": set to **`warn`** or remove it.
- A test should only exist if you can take a **specific action** when it fails. Keep a nice-to-know test (as a warning) only if you're gathering evidence for an action planned within ~6 months.
- **Action plan:** write 1–2 debugging steps per concern (consider adding to the test's `description`), then source ready-made tests from hub.getdbt.com — `dbt-expectations` and `dbt_utils`. Keep the prioritized list as a living doc linked in the README.

## Exam-relevant tokens

`severity`, `error`, `warn`, `description`, ADLC, staging-layer hygiene, `dbt-expectations`, `dbt_utils`, customer-facing / financial / executive-facing → error

## Gotchas

- Severity choice is deliberate: only customer-facing / financial / executive-facing concerns warrant `error`; the rest are `warn` or untested.
- Data-hygiene tests belong in **staging**; business anomalies are human-set and need re-tuning (e.g. during hypergrowth).
- A test with no actionable response shouldn't exist.

Source: [Test smarter not harder: add the right tests to your dbt project](https://docs.getdbt.com/blog/test-smarter-not-harder) · raw: `docs__blog__test-smarter-not-harder.md`
