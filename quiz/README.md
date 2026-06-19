# Quiz layer — dbt cert exam practice

A practice-exam tester grounded in the wiki. Every question cites a `wiki/` or
`raw/` source page, and the validator refuses ungrounded items.

## Files
- `schema/item.schema.json` — the item schema for all six formats.
- `questions.json` — the question bank (grows over time; git-tracked).
- `blueprints/exam-65.json` — full mock-exam form (domain weights, format mix, 65 Q / 120 min / 65% pass).
- `player/index.html` — single-file exam player (MCQ, fill-in-the-blank, matching, build-list, DOMC).
- `validate_bank.py` — schema + per-format key checks + the grounding gate.
- `coverage.py` — what's covered and which sub-topics still need questions.

## Run the player
Browsers block reading local files, so serve the project folder:

```bash
cd "dbt analytics engineer cert chatbot"
python -m http.server 8000
# open http://localhost:8000/quiz/player/
```

(Or just open `quiz/player/index.html` and use the file-picker fallback to load `questions.json`.)

Pick **Practice** (instant feedback + citations) or **Exam** (timed, locked, scored at the end).

## Develop more questions
1. `python quiz/coverage.py` — see which sub-topics have no items.
2. Author new items into `questions.json` following `schema/item.schema.json`
   (ground each in a real `wiki/sources/*` or `raw/*` page).
3. `python quiz/validate_bank.py` — must pass before use.

Formats & scoring mirror Caveon/Scorpion: MCQ (default/partial/select-all),
fill-in-the-blank (dropdown/short-answer), matching, build-list (ordered,
weighted = partial by position), and DOMC (one option at a time, any wrong
response fails the item, forward-only).
