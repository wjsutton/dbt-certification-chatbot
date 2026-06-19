---
title: "Materializations best practices"
source_url: https://docs.getdbt.com/best-practices/materializations/1-guide-overview
retrieved_via: html-extract
fetched: 2026-06-12
---

# Materializations best practices

What *really* happens when you type `dbt build`? This guide explores the objects that get built into your warehouse, why they matter, and how dbt knows what to build.

The configurations that tell dbt how to construct these objects are called *materializations*, and knowing how to use them is a crucial skill for effective analytics engineering. When you've completed this guide, you'll be able to use the three core materializations that cover most common analytics engineering situations.

> **Info — Materializations abstract away DDL and DML.** Typically in raw SQL- or Python-based data transformation, you have to write specific imperative instructions on how to build or modify your data objects. dbt's materializations make this declarative: we tell dbt how we want things constructed and it figures out how to do that given the unique conditions and qualities of our warehouse.

## Learning goals

By the end of this guide you should have a solid understanding of:

- what **materializations** are
- how the three main materializations that ship with dbt — **table**, **view**, and **incremental** — differ
- **when** and **where** to use specific materializations to optimize your development and production builds
- how to **configure materializations** at various scopes, from an individual model to an entire folder

## Prerequisites

- You'll want to have worked through the [quickstart guide](https://docs.getdbt.com/guides) and have a project set up.
- Concepts like dbt runs, `ref()` statements, and models should be familiar to you.
- [Optional] Reading [How we structure our dbt projects](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview) will help with the last section, on best practices using staging models and marts.

## Guiding principle

The basic guideline is **start as simple as possible**. Follow a tiered approach, only moving up a tier when necessary:

- **Start with a view.** When the view gets too long to *query* for end users,
- **Make it a table.** When the table gets too long to *build* in your dbt jobs,
- **Build it incrementally.** That is, layer the data on in chunks as it comes in.
