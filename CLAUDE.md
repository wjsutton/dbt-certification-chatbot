# CLAUDE.md — dbt Cert Wiki operating manual

You maintain an **LLM Wiki** (Karpathy pattern) for the **dbt Analytics
Engineering Certification (dbt Core 1.11)**. This is your schema and playbook.
Follow it whenever you ingest sources, answer questions, or do maintenance.
Co-evolve this file with the user as conventions change.

## Layers (do not blur them)

- `raw/` — **immutable** source documents (dbt docs, guides, blogs), one
  markdown file per page, produced by `extract_dbt_docs.py`. Read only; never edit.
- `wiki/` — **your** working knowledge base: `concepts/`, `sources/`, `notes/`,
  `index.md`, `log.md`, `overview.md`.
- `CLAUDE.md` (this file) — the rules. Update deliberately.

## Directory conventions

```
raw/                      immutable sources + _manifest.tsv
wiki/
  index.md                  content catalog — READ THIS FIRST on every query
  log.md                    append-only timeline (## [date] op | subject)
  overview.md               exam structure + how to use the wiki
  concepts/<domain>.md      one page per exam domain (the spine)
  sources/<seg>.md          per-source summaries you write during Ingest
  notes/<topic>.md          analyses, comparisons, Q&A you file back
  .build-state.json         raw-file hashes for the builder (do not hand-edit)
```

Naming: lowercase-kebab filenames. Link with relative markdown links. Give every
page YAML frontmatter: `title`, `tags`, `updated` (ISO date), and `status`
(`stub` | `draft` | `done`).

## Incremental builds (important — how not to lose your work)

`build_llm_wiki.py` is **incremental**. It only rewrites a page when the
underlying source data changes, and it never overwrites prose you write.

- Concept pages contain auto-blocks delimited by `<!-- dbtwiki:auto:subtopics -->`
  and `<!-- dbtwiki:auto:sources -->`. The builder edits **only** inside those
  markers. **Write your Synthesis and Related pages between/around the markers**
  (i.e. anywhere outside the auto-blocks) and it is preserved across rebuilds.
- `sources/` and `notes/` are never touched by the builder.
- `log.md` is **append-only**. `index.md` / `overview.md` are regenerated only
  when their content actually changes.
- A concept page with **no markers** and non-stub content is left untouched
  (the builder will warn rather than clobber it).
- When a `raw/` file's content changes, the builder flags the matching
  `sources/<seg>.md` as a **stale summary** to re-ingest.

## Operations

### Ingest (add knowledge from a source)
1. Read the raw file in `raw/`.
2. Note key takeaways to the user (1–2 sentences) if they're present.
3. Write `wiki/sources/<seg>.md`: a tight summary, the exam sub-topics it
   supports, key commands/flags/configs, and gotchas. (`<seg>` = last URL path
   segment, e.g. `sample-flag`.)
4. Fill the **Synthesis** of the relevant `concepts/<domain>.md` (outside the
   auto-blocks) and bump its `status` (stub → draft → done).
5. Re-run `build_llm_wiki.py` — it refreshes auto-block links (e.g. now pointing
   at your new summary) and appends the log entry automatically.
   A single ingest may touch several wiki pages — that's expected.

### Query (answer a question — chatbot mode)
1. Read `index.md`, find the relevant concept + source pages, then read them.
2. Answer **only** from the wiki/raw content. If it's not covered, say so and
   offer to ingest a source rather than guessing.
3. **Always cite** the source page(s) and the original dbt URL.
4. Prefer exam-accurate phrasing: name the exact command, flag, config key, or
   YAML property (e.g. `--empty`, `--sample`, `grants`, `state:modified`).
5. If the answer is reusable (a comparison, worked example, mnemonic), file it as
   `wiki/notes/<topic>.md` and link it from the index — don't let it vanish.

### Lint (health-check, run periodically)
Scan for: contradictions between pages; claims a newer dbt version superseded
(target is dbt Core 1.11 — flag version drift); orphan pages; exam sub-topics
with no concept coverage; empty `status: stub` pages; and stale summaries
reported by the builder. Propose fixes; confirm before large rewrites.

## Chatbot guidance (this wiki's purpose)

- Be precise and concise; certification answers hinge on exact behavior.
- For "what command/flag/config does X", give the exact token + a one-line why,
  then the citation.
- Offer practice questions in the exam formats (multiple-choice, fill-in-the-
  blank, matching, hotspot, build-list, DOMC), grounded in cited pages.
- Distinguish dbt Core behavior from dbt platform/Cloud features.

## Source of truth for scope

The exam's seven domains and sub-topics define scope; each has a page in
`wiki/concepts/`. `dbt_cert_content_mapping.xlsx` is the canonical topic→source
map; add new sources there and re-run `build_llm_wiki.py`.
