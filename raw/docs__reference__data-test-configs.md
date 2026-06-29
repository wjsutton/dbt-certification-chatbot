---
title: "Data test configurations"
source_url: https://docs.getdbt.com/reference/data-test-configs
retrieved_via: md-endpoint
fetched: 2026-06-29
---

# Data test configurations

## Related documentation

* [Data tests](https://docs.getdbt.com/docs/build/data-tests)

Data tests can be configured in a few different ways:
1. Properties within `.yml` definition (generic tests only, see [test properties](https://docs.getdbt.com/reference/resource-properties/data-tests) for full syntax)
2. A `config()` block within the test's SQL definition
3. In `dbt_project.yml`

Data test configs are applied hierarchically, in the order of specificity outlined above. In the case of a singular test, the `config()` block within the SQL definition takes precedence over configs in the project YAML file. In the case of a specific instance of a generic test, the test's `.yml` properties would take precedence over any values set in its generic SQL definition's `config()`, which in turn would take precedence over values set in the project YAML file (`dbt_project.yml`).

## Available configurations

Click the link on each configuration option to read more about what it can do.

### Data test-specific configurations

```yaml
data_tests:
  [<resource-path>](https://docs.getdbt.com/reference/resource-configs/resource-path):
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[fail_calc](https://docs.getdbt.com/reference/resource-configs/fail_calc): <string>
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[limit](https://docs.getdbt.com/reference/resource-configs/limit): <integer>
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[severity](https://docs.getdbt.com/reference/resource-configs/severity): error | warn
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[error_if](https://docs.getdbt.com/reference/resource-configs/severity): <string>
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[warn_if](https://docs.getdbt.com/reference/resource-configs/severity): <string>
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[store_failures](https://docs.getdbt.com/reference/resource-configs/store_failures): true | false
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[where](https://docs.getdbt.com/reference/resource-configs/where): <string>

```

```jinja

{{ config(
    [fail_calc](https://docs.getdbt.com/reference/resource-configs/fail_calc) = "<string>",
    [limit](https://docs.getdbt.com/reference/resource-configs/limit) = <integer>,
    [severity](https://docs.getdbt.com/reference/resource-configs/severity) = "error | warn",
    [error_if](https://docs.getdbt.com/reference/resource-configs/severity) = "<string>",
    [warn_if](https://docs.getdbt.com/reference/resource-configs/severity) = "<string>",
    [store_failures](https://docs.getdbt.com/reference/resource-configs/store_failures) = true | false,
    [where](https://docs.getdbt.com/reference/resource-configs/where) = "<string>"
) }}

```

```yaml
<resource_type>:
  - name: <resource_name>
    data_tests:
      - <test_name>: # # Actual name of the test. For example, dbt_utils.equality
          name: # Human friendly name for the test. For example, equality_fct_test_coverage
          [description](https://docs.getdbt.com/reference/resource-properties/description): "markdown formatting"
          arguments: # Available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
            <argument_name>: <argument_value>
          [config](https://docs.getdbt.com/reference/resource-properties/config):
            [fail_calc](https://docs.getdbt.com/reference/resource-configs/fail_calc): <string>
            [limit](https://docs.getdbt.com/reference/resource-configs/limit): <integer>
            [severity](https://docs.getdbt.com/reference/resource-configs/severity): error | warn
            [error_if](https://docs.getdbt.com/reference/resource-configs/severity): <string>
            [warn_if](https://docs.getdbt.com/reference/resource-configs/severity): <string>
            [store_failures](https://docs.getdbt.com/reference/resource-configs/store_failures): true | false
            [where](https://docs.getdbt.com/reference/resource-configs/where): <string>
            # Available in v1.12 and higher. Requires enabling the `require_sql_header_in_test_configs` flag.
            [sql_header](https://docs.getdbt.com/reference/resource-configs/sql_header): <string> 

    [columns](https://docs.getdbt.com/reference/resource-properties/columns):
      - name: <column_name>
        data_tests:
          - <test_name>:
              name:
              [description](https://docs.getdbt.com/reference/resource-properties/description): "markdown formatting"
              arguments: # Available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                <argument_name>: <argument_value>
              [config](https://docs.getdbt.com/reference/resource-properties/config):
                [fail_calc](https://docs.getdbt.com/reference/resource-configs/fail_calc): <string>
                [limit](https://docs.getdbt.com/reference/resource-configs/limit): <integer>
                [severity](https://docs.getdbt.com/reference/resource-configs/severity): error | warn
                [error_if](https://docs.getdbt.com/reference/resource-configs/severity): <string>
                [warn_if](https://docs.getdbt.com/reference/resource-configs/severity): <string>
                [store_failures](https://docs.getdbt.com/reference/resource-configs/store_failures): true | false
                [where](https://docs.getdbt.com/reference/resource-configs/where): <string>
                # Available in v1.12 and higher. Requires enabling the `require_sql_header_in_test_configs` flag.
                [sql_header](https://docs.getdbt.com/reference/resource-configs/sql_header): <string> 
```

This configuration mechanism is supported for specific instances of generic tests only. To configure a specific singular test, you should use the `config()` macro in its SQL definition.

Starting in core v1.12, you can set [`sql_header`](https://docs.getdbt.com/reference/resource-configs/sql_header) in the `config` of a generic data test at the model or column level of your `properties.yml`. Enable the [`require_sql_header_in_test_configs`](https://docs.getdbt.com/reference/global-configs/behavior-flag-introduction#sql_header-in-data-tests) flag to use `config.sql_header` in your data tests.

### General configurations

```yaml
data_tests:
  [<resource-path>](https://docs.getdbt.com/reference/resource-configs/resource-path):
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[enabled](https://docs.getdbt.com/reference/resource-configs/enabled): true | false
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[tags](https://docs.getdbt.com/reference/resource-configs/tags): <string> | [<string>]
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[meta](https://docs.getdbt.com/reference/resource-configs/meta): {dictionary}
    # relevant for [store_failures](https://docs.getdbt.com/reference/resource-configs/store_failures) only
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[database](https://docs.getdbt.com/reference/resource-configs/database): <string>
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[schema](https://docs.getdbt.com/reference/resource-properties/schema): <string>
    [+](https://docs.getdbt.com/reference/resource-configs/plus-prefix)[alias](https://docs.getdbt.com/reference/resource-configs/alias): <string>
```

```jinja

{{ config(
    [enabled](https://docs.getdbt.com/reference/resource-configs/enabled)=true | false,
    [tags](https://docs.getdbt.com/reference/resource-configs/tags)="<string>" | ["<string>"]
    [meta](https://docs.getdbt.com/reference/resource-configs/meta)={dictionary},
    [database](https://docs.getdbt.com/reference/resource-configs/database)="<string>",
    [schema](https://docs.getdbt.com/reference/resource-properties/schema)="<string>",
    [alias](https://docs.getdbt.com/reference/resource-configs/alias)="<string>",
) }}

```

```yaml

<resource_type>:
  - name: <resource_name>
    data_tests:
      - <test_name>: # Actual name of the test. For example, dbt_utils.equality
          name: # Human friendly name for the test. For example, equality_fct_test_coverage
          [description](https://docs.getdbt.com/reference/resource-properties/description): "markdown formatting"
          arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
            <argument_name>: <argument_value>
          [config](https://docs.getdbt.com/reference/resource-properties/config):
            [enabled](https://docs.getdbt.com/reference/resource-configs/enabled): true | false
            [tags](https://docs.getdbt.com/reference/resource-configs/tags): <string> | [<string>]
            [meta](https://docs.getdbt.com/reference/resource-configs/meta): {dictionary}
            # relevant for [store_failures](https://docs.getdbt.com/reference/resource-configs/store_failures) only
            [database](https://docs.getdbt.com/reference/resource-configs/database): <string>
            [schema](https://docs.getdbt.com/reference/resource-properties/schema): <string>
            [alias](https://docs.getdbt.com/reference/resource-configs/alias): <string>

    [columns](https://docs.getdbt.com/reference/resource-properties/columns):
      - name: <column_name>
        data_tests:
          - <test_name>:
              name: 
              [description](https://docs.getdbt.com/reference/resource-properties/description): "markdown formatting"
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                <argument_name>: <argument_value>
              [config](https://docs.getdbt.com/reference/resource-properties/config):
                [enabled](https://docs.getdbt.com/reference/resource-configs/enabled): true | false
                [tags](https://docs.getdbt.com/reference/resource-configs/tags): <string> | [<string>]
                [meta](https://docs.getdbt.com/reference/resource-configs/meta): {dictionary}
                # relevant for [store_failures](https://docs.getdbt.com/reference/resource-configs/store_failures) only
                [database](https://docs.getdbt.com/reference/resource-configs/database): <string>
                [schema](https://docs.getdbt.com/reference/resource-properties/schema): <string>
                [alias](https://docs.getdbt.com/reference/resource-configs/alias): <string>
```

This configuration mechanism is supported for specific instances of generic data tests only. To configure a specific singular test, you should use the `config()` macro in its SQL definition.

### Examples

#### Add a tag to one test

If a specific instance of a generic data test:

.yml'>

```yml
models:
  - name: my_model
    columns:
      - name: id
        data_tests:
          - unique:
              config:
                tags: ['my_tag'] # changed to config in v1.10
```

If a singular data test:

.sql'>

```sql
{{ config(tags = ['my_tag']) }}

select ...
```

#### Set the default severity for all instances of a generic data test

.sql'>

```sql
{% test my_test() %}

    {{ config(severity = 'warn') }}

    select ...

{% endtest %}
```

#### Disable all data tests from a package

```yml
data_tests:
  package_name:
    +enabled: false
```

#### Specify custom configurations for generic data tests

Beginning in dbt v1.9, you can use any custom config key to specify custom configurations for data tests. For example, the following specifies the `snowflake_warehouse` custom config that dbt should use when executing the `accepted_values` data test:

```yml

models:
  - name: my_model
    columns:
      - name: color
        data_tests:
          - accepted_values:
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                values: ['blue', 'red']
              config:
                severity: warn
                snowflake_warehouse: my_warehouse

```

Given the config, the data test runs on a different Snowflake virtual warehouse than the one in your default connection to enable better price-performance with a different warehouse size or more granular cost allocation and visibility.

#### Add a description to generic and singular tests

Starting from dbt v1.9 (also available to dbt [release tracks](https://docs.getdbt.com/docs/dbt-versions/dbt-release-tracks)), you can add [descriptions](https://docs.getdbt.com/reference/resource-properties/data-tests#description) to both generic and singular tests.

For a generic test, add the description in line with the existing YAML:

.yml'>

```yml

models:
  - name: my_model
    columns:
      - name: delivery_status
        data_tests:
          - accepted_values:
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                values: ['delivered', 'pending', 'failed']
              description: "This test checks whether there are unexpected delivery statuses. If it fails, check with logistics team"

```

You can also add descriptions to the Jinja macro that provides the core logic of a generic data test. Refer to the [Add description to generic data test logic](https://docs.getdbt.com/best-practices/writing-custom-generic-tests#add-description-to-generic-data-test-logic) for more information.

For a singular test, define it in the test's directory:

```yml

data_tests: 
  - name: my_custom_test
    description: "This test checks whether the rolling average of returns is inside of expected bounds. If it isn't, flag to customer success team"

```

For more information refer to [Add a description to a data test](https://docs.getdbt.com/reference/resource-properties/description#add-a-description-to-a-data-test).

<VersionBlock firstVersion="1.12">

#### Set `sql_header` in a generic data test

When the [`require_sql_header_in_test_configs`](https://docs.getdbt.com/reference/global-configs/behavior-flag-introduction#sql_header-in-data-tests) flag is enabled, you can set [`sql_header`](https://docs.getdbt.com/reference/resource-configs/sql_header) in the `config` of a generic data test so that the specified SQL runs before the test executes (for example, to set session parameters or add a comment):

```yaml
models:
  - name: orders
    columns:
      - name: order_id
        data_tests:
          - not_null:
              name: not_null_orders_order_id
              config:
                sql_header: "-- SQL_HEADER_TEST_MARKER"
```

</VersionBlock>
