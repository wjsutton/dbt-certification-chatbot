---
title: "docs__reference__dbt_project.yml.md"
source_url: https://docs.getdbt.com/reference/dbt_project.yml
retrieved_via: md-endpoint
fetched: 2026-06-12
---

Every [dbt project](https://docs.getdbt.com/docs/build/projects) needs a `dbt_project.yml` file — this is how dbt knows a directory is a dbt project. It also contains important information that tells dbt how to operate your project. It works as follows:

- dbt uses [YAML](https://yaml.org/) in a few different places. If you're new to YAML, it would be worth learning how arrays, dictionaries, and strings are represented.
- By default, dbt looks for the `dbt_project.yml` in your current working directory and its parents, but you can set a different directory using the `--project-dir` flag or the <VersionBlock lastVersion="1.10">`DBT_PROJECT_DIR`</VersionBlock><VersionBlock firstVersion="1.11">`DBT_ENGINE_PROJECT_DIR`</VersionBlock> environment variable.
- Specify your dbt project ID in the `dbt_project.yml` file using `project-id` under the [`dbt-cloud` config](https://docs.getdbt.com/reference/dbt_cloud.yml#the-dbt-cloud-block-in-dbt_projectyml). Find your project ID in your dbt project URL: For example, in `https://YOUR_ACCESS_URL/develop/projects/123456`, the project ID is `123456`.

- Note, you can't set up a "property" in the `dbt_project.yml` file if it's not a config (an example is [macros](https://docs.getdbt.com/reference/macro-properties)). This applies to all types of resources. Refer to [Configs and properties](https://docs.getdbt.com/reference/configs-and-properties) for more detail.

## Example

The following example is a list of all available configurations in the `dbt_project.yml` file:

```yml
[name](https://docs.getdbt.com/reference/project-configs/name): string

[config-version](https://docs.getdbt.com/reference/project-configs/config-version): 2
[version](https://docs.getdbt.com/reference/project-configs/version): version

[profile](https://docs.getdbt.com/reference/project-configs/profile): profilename

[model-paths](https://docs.getdbt.com/reference/project-configs/model-paths): [directorypath]
[seed-paths](https://docs.getdbt.com/reference/project-configs/seed-paths): [directorypath]
[test-paths](https://docs.getdbt.com/reference/project-configs/test-paths): [directorypath]
[analysis-paths](https://docs.getdbt.com/reference/project-configs/analysis-paths): [directorypath]
[macro-paths](https://docs.getdbt.com/reference/project-configs/macro-paths): [directorypath]
[snapshot-paths](https://docs.getdbt.com/reference/project-configs/snapshot-paths): [directorypath]
[docs-paths](https://docs.getdbt.com/reference/project-configs/docs-paths): [directorypath]
[asset-paths](https://docs.getdbt.com/reference/project-configs/asset-paths): [directorypath]
[function-paths](https://docs.getdbt.com/reference/project-configs/function-paths): [directorypath]

[packages-install-path](https://docs.getdbt.com/reference/project-configs/packages-install-path): directorypath

[clean-targets](https://docs.getdbt.com/reference/project-configs/clean-targets): [directorypath]

[query-comment](https://docs.getdbt.com/reference/project-configs/query-comment): string

[require-dbt-version](https://docs.getdbt.com/reference/project-configs/require-dbt-version): version-range | [version-range]

[flags](https://docs.getdbt.com/reference/global-configs/project-flags):
  [<global-configs>](https://docs.getdbt.com/reference/global-configs/project-flags)

[dbt-cloud](https://docs.getdbt.com/reference/dbt_cloud.yml#the-dbt-cloud-block-in-dbt_projectyml):
  [project-id](https://docs.getdbt.com/docs/platform/configure-dbt-cli#configure-the-dbt-cli): project_id # Required
  [defer-env-id](https://docs.getdbt.com/docs/platform/about-defer#defer-in-dbt-cli): environment_id # Optional
  [account-host](https://docs.getdbt.com/docs/platform/about-platform/access-regions-ip-addresses): account-host # Defaults to 'cloud.getdbt.com'; Required if use a different Access URL

[analyses](https://docs.getdbt.com/docs/build/analyses): # Requires the require_corrected_analysis_fqns flag; available starting v1.12
  [<analysis-configs>](https://docs.getdbt.com/reference/analysis-properties)

[exposures](https://docs.getdbt.com/docs/build/exposures):
  +[enabled](https://docs.getdbt.com/reference/resource-configs/enabled): true | false

[quoting](https://docs.getdbt.com/reference/project-configs/quoting):
  database: true | false
  schema: true | false
  identifier: true | false
  snowflake_ignore_case: true | false  # Fusion-only config. Aligns with Snowflake's session parameter QUOTED_IDENTIFIERS_IGNORE_CASE behavior. 
                                       # Ignored by dbt Core and other adapters.
metrics:
  [<metric-configs>](https://docs.getdbt.com/docs/build/metrics-overview)

models:
  [<model-configs>](https://docs.getdbt.com/reference/model-configs)

seeds:
  [<seed-configs>](https://docs.getdbt.com/reference/seed-configs)

semantic-models:
  [<semantic-model-configs>](https://docs.getdbt.com/docs/build/semantic-models)

saved-queries:
  [<saved-queries-configs>](https://docs.getdbt.com/docs/build/saved-queries)

snapshots:
  [<snapshot-configs>](https://docs.getdbt.com/reference/snapshot-configs)

sources:
  [<source-configs>](source-configs)
  
data_tests:
  [<test-configs>](https://docs.getdbt.com/reference/data-test-configs)

vars:
  [<variables>](https://docs.getdbt.com/docs/build/project-variables)

[on-run-start](https://docs.getdbt.com/reference/project-configs/on-run-start-on-run-end): sql-statement | [sql-statement]
[on-run-end](https://docs.getdbt.com/reference/project-configs/on-run-start-on-run-end): sql-statement | [sql-statement]

[dispatch](https://docs.getdbt.com/reference/project-configs/dispatch-config):
  - macro_namespace: packagename
    search_order: [packagename]

[restrict-access](https://docs.getdbt.com/docs/mesh/govern/model-access): true | false

functions:
  [<function-configs>](https://docs.getdbt.com/reference/function-configs)

```

## The `+` prefix

## Naming convention

It's important to follow the correct YAML naming conventions for the configs in your `dbt_project.yml` file to ensure dbt can process them properly. This is especially true for resource types with more than one word.

- Use dashes (`-`) when configuring resource types with multiple words in your `dbt_project.yml` file. Here's an example for [saved queries](https://docs.getdbt.com/docs/build/saved-queries#configure-saved-query):

    

    ```yml
    saved-queries:  # Use dashes for resource types in the dbt_project.yml file.
      my_saved_query:
        +cache:
          enabled: true
    ```
    

- Use underscore (`_`) when configuring resource types with multiple words for YAML files other than the `dbt_project.yml` file. For example, here's the same saved queries resource in the `semantic_models.yml` file:

    

    ```yml
    saved_queries:  # Use underscores everywhere outside the dbt_project.yml file.
      - name: saved_query_name
        ... # Rest of the saved queries configuration.
        config:
          cache:
            enabled: true
    ```
