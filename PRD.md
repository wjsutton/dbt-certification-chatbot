# PRD — dbt Certification Coach (repo + MCP quiz tool + refresh pipeline)

**Author:** Will Sutton · **Status:** Draft v1 · **Date:** 2026-06-12
**One-liner:** Package the existing dbt cert knowledge base and quiz engine as a versioned GitHub repo that any teammate can clone *or* connect to as an MCP tool to be quizzed on the dbt Analytics Engineering Certification (dbt Core 1.11), with a pipeline that keeps the underlying docs current as dbt evolves.

---

## 1. Summary

We have built a working, grounded study system for the dbt Analytics Engineering Certification: an immutable corpus of dbt docs (`raw/`), an LLM-maintained wiki (`wiki/`), a validated 66-question bank (`quiz/`), an exam-style player, and a chat-style question generator. This PRD scopes turning that into a **shared team product**:

1. A clean, documented **GitHub repository** as the single source of truth.
2. An **MCP server** ("dbt-cert-coach") teammates connect to from Claude/Cursor/etc. to be quizzed conversationally — random questions, topic drills, adaptive interviews, and a certification overview.
3. A **content refresh pipeline** (CI) that re-extracts dbt docs, detects changes, flags stale summaries/questions, and opens a review PR — so the material tracks new dbt releases.

## 2. Problem & motivation

- Several team members are preparing for the dbt cert; study material is scattered and not exam-shaped.
- Generic LLM quizzing hallucinates and drifts from the current dbt version.
- dbt ships frequently (e.g. 1.11 → next); static study notes rot. We need a maintainable, **grounded** (cited, version-pinned) system that updates with minimal effort.

## 3. Goals & non-goals

**Goals**
- G1 — One `git clone` gives a teammate the full corpus, bank, player, and tooling.
- G2 — A teammate can connect an MCP client and be quizzed without cloning or local setup beyond client config.
- G3 — Every question is **grounded** (cites a wiki/raw source) and **version-pinned** to dbt Core 1.11 (configurable).
- G4 — A scheduled/manual pipeline refreshes docs from dbt, surfaces what changed, and gates updates behind validation + human review.
- G5 — Track each user's weak domains to drive adaptive practice (the "interview me / find gaps" flow).

**Non-goals**
- Not a proctored/real exam; no integration with Caveon/Talview.
- Not a public product; internal team use (private repo).
- No warehouse connection or running dbt itself — this is study content only.

## 4. Users & use cases

| Persona | Need | Entry point |
|---|---|---|
| **Exam candidate** | Practice in exam formats; find & close gaps | MCP chat or local player |
| **Reviewer / maintainer** | Keep content correct & current; approve refresh PRs | Repo + CI |
| **Team lead** | See readiness across the team | Progress export (stretch) |

Core use cases: "give me a random certification question", "quiz me on snapshots / uber-hard", "interview me to identify gaps", "give me an overview of the exam", "explain `state:modified`".

## 5. Current state (what already exists — reuse, don't rebuild)

- `extract_dbt_docs.py` — fetches & cleans 57 dbt sources → `raw/` (+ `_manifest.tsv`).
- `build_llm_wiki.py` — **incremental** builder of `wiki/` (concepts, sources, index, log); preserves human prose via marker blocks; tracks raw-file hashes in `.build-state.json` and flags **stale summaries**.
- `dbt_cert_content_mapping.xlsx` — canonical exam-topic → source map.
- `CLAUDE.md` — operating manual (Ingest / Query / Lint) for the LLM maintainer.
- `wiki/` — 7 concept pages (all `status: done`) + 56 source summaries.
- `quiz/` — `schema/item.schema.json`, `questions.json` (66 grounded items), `blueprints/exam-65.json`, `player/index.html`, `validate_bank.py` (schema + grounding gate), `coverage.py`, `generator.html`, `README.md`.
- Cowork artifact "dbt-question-generator" — chat coach (random / interview / overview) with all six exam-format renderers incl. hot-spot.

## 6. Proposed solution

Three coordinated deliverables on top of the current assets.

### 6.1 Repository (`dbt-cert-coach`)
A private GitHub repo, MIT-or-internal-licensed, with a clear README, the corpus, the bank, the tooling, CI, and the MCP server. Static player and generator are openable straight from a clone (or GitHub Pages, internal).

### 6.2 MCP server ("dbt-cert-coach")
A small Python MCP server (FastMCP / official MCP SDK) that loads `quiz/questions.json` + `wiki/sources/*` at startup and exposes tools teammates call from any MCP client (Claude Desktop, Cursor, Cowork). Two grounding modes: **served** (pull a vetted item from the bank — default, zero hallucination) and **generated** (LLM writes a fresh item grounded in retrieved summaries — for infinite practice).

**Tools (v1):**
- `get_random_question(domain?, difficulty?, format?)` → vetted item from the bank.
- `get_question_on(topic, difficulty?, format?, mode="served|generated")` → grounded item.
- `grade_answer(question_id, answer)` → correct/incorrect + per-blank/partial score + rationale + citation.
- `start_interview(length=8)` / `interview_next()` / `interview_finish()` → adaptive session; returns per-domain gap report.
- `exam_overview()` → logistics + the six question types + domain weighting.
- `search_wiki(query, k=4)` → grounded snippets (tutor/explain).
- `list_domains()` / `coverage()` → catalog + bank coverage.

Transport: **stdio** for local clients (pip/uvx install) in v1; optional **streamable-HTTP remote** (one shared internal URL) in v2. Session state (interview progress, per-user scores) kept per-connection; optional persistence in v2.

### 6.3 Content refresh pipeline (CI)
GitHub Actions, scheduled (weekly) + manual `workflow_dispatch`:
1. `pip install -r requirements.txt`
2. `python extract_dbt_docs.py` (network to docs.getdbt.com) → updates `raw/`.
3. `python build_llm_wiki.py` → refreshes `wiki/`, recomputes hashes, emits **stale-summary** + **changed-source** report.
4. `python quiz/validate_bank.py` → grounding gate (fails CI on any ungrounded/broken item).
5. `python quiz/coverage.py` → coverage report (artifact).
6. If anything changed → open a **PR** with the diff + a generated changelog ("these sources changed; these summaries/questions may be stale") for human review.
7. *(Optional, gated)* an LLM job (Claude) re-ingests stale summaries and proposes question updates **as PR suggestions only** — never auto-merged; `validate_bank.py` must pass.

Version bumps (e.g. dbt 1.11 → 1.12) are handled by updating the target version in `CLAUDE.md` + `version_target` policy and re-running the pipeline; the `--empty`/version-block handling already prefers the targeted release.

## 7. Functional requirements

- FR1 The MCP server returns a question matching requested `domain`/`difficulty`/`format` when available; otherwise nearest match with a note.
- FR2 Served questions come verbatim from `questions.json`; generated questions must include ≥1 citation to an existing `wiki/`-or-`raw/` file (reject otherwise).
- FR3 `grade_answer` implements the same scoring as the player (MCQ select-all, FITB per-blank, matching, ordered build-list, DOMC any-wrong-fails, hot-spot region match).
- FR4 Interview mode samples across all 7 domains, scores, and returns weakest domains + recommended sub-topics + links.
- FR5 CI fails on: ungrounded items, schema violations, or `version_target` drift.
- FR6 Refresh PR clearly lists changed sources and the summaries/questions that cite them.
- FR7 Local player + generator run from a clone with no build step (static HTML); generator's live mode degrades gracefully outside an LLM host.

## 8. Non-functional requirements

- **Grounded & cited** — no item ships without a source; grounding gate enforced in CI.
- **Version-pinned** — default dbt Core 1.11; single switch to retarget.
- **Reproducible** — pinned `requirements.txt`; deterministic builder (idempotent, no-op when unchanged).
- **Low-maintenance** — refresh is one workflow; human only reviews diffs.
- **Secure** — private repo; no secrets in content; if an LLM CI step is enabled, the API key is a repo secret. MCP server is read-only over local files; remote mode behind SSO/VPN.
- **Licensing** — dbt docs are dbt Labs' content; store as study excerpts with source links; keep repo internal. Add a NOTICE describing source + attribution before any external sharing.

## 9. Repository structure (proposed)

```
dbt-cert-coach/
  README.md                 quickstart (clone / connect MCP / run player)
  CLAUDE.md                 LLM maintainer playbook
  PRD.md                    this document
  requirements.txt
  dbt_cert_content_mapping.xlsx
  extract_dbt_docs.py
  build_llm_wiki.py
  raw/                      immutable sources + _manifest.tsv
  wiki/                     concepts/ sources/ notes/ index.md overview.md log.md
  quiz/
    schema/item.schema.json
    questions.json
    blueprints/exam-65.json
    player/index.html
    generator.html
    validate_bank.py  coverage.py  README.md
  mcp/
    server.py               the dbt-cert-coach MCP server
    README.md               client config (Claude Desktop / Cursor / Cowork)
  .github/workflows/
    refresh.yml             scheduled doc refresh → PR
    validate.yml            PR gate: validate_bank + coverage
  docs/EXAM_TESTER_DESIGN.md
```

## 10. Milestones

- **M0 — Repo cut (0.5 day):** move assets in, write README + requirements, add `validate.yml` (grounding gate on PRs). Outcome: clone-and-study works today.
- **M1 — MCP server v1 (2–3 days):** stdio server with served-bank tools (random/topic/grade/overview/interview/search). Client config docs. Outcome: teammates connect and get quizzed.
- **M2 — Refresh pipeline (1–2 days):** `refresh.yml` runs extractor+builder+validate, opens PR with change report. Outcome: docs stay current with review.
- **M3 — Generated mode + coverage to 65 (2–3 days):** generated questions behind the grounding gate; grow bank toward the 65-per-exam blueprint in thin domains.
- **M4 (stretch) — Remote MCP + progress tracking:** shared hosted endpoint; per-user readiness export for the team lead.

## 11. Success metrics

- ≥ N teammates connected and completing ≥1 interview/week.
- Refresh pipeline runs green weekly; median reviewer time per refresh PR < 15 min.
- 0 ungrounded items in `main` (CI-enforced).
- Bank coverage: ≥3 items per exam sub-topic across ≥4 formats.
- Self-reported readiness ↑ and (eventually) pass rate of teammates who used it.

## 12. Risks & mitigations

| Risk | Mitigation |
|---|---|
| dbt restructures docs / URLs (404s, like the materializations `.md`) | Extractor has HTML fallback; refresh PR surfaces failures for a human to fix the mapping. |
| Generated questions are wrong/ambiguous | Default to **served** bank; generated items are review-only and must pass the grounding gate. |
| Content licensing if shared externally | Keep repo private; NOTICE + source links; treat as excerpts. |
| Version drift (1.11 → next) | `version_target` policy + single retarget switch + pipeline re-run. |
| LLM-in-CI cost/secret management | Optional, off by default; key as repo secret; human-gated PRs. |
| MCP host differences | v1 stdio (broadest support); document Claude Desktop/Cursor/Cowork configs. |

## 13. Open questions / decisions

1. **MCP transport for v1** — local stdio (recommended) vs hosted remote? (Affects auth & infra.)
2. **Generated questions** — enable the LLM-in-CI re-ingest step, or keep all authoring human/Claude-in-session?
3. **Progress tracking** — ephemeral per-session, or persist per-user scores (where: repo, a small DB, or none)?
4. **Hosting the player** — clone-only, or internal GitHub Pages?
5. **Repo visibility & licensing** — confirm private + attribution approach for dbt content.
6. **Refresh cadence** — weekly cron vs on dbt-release webhook.

## 14. Appendix — MCP tool sketch (server.py, v1)

```python
# pip install "mcp[cli]"  (official Python SDK / FastMCP)
from mcp.server.fastmcp import FastMCP
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
BANK = json.loads((ROOT/"quiz/questions.json").read_text())["items"]
mcp = FastMCP("dbt-cert-coach")

@mcp.tool()
def get_random_question(domain: str = "", difficulty: str = "", format: str = "") -> dict:
    """Return a vetted, source-cited practice question from the bank."""
    ...

@mcp.tool()
def grade_answer(question_id: str, answer: dict) -> dict:
    """Score an answer (same rules as the player) with rationale + citation."""
    ...

@mcp.tool()
def exam_overview() -> dict:
    """Logistics, the six question types, and domain weighting."""
    ...

if __name__ == "__main__":
    mcp.run()   # stdio
```

Client config (e.g. Claude Desktop): add a `dbt-cert-coach` server pointing at `python mcp/server.py` (or `uvx` the published package).
