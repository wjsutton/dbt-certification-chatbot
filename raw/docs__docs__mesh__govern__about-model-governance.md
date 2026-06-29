---
title: "About model governance"
source_url: https://docs.getdbt.com/docs/mesh/govern/about-model-governance
retrieved_via: md-endpoint
fetched: 2026-06-29
---

# About model governance

dbt supports model governance to help you control who can access models, what data they contain, how they change over time, and reference them across projects. dbt supports model governance in dbt Core and the dbt_platform, with some differences in the features available across environments/plans.

- Use model governance to define model structure and visibility in dbt Core and the dbt_platform.
- dbt builds on this with features like [cross-project ref](https://docs.getdbt.com/docs/mesh/govern/project-dependencies) that enable collaboration at scale across multiple projects, powered by its metadata service and [catalog](https://docs.getdbt.com/docs/explore/explore-projects). Available in dbt Enterprise or Enterprise+ plans.

All of the following features are available in dbt Core and the dbt_platform, _except_ project dependencies, which is only available to [dbt Enterprise-tier plans](https://www.getdbt.com/pricing).

- [**Model access**](model-access)  &mdash; Mark models as "public" or "private" to distinguish between mature data products and implementation details — and to control who can `ref` each. 
- [**Model contracts**](model-contracts) &mdash;Guarantee the shape of a model (column names, data types, constraints) before it builds, to prevent surprises for downstream data consumers. 
- [**Model versions**](model-versions) &mdash; When a breaking change is unavoidable, provide a smoother upgrade pathway and deprecation window for downstream data consumers. 
- [**Model namespaces**](https://docs.getdbt.com/reference/dbt-jinja-functions/ref#ref-project-specific-models) &mdash; Organize models into [groups](https://docs.getdbt.com/docs/build/groups) and [packages](https://docs.getdbt.com/docs/build/packages) to delineate ownership boundaries. Models in different packages can share the same name, and the `ref` function can take the project/package namespace as its first argument. 
- [**Project dependencies**](https://docs.getdbt.com/docs/mesh/govern/project-dependencies) &mdash; Resolve references to public models in other projects ("cross-project ref") using an always-on stateful metadata service, instead of importing all models from those projects as packages. Each project serves data products (public model references) while managing its own implementation details, enabling an [enterprise data mesh](https://docs.getdbt.com/best-practices/how-we-mesh/mesh-1-intro).
