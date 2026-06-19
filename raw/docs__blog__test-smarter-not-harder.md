---
title: "Test smarter not harder: add the right tests to your dbt project"
source_url: https://docs.getdbt.com/blog/test-smarter-not-harder
retrieved_via: html-extract
fetched: 2026-06-12
---

# Test smarter not harder: add the right tests to your dbt project

Testing is a key phase of the Analytics Development Lifecycle (ADLC) and should *drive data quality*. Many teams over-test (so many tests that errors become noise and cause alert fatigue) or under-test (only primary keys). This post offers a middle path: first **define** data quality, then **prioritize** it.

## Define data quality — three buckets

List 2–3 concerns in your own business context for each bucket:

1. **Data hygiene** — issues you address in the **staging layer**; data meeting expectations on formatting, completeness, and granularity. Examples:
   - *Granularity:* primary keys are unique and not null (duplicates skew calculations).
   - *Completeness:* columns that should always contain text, do.
   - *Formatting:* email addresses always have a valid domain.
2. **Business-focused anomalies** — aspects of the data that differ from what you know to be typical for your business. Set by a human, so they're fluid and need periodic adjustment (e.g. a "sales change > 20% day-over-day" fraud/OMS check that must be re-tuned during hypergrowth). Identify them by starting at your BI layer: pick 1–3 frequently used dashboards/tables and list 1–3 expected behaviors each (e.g. "revenue shouldn't change > X% in Y time", "monthly active users shouldn't decline > X% after onboarding"). Also guard against past incidents.
3. **Stats-focused anomalies** — fluctuations against expected volumes/metrics (volume anomalies, dimensional anomalies, column values many standard deviations from the mean). More advanced; tackle after hygiene + business anomalies.

## Prioritize — which failures should fail the pipeline

Think about real-life impact. Treat as high-impact, **pipeline-failing (error severity)** anything that is:
- **customer-facing**, or
- **used for financial decisions**, or
- **executive-facing**.

Everything else is a **nice-to-know**: set it to **warning**, or remove it. A test should only exist if you can take a *specific action* when it fails. (Keep a nice-to-know test only if you're gathering evidence for an action planned within ~6 months — still as a warning.)

## Action plan
For each prioritized concern, write 1–2 initial debugging steps (and consider adding them to the test's `description`). Then find tests on hub.getdbt.com that address your top concerns — `dbt-expectations` and `dbt_utils` are good starting points. Error-marked concerns get **error** severity; nice-to-knows are **not tested or set to warning**. Keep this prioritized list as a living document linked in your project README.

**Key exam-relevant ideas:** testing should drive *action*; use **severity** (`error` vs `warn`) deliberately; data hygiene tests belong in **staging**; business anomalies are human-set and fluid.
