---
title: "About the `--empty` flag"
source_url: https://docs.getdbt.com/docs/build/empty-flag
retrieved_via: md-endpoint
fetched: 2026-06-12
---

# About the `--empty` flag

> **Note**
>
> 
> The `--empty` flag is not currently available for Python models. If the flag is used with a Python model, it will be ignored.
> 

During dbt development, you might want to validate that your models are semantically correct without the time-consuming cost of building the entire model in the data warehouse. The [`run`](https://docs.getdbt.com/reference/commands/run), [`build`](https://docs.getdbt.com/reference/commands/build), [`snapshot`](https://docs.getdbt.com/reference/commands/snapshot), and [`compile`](https://docs.getdbt.com/reference/commands/compile) commands support the `--empty` flag. Starting in core v1.12, [`seed`](https://docs.getdbt.com/reference/commands/seed) also supports the `--empty` flag for building schema-only dry runs. The `--empty` flag limits the refs and sources to zero rows. dbt will still execute the model SQL against the target data warehouse but will avoid expensive reads of input data. This validates dependencies and ensures your models will build properly.

### Examples

Run all models in a project while building only the schemas in your development environment:

```
dbt run --empty
```

Run a specific model:

```
dbt run --select path/to/your_model --empty
```

dbt will build and execute the SQL, resulting in an empty schema in the data warehouse.
