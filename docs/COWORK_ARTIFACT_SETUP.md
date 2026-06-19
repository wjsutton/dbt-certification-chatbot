# Run the dbt Cert Coach as a live Cowork artifact

The **dbt Cert Coach** is a single, self-contained HTML app —
[`quiz/generator.html`](../quiz/generator.html) — with four modes (Test, Learn,
Interview, and a full grey **mock-exam simulator**). It runs as a **live
artifact inside Cowork**: question generation, tutoring, and grading all run on
Cowork's built-in AI (`window.cowork.askClaude`), grounded in an embedded
snapshot of the dbt wiki. No server, no database, no API keys.

This guide is for **sharing it with your team** — each teammate registers it as
a live artifact in their own Cowork.

## Why it must run in Cowork

The AI features call `window.cowork.askClaude`, which only exists inside the
Claude desktop app's **Cowork** mode. If you open the file directly in a normal
browser, the UI loads but anything that needs the model (generating a question,
discussing an answer, the end-of-test feedback) stays blank. So the app is run
*inside* Cowork, not as a standalone web page.

## Prerequisites

- The **Claude desktop app** with Cowork mode.
- This repository cloned or downloaded locally.

## Install it (recommended — about 30 seconds)

1. Open the Claude desktop app and start a **Cowork** session.
2. **Connect the `dbt-certification-chatbot` repo folder** (use the folder
   picker / "select a folder" so Cowork can read the files). Connect *only* this
   folder for the install — see the caution below.
3. Paste this prompt:

   > Read `quiz/generator.html` from the **dbt-certification-chatbot** repo and
   > register it as a live Cowork artifact with the id `dbt-question-generator`
   > (call `create_artifact` with that file as `html_path`). Then open it.

> ⚠️ **Only have one copy of `quiz/generator.html`.** If you keep a second copy
> of this project elsewhere (e.g. a separate "Claude Project" folder) and both
> are connected, Claude may read the *older* copy and you'll see a stale UI.
> Connect just the repo, or make sure every copy is in sync, before installing.

4. Claude registers it. **"Dbt Question Generator"** now appears in your Cowork
   artifacts sidebar and reopens any time — it persists across sessions.

That's the whole install. The file is fully self-contained (no external scripts,
no network calls, no connector tools), so nothing else needs to be set up.

## Using it

- Open **Dbt Question Generator** from the artifacts sidebar.
- From the landing page, pick **Test**, **Learn**, **Interview**, or **Mock** —
  or type a topic directly.
- **Test** — pick count, difficulty, and a domain/sub-topic; answer in chat and
  get per-option discussion with links to the dbt docs.
- **Learn** — type any topic (or pick a section/sub-topic); it teaches you in
  chat, then a **Test me on this** button quizzes you on it.
- **Mock** — choose a category and question count, then sit a timed, grey,
  Caveon-style exam with a 1–N question palette; feedback is locked until you
  submit, then you get a domain-by-domain report.
- Dark-mode toggle is top-right; the dbt-logo home button is top-left. Your
  theme choice is remembered.

## Updating to the latest version

When the repo's `quiz/generator.html` changes (new features, or refreshed dbt
content), each teammate re-syncs with:

> Re-read `quiz/generator.html` and update the `dbt-question-generator` artifact
> (call `update_artifact`).

(Re-running the original install prompt also works.)

## Keeping the dbt knowledge current (maintainer note)

The artifact embeds a snapshot of the wiki — the `const SUMMARIES = [...]` block
plus `quiz/exam_meta.json` — so it works offline inside Cowork but is only as
current as its last rebuild. When dbt ships changes:

1. Refresh the corpus and wiki (the existing pipeline):

   ```bash
   pip install -r requirements.txt
   python extract_dbt_docs.py     # refresh raw/ from docs.getdbt.com
   python build_llm_wiki.py       # incremental rebuild; flags stale summaries
   python quiz/validate_bank.py   # grounding gate
   ```

2. Regenerate the artifact's embedded knowledge (the `SUMMARIES` / `EXAM` blocks
   in `quiz/generator.html`) from `wiki/sources/` and `quiz/exam_meta.json`,
   then re-publish with `update_artifact`.

> An automated injector script (template + `wiki/sources/` → rebuilt embed) is a
> sensible next step so this becomes one command. Not yet built — ask if you'd
> like it.

## Troubleshooting

- **Blank where questions/answers should appear, or a message like "Open this
  inside Cowork…":** you're not running inside Cowork, so
  `window.cowork.askClaude` is unavailable. Open the app from the Cowork
  artifacts sidebar — not by double-clicking the file in a browser.
- **Artifact not in the sidebar:** re-run the install prompt and confirm the
  repo folder is connected to the session.
- **Mock questions appear one at a time / slowly:** that's by design — each
  question is written on demand by the AI and cached per slot, so navigating
  back keeps your previous answers.

## What teammates can and can't change

It's one file, safe to copy and reopen. To change the UI, edit
`quiz/generator.html` and re-publish with `update_artifact`. Nothing leaves the
machine except following the dbt documentation links the coach cites.
