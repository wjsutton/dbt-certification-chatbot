# dbt Certification Coach

A grounded, self-updating study system for the **dbt Analytics Engineering
Certification (dbt Core 1.11)**. It turns the official dbt docs into a
maintained knowledge wiki and serves exam-style practice — via a static player,
a chat generator, or an **MCP server** your teammates connect to and get quizzed.

```
raw/        immutable dbt-doc excerpts (one md per page) + _manifest.tsv
wiki/       LLM-maintained knowledge base (concepts/, sources/, index, log)
quiz/       schema, question bank, blueprint, player, generator, validators
mcp/        the dbt-cert-coach MCP server (generation-first, grounded)
scripts     extract_dbt_docs.py (corpus) · build_llm_wiki.py (incremental wiki)
.github/    CI: validate (grounding gate) + refresh (weekly doc update → PR)
CLAUDE.md   operating manual for the LLM wiki maintainer
PRD.md      product requirements
```

## Four ways to use it

1. **Live Cowork artifact (recommended for the team).** `quiz/generator.html` is
   a single self-contained app — Test, Learn, Interview, and a full timed,
   Caveon-style **mock-exam simulator** — that runs as a live artifact inside the
   Claude desktop app's Cowork mode. Generation, tutoring, and grading run on
   `window.cowork.askClaude`, grounded in the embedded wiki; no server or keys.
   Each teammate registers it once in their own Cowork — see
   [`docs/COWORK_ARTIFACT_SETUP.md`](docs/COWORK_ARTIFACT_SETUP.md).
2. **MCP coach.** Connect an MCP client and be quizzed conversationally — fresh
   questions generated on demand, grounded in the wiki. See
   [`mcp/README.md`](mcp/README.md). Try: *"generate an uber-hard question on
   `dbt parse`"*, *"interview me to find my gaps"*, *"certification overview"*.
3. **Static exam player.** Open `quiz/player/index.html` (serve the repo:
   `python -m http.server` → `/quiz/player/`) to take the curated 66-question
   mock in real exam formats with timer + scoring.
4. **Chat generator (raw file).** `quiz/generator.html` opened directly — UI
   only; the AI features need Cowork (option 1).

## Keeping it current (the pipeline)

dbt ships often; the corpus stays fresh without hand-maintenance:

```bash
pip install -r requirements.txt
python extract_dbt_docs.py     # refresh raw/ from docs.getdbt.com
python build_llm_wiki.py       # incremental: only changed pages rewritten; flags stale summaries
python quiz/validate_bank.py   # grounding gate — every item must cite a real source
```

CI runs the grounding gate on every PR (`.github/workflows/validate.yml`) and a
**weekly refresh** that re-extracts, rebuilds, and opens a review PR with a
change report (`.github/workflows/refresh.yml`). Bump the dbt version by
retargeting `version_target` and re-running the pipeline.

## Principles
- **Grounded:** no question ships without a citation to a `wiki/`/`raw/` source.
- **Version-pinned:** dbt Core 1.11 (single switch to retarget).
- **Incremental & idempotent:** the builder only rewrites what changed and never
  clobbers human-written synthesis (marker blocks).

---
Study content is excerpted from dbt Labs documentation — see [`NOTICE`](NOTICE). Internal use.
