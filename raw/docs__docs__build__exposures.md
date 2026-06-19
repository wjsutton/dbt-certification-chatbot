---
title: "Add Exposures to your DAG"
source_url: https://docs.getdbt.com/docs/build/exposures
retrieved_via: md-endpoint
fetched: 2026-06-12
---

# Add Exposures to your DAG

Exposures make it possible to define and describe a downstream use of your dbt project, such as in a dashboard, application, or data science pipeline. By defining exposures, you can then:
- run, test, and list resources that feed into your exposure
- populate a dedicated page in the auto-generated [documentation](https://docs.getdbt.com/docs/build/documentation) site with context relevant to data consumers

Exposures can be defined in two ways:
- Manual &mdash; Declared [explicitly](https://docs.getdbt.com/docs/build/exposures#declaring-an-exposure) in your project’s YAML files.
- Automatic &mdash;  dbt [creates and visualizes downstream exposures](https://docs.getdbt.com/docs/platform-integrations/downstream-exposures) automatically for supported integrations, removing the need for manual YAML definitions. These downstream exposures are stored in dbt’s metadata system, appear in [catalog](https://docs.getdbt.com/docs/explore/explore-projects), and behave like manual exposures. However, they don’t exist in YAML files.

### Declaring an exposure

Exposures are defined in `.yml` files nested under an `exposures:` key.

The following example shows an exposure definition in a `models/<filename>.yml` file:

.yml'>

```yaml

exposures:

  - name: weekly_jaffle_metrics
    label: Jaffles by the Week
    type: dashboard
    maturity: high
    url: https://bi.tool/dashboards/1
    description: >
      Did someone say "exponential growth"?

    depends_on:
      - ref('fct_orders')
      - ref('dim_customers')
      - source('gsheets', 'goals')
      - metric('count_orders')

    owner:
      name: Callum McData
      email: data@jaffleshop.com
```

### Available properties

_Required:_
- **name**: a unique exposure name written in [snake case](https://en.wikipedia.org/wiki/Snake_case)
- **type**: one of `dashboard`, `notebook`, `analysis`, `ml`, `application` (used to organize in docs site)
- **owner**: `name` or `email` required; additional properties allowed

_Expected:_
- **depends_on**: list of refable nodes, including `metric`, `ref`, and `source`. While possible, it is highly unlikely you will ever need an `exposure` to depend on a `source` directly.

  :::tip
  Do not confuse this `depends_on` YAML property with the [`-- depends_on`](https://docs.getdbt.com/reference/dbt-jinja-functions/statement-blocks#example-using-depends_on) a SQL comment directive defined at the top of a model SQL file, which explicitly adds dependencies to the DAG and ensures the referenced resources are built before the model executes.
  :::

_Optional:_
- **label**:  May contain spaces, capital letters, or special characters.
- **url**:  Activates and populates the link to **View this exposure** in the upper right corner of the generated documentation site
- **maturity**: Indicates the level of confidence or stability in the exposure. One of `high`, `medium`, or `low`. For example, you could use `high` maturity for a well-established dashboard, widely used and trusted within your organization. Use `low` maturity for a new or experimental analysis.

_General properties (optional)_

- [**description**](https://docs.getdbt.com/reference/resource-properties/description)
- [**tags**](https://docs.getdbt.com/reference/resource-configs/tags)
- [**meta**](https://docs.getdbt.com/reference/resource-configs/meta)
- [**enabled**](https://docs.getdbt.com/reference/resource-configs/enabled) &mdash; You can set this property at the exposure level or at the project level in the [`dbt_project.yml`](https://docs.getdbt.com/reference/dbt_project.yml) file.

### Referencing exposures

Once an exposure is defined, you can run commands that reference it:
```
dbt run -s +exposure:weekly_jaffle_report
dbt test -s +exposure:weekly_jaffle_report

```

When we generate the [catalog site](https://docs.getdbt.com/docs/explore/explore-projects), you'll see the exposure appear:

## Related docs

- [Exposure properties](https://docs.getdbt.com/reference/exposure-properties)
- [`exposure:` selection method](https://docs.getdbt.com/reference/node-selection/methods#exposure)
- [Data health tiles](https://docs.getdbt.com/docs/explore/data-tile)
