# Exam Tester — design & deployment plan

A quiz layer on top of the dbt cert LLM Wiki that generates and delivers practice
questions in the **six exam formats**, grounded in the wiki content and mapped to
the certification's seven domains — replicating the real exam environment.

Real-exam parameters to mirror (from the study guide): **65 questions, 2 hours,
65% to pass, immediate score, mixed item formats, dbt Core 1.11.**

---

## 1. Where it sits

```
raw/ ──► wiki/ (concepts, sources, index)        ← knowledge base (already built)
          │
          ├── dbt_cert_content_mapping.xlsx        ← blueprint: domain → sub-topic → sources
          ▼
quiz/  ── build_question_bank.py  ──► questions.json (item bank, git-tracked, grows)
          │                                    ▲
          schema/item.schema.json              │ cites wiki pages
          player/index.html  ◄─────────────────┘  ← exam player (6 formats, timer, scoring)
          blueprints/exam-65.json                  ← form assembly (counts, weights, format mix)
```

The quiz **reuses the wiki as its source of truth**: every generated item must cite
the wiki source page(s) for its sub-topic. The item bank compounds the same way the
wiki does — generated once, verified, stored, reused, and regenerated only when the
underlying source changes (it reads `wiki/.build-state.json` and the builder's stale
flags, so a changed `raw/` page only invalidates items that cite it).

---

## 2. The six formats (Caveon/Scorpion mechanics → our schema)

| Format | Examinee task | Scoring methods (Scorpion) | Our key fields |
|--------|---------------|----------------------------|----------------|
| **Multiple choice** | pick one *or more* correct options | default (all-or-nothing), partial, cutscore, weighted; *select-all-that-apply* + *selection limit* | `options[].correct`, `select_all`, `selection_limit` |
| **Fill-in-the-blank** | type / pick into blanks (short-answer or dropdown) | default, manual, partial, cutscore, weighted (per blank) | `blanks[]` = `dropdown(options)` or `short_answer(accepted[])` |
| **Matching** | pair two sets of data | default, partial, cutscore, weighted | `left[]`, `right[]`, `key{}`, optional extra `right` distractors |
| **Hotspot** | click the correct spot(s) on an image | default, partial, cutscore, weighted; *number of selections* | `image`, `regions[]`, `correct_regions`, `num_selections` |
| **Build list** | sort/sequence options into the correct order | default, manual, weighted | `items[]` ordered key; optional distractors; per-position credit |
| **DOMC** | options shown **one at a time** with YES/NO | any single wrong YES/NO ⇒ item incorrect; forward-only (no review) | `options[].correct`, `present_n`, `super` (oversample), `unscored_after` |

Notes that affect the engine:
- **Option order**: random / fixed / length / alphabetical (most formats).
- **Enemies**: never place two items that give away each other's answers on the same
  form — model as an `enemies: [item_id]` list and enforce at form assembly.
- **DOMC specifics**: present options randomly one-by-one; stop as soon as the item is
  decided; *forward-only* (cannot revisit, except un-answered items may be marked for
  later); SUPER-DOMC oversamples correct/incorrect options so items rarely repeat;
  optional non-scored options after scoring to avoid leaking the key.

---

## 3. Normalized item schema (one shape for all formats)

```jsonc
{
  "id": "d07-state-mcq-001",
  "domain": "07 — Leveraging the dbt state",
  "subtopic": "Understanding state & state selection",
  "format": "mcq",                         // mcq | fitb | matching | hotspot | build_list | domc
  "difficulty": "medium",                  // easy | medium | hard
  "stem": "…markdown question text…",
  "scoring": { "method": "default", "points": 1 },
  "options": [ … ],                        // format-specific (see §2)
  "answer":  { … },                        // format-specific key
  "rationale": "why the key is correct, in exam-accurate dbt terms",
  "citations": [
    { "title": "About local state in dbt", "wiki": "wiki/sources/state-selection.md",
      "url": "https://docs.getdbt.com/reference/node-selection/state-selection" }
  ],
  "version_target": "dbt-core-1.11",
  "provenance": { "generated": "2026-06-12", "source_hash": "…", "verified": true }
}
```

`source_hash` is the hash of the cited `raw/` file at generation time → lets the bank
detect **stale items** when a source changes (same mechanism as the wiki builder).

### Worked examples (grounded in the already-ingested Domain 07 content)

**MCQ (select-all):**
```jsonc
{ "format": "mcq", "subtopic": "Understanding state & state selection",
  "stem": "Which selectors require a comparison manifest passed via `--state`? (Select all that apply.)",
  "options": [
    {"id":"a","text":"state:modified","correct":true},
    {"id":"b","text":"result:fail","correct":true},
    {"id":"c","text":"tag:nightly","correct":false},
    {"id":"d","text":"source_status:fresher","correct":true},
    {"id":"e","text":"config.materialized:incremental","correct":false}],
  "scoring":{"method":"default"},
  "rationale":"state:, result:, and source_status: compare against prior artifacts; tag/config read the current project.",
  "citations":[{"wiki":"wiki/sources/methods.md"}] }
```

**Fill-in-the-blank (dropdown + short answer):**
```jsonc
{ "format":"fitb", "subtopic":"Understanding state & state selection",
  "stem":"To run only changed models against production, use `dbt run --select \"{{b1}}\" --state {{b2}}`.",
  "blanks":[
    {"id":"b1","type":"dropdown","options":["state:modified","state:old","result:error"],"answer":"state:modified"},
    {"id":"b2","type":"short_answer","accepted":["path/to/artifacts","path/to/prod/artifacts"]}],
  "citations":[{"wiki":"wiki/sources/state-selection.md"}] }
```

**Build list (ordering — Slim CI):**
```jsonc
{ "format":"build_list", "subtopic":"Understanding state & state selection",
  "stem":"Order the steps of a Slim CI run.",
  "items":[
    {"id":"1","text":"Retrieve production manifest as state"},
    {"id":"2","text":"Select state:modified to find changed models"},
    {"id":"3","text":"--defer unbuilt parents to production"},
    {"id":"4","text":"Build & test only the modified subset"}],
  "answer":{"order":["1","2","3","4"]},
  "scoring":{"method":"weighted"},
  "citations":[{"wiki":"wiki/sources/defer.md"},{"wiki":"wiki/sources/state-selection.md"}] }
```

**DOMC:**
```jsonc
{ "format":"domc", "subtopic":"Using dbt retry",
  "stem":"Is the statement a TRUE property of `dbt retry`?",
  "options":[
    {"text":"Resumes from the point of failure using run_results.json","correct":true},
    {"text":"Re-runs all upstream dependencies from scratch","correct":false},
    {"text":"Is a no-op after a fully successful run","correct":true},
    {"text":"Lets you override --select on retry in dbt Core","correct":false}],
  "present_n":2, "unscored_after":1,
  "rationale":"retry reads run_results.json and resumes failed/skipped nodes; selection is inherited in Core.",
  "citations":[{"wiki":"wiki/sources/retry.md"}] }
```

(Matching and Hotspot follow the §2 fields. For a code cert, *hotspot* works well as a
rendered code block / DAG image where the examinee clicks the offending line or the
correct node — `regions[]` are rectangles over the image.)

---

## 4. Generation pipeline (grounded + verified)

`build_question_bank.py` mirrors the wiki's Ingest/Lint discipline:

1. **Select** a `(sub-topic, format, difficulty)` target from the blueprint.
2. **Retrieve** the cited wiki context — concept synthesis + `sources/<seg>.md` + `raw/`
   — via `index.md` (no embeddings needed at this scale).
3. **Generate** one item in the schema, constrained to the retrieved content and required
   to use **exact dbt tokens** (`--empty`, `state:modified`, `grants`, …).
4. **Verify** (separate critic pass + rule checks): the key is supported by a citation;
   distractors are wrong-but-plausible; JSON is schema-valid; no ambiguity; difficulty
   tagged; version is 1.11. Reject → regenerate on failure.
5. **Store** with provenance + `source_hash`. Items accumulate; the bank is git-tracked.

**Incremental regeneration:** when the wiki builder flags a source as changed/stale,
only the items whose `source_hash` no longer matches are re-generated/re-verified —
the rest are untouched, exactly like the page builder.

---

## 5. Exam-mode delivery

- **Form assembly** from `blueprints/exam-65.json`: 65 items (configurable), sampled
  across the 7 domains by weight, mixed formats, no repeats, enemies excluded.
  - Domain weighting: the official per-domain weights aren't published, so default to
    *proportional to sub-topic count* (Domain 01 is by far the largest), with an override
    file so you can tune toward observed exam emphasis.
- **Timer & scoring**: 2-hour countdown; per-format scoring matching Scorpion semantics;
  pass at ≥ 65%; score shown immediately on submit.
- **Two modes**: *Practice* (instant per-item feedback + citation links back into the wiki)
  and *Exam* (locked until submit). **DOMC is always forward-only.**
- **Review screen**: after submit, list each item with the correct key, the `rationale`,
  and a link to the citing wiki page — so wrong answers drive study back into the wiki.

---

## 6. Deployment options

| Option | What | Pros | Cons |
|--------|------|------|------|
| **A. Single-file HTML player** | static `index.html` loads `questions.json`, runs fully client-side | zero infra, shareable, offline, fast to ship | bank is static until regenerated |
| **B. Cowork live artifact** | a `create_artifact` page that calls an LLM at runtime to generate fresh, wiki-grounded items | infinite non-repeating items, always current | needs runtime LLM calls |
| **C. Generator + versioned bank + player** | `build_question_bank.py` produces/validates `questions.json` from the wiki; player delivers it; CI regenerates on wiki change | reproducible, auditable, compounding bank, ties into incremental build | most setup |

**Recommendation:** build **C's generator + bank** and ship the **A player** first; add **B**
later for endless fresh items. The generator and player share `schema/item.schema.json`,
so the bank stays portable across all three.

---

## 7. Suggested MVP (proves the pipeline end-to-end)

1. `schema/item.schema.json` — the six-format schema above (+ a JSON-Schema validator).
2. A hand-verified **seed bank for Domain 07** (fully ingested): ~12 items spanning
   MCQ, FITB, build-list, and DOMC, each citing a `wiki/sources/*` page.
3. `player/index.html` — single-file player supporting those four formats, with timer,
   scoring, and a citation-linked review screen (matching + hotspot added next).
4. `build_question_bank.py` — generator + verifier; wire it to the wiki index and the
   stale-flag mechanism.
5. `blueprints/exam-65.json` — domain weights + format mix for a full mock exam.

Domain 07 is the natural first target because it's already fully ingested, so the seed
bank is genuinely grounded today.

---

## 8. Quality & maintenance

- **Grounding gate**: no item ships without a wiki citation; ungrounded items are rejected.
- **Item lint** (mirrors the wiki lint): flag stale items (cited source changed),
  contradictory keys, ambiguous stems, and **version drift** (must be dbt Core 1.11).
- **Calibration**: track per-item performance to refine `difficulty` over time.
- **Coverage report**: cross-check the bank against the mapping spreadsheet so every
  sub-topic has items in several formats.
