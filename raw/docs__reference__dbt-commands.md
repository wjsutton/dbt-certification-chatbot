---
title: "dbt Command reference"
source_url: https://docs.getdbt.com/reference/dbt-commands
retrieved_via: md-endpoint
fetched: 2026-06-29
---

# dbt Command reference

You can run dbt using the following tools:

- In your browser with the [studio_ide](https://docs.getdbt.com/docs/platform/studio-ide/develop-in-studio)
- On the command line interface using the [platform_cli](https://docs.getdbt.com/docs/platform/dbt-cli-installation) or open-source [core](https://docs.getdbt.com/docs/local/install-dbt).

A key distinction is that platform_cli and studio_ide are designed to support safe parallel execution of dbt commands, leveraging dbt_platform's infrastructure and its comprehensive [features](https://docs.getdbt.com/docs/platform/about-platform/dbt-platform-features). In contrast, core _doesn't support_ safe parallel execution for multiple invocations in the same process. Learn more in the [parallel execution](#parallel-execution) section.

## Parallel execution

dbt_platform allows for concurrent execution of commands, enhancing efficiency without compromising data integrity. This enables you to run multiple commands at the same time. However, it's important to understand which commands can be run in parallel and which can't.

In contrast, [`dbt-core` _doesn't_ support](https://docs.getdbt.com/reference/programmatic-invocations#parallel-execution-not-supported) safe parallel execution for multiple invocations in the same process, and requires users to manage concurrency manually to ensure data integrity and system stability.

To ensure your dbt workflows are both efficient and safe, you can run different types of dbt commands in parallel &mdash; for example, `dbt build` (write operation) can safely run alongside `dbt parse` (read operation). However, you can't run `dbt build` and `dbt run` (both write operations) in parallel.

dbt commands can be `read` or `write` commands:

| Command type | Description | Example |
|------|-------------|---------|
| **Write** | These commands perform actions that change data or metadata in your data platform.<br /><br /> Limited to one invocation at any given time, which prevents any potential conflicts, such as overwriting the same table in your data platform at the same time. | `dbt build`<br />`dbt run` |
| **Read** | These commands involve operations that fetch or read data without making any changes to your data platform.<br /><br /> Can have multiple invocations in parallel and aren't limited to one invocation at any given time. This means read commands can run in parallel with other read commands and a single write command.| `dbt parse`<br />`dbt compile`|

## Available commands

The following sections outline the commands supported by dbt and their relevant flags. They are available in all tools and all [supported versions](https://docs.getdbt.com/docs/dbt-versions) unless noted otherwise. You can run these commands in your specific tool by prefixing them with `dbt` &mdash; for example, to run the `test` command, type `dbt test`.

You can also call these commands and flags programmatically using `dbtRunner.invoke`. For details, refer to [Programmatic invocations](https://docs.getdbt.com/reference/programmatic-invocations).

For information about selecting models on the command line, refer to [Model selection syntax](https://docs.getdbt.com/reference/node-selection/syntax).

Commands marked ❌ indicate write commands, commands marked ✅ indicate read commands, and commands marked N/A indicate that parallel execution isn't relevant for that command.

> **Info**
>
> Some commands are not yet supported in the fusion_engine or have limited functionality. Refer to the [Fusion supported features](https://docs.getdbt.com/docs/fusion/supported-features) page for details.

| Command | Description | Parallel execution |  Caveats |
|---------|-------------| :-----------------:| ------------------------------------------ |
| [build](https://docs.getdbt.com/reference/commands/build) | Builds and tests all selected resources (models, seeds, tests, and more) |  ❌ | All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) | 
| cancel | Cancels the most recent invocation. | N/A | platform_cli <br /> Requires [dbt v1.6 or higher](https://docs.getdbt.com/docs/dbt-versions) |
| [clean](https://docs.getdbt.com/reference/commands/clean) | Deletes artifacts present in the dbt project |  ✅ | All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [clone](https://docs.getdbt.com/reference/commands/clone) | Clones selected models from the specified state |  ❌ | All tools <br /> Requires [dbt v1.6 or higher](https://docs.getdbt.com/docs/dbt-versions) |
| [compile](https://docs.getdbt.com/reference/commands/compile) | Compiles (but does not run) the models in a project |  ✅ | All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [debug](https://docs.getdbt.com/reference/commands/debug) | Debugs dbt connections and projects | ✅ | All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [deps](https://docs.getdbt.com/reference/commands/deps) | Downloads dependencies for a project |  ✅ |  All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [docs](https://docs.getdbt.com/reference/commands/cmd-docs) | Generates documentation for a project |   ✅ | All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [environment](https://docs.getdbt.com/reference/commands/dbt-environment) | Enables you to interact with your dbt_platform environment. |   N/A | platform_cli <br /> Requires [dbt v1.5 or higher](https://docs.getdbt.com/docs/dbt-versions) |
| help | Displays help information for any command | N/A | core, platform_cli <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [init](https://docs.getdbt.com/reference/commands/init) | Initializes a new dbt project |   ✅ | fusion <br /> core<br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [invocation](https://docs.getdbt.com/reference/commands/invocation) | Enables users to debug long-running sessions by interacting with active invocations.|  N/A | platform_cli <br /> Requires [dbt v1.5 or higher](https://docs.getdbt.com/docs/dbt-versions) |
| [lint](https://docs.getdbt.com/reference/commands/lint) | Lints SQL files in a project for style, correctness, and convention violations | ✅ | Requires dbt_platform project on fusion |
| [list](https://docs.getdbt.com/reference/commands/list) | Lists resources defined in a dbt project |  ✅ | All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [login](https://docs.getdbt.com/reference/commands/login) | Logs in to your dbt_platform account | N/A | core v2.0 and later <br /> platform_cli |
| [parse](https://docs.getdbt.com/reference/commands/parse) | Parses a project and writes detailed timing info |  ✅ | All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| reattach | Reattaches to the most recent invocation to retrieve logs and artifacts. |   N/A | platform_cli <br /> Requires [dbt v1.6 or higher](https://docs.getdbt.com/docs/dbt-versions) |
| [retry](https://docs.getdbt.com/reference/commands/retry) | Retry the last run `dbt` command from the point of failure |  ✅ | All tools <br /> Requires [dbt v1.6 or higher](https://docs.getdbt.com/docs/dbt-versions) |
| [run](https://docs.getdbt.com/reference/commands/run) | Runs the models in a project |   ❌ | All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [run-operation](https://docs.getdbt.com/reference/commands/run-operation) | Invokes a macro, including running arbitrary maintenance SQL against the database | ❌ | All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [seed](https://docs.getdbt.com/reference/commands/seed) | Loads CSV files into the database |  ❌ | All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [show](https://docs.getdbt.com/reference/commands/show) | Previews table rows post-transformation | ✅ |  All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [snapshot](https://docs.getdbt.com/reference/commands/snapshot) | Executes "snapshot" jobs defined in a project |  ❌ | All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [source](https://docs.getdbt.com/reference/commands/source) | Provides tools for working with source data (including validating that sources are "fresh") | ✅ | All tools<br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) |
| [test](https://docs.getdbt.com/reference/commands/test) | Executes tests defined in a project  |  ✅ | All tools <br /> All [supported versions](https://docs.getdbt.com/docs/dbt-versions) <br /> fusion flag `--warn-error` not yet supported  |
| [`wizard`](https://docs.getdbt.com/docs/dbt-ai/wizard-cli-reference) | Starts an agentic dbt development session with wizard from the command line | N/A | Local development <br />  [All supported versions](https://docs.getdbt.com/docs/dbt-versions) |

Note, use the [`--version`](https://docs.getdbt.com/reference/commands/version) flag to display the installed core or platform_cli version. (Not applicable for the studio_ide). Available on all [supported versions](https://docs.getdbt.com/docs/dbt-versions).
