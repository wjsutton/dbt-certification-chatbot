"""quizcore — dependency-free core for the dbt Cert Coach MCP server.

Generation-first: the server uses MCP *sampling* (the connected client's LLM)
to write fresh, wiki-grounded questions; this module builds the grounding +
prompt, parses/validates the result, hides the answer for presentation, and
grades authoritatively. The static bank is used only for few-shot style
examples and offline validation — never served as the question itself.
"""
from __future__ import annotations
import json, re, random, hashlib, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "wiki" / "sources"
RAW_DIR = ROOT / "raw"
VERSION_TARGET = "dbt-core-1.11"

# ---------------- load corpus ----------------
def _frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    return (m.group(1), m.group(2)) if m else ("", text)

def load_sources():
    out = []
    for f in sorted(SRC_DIR.glob("*.md")):
        fm, body = _frontmatter(f.read_text(encoding="utf-8"))
        g = lambda k: (re.search(k+r':\s*"?(.*?)"?\s*$', fm, re.M) or [None, ""])[1]
        out.append({"id": f.stem, "title": re.sub(r"^Source summary — ", "", g("title")) or f.stem,
                    "url": g("source_url"), "domain": g("domain"), "text": body.strip()})
    return out

def load_examples():
    p = ROOT / "quiz" / "questions.json"
    return json.loads(p.read_text(encoding="utf-8"))["items"] if p.exists() else []

def load_meta():
    p = ROOT / "quiz" / "exam_meta.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

# ---------------- ranking (grounding retrieval) ----------------
_STOP = set("the a an of to in for on and or is are with how what which when use using your you it its as be by give me random question hard easy medium uber a an".split())
def rank(topic, sources=None, k=4):
    sources = sources if sources is not None else load_sources()
    terms = [t for t in re.findall(r"[a-z0-9_:+.-]+", (topic or "").lower()) if t not in _STOP and len(t) > 1]
    scored = []
    for s in sources:
        hay = (s["title"] + " " + s["id"] + " " + s["text"]).lower()
        n = sum((hay.count(t)) * (3 if (t in s["title"].lower() or t in s["id"]) else 1) for t in terms)
        scored.append((n, s))
    scored.sort(key=lambda x: -x[0])
    top = [s for n, s in scored if n > 0][:k]
    if not top:
        top = random.sample(sources, min(k, len(sources)))
    return top

def example_for(fmt, examples=None):
    examples = examples if examples is not None else load_examples()
    pool = [e for e in examples if fmt in ("auto", "", None) or e.get("format") == fmt]
    return random.choice(pool) if pool else (random.choice(examples) if examples else None)

# ---------------- generation prompt (for MCP sampling) ----------------
def gen_prompt(topic, difficulty, fmt, picks, example=None):
    fl = ("Choose the single best-fitting format from mcq, fitb, matching, build_list, domc, hotspot."
          if fmt in ("auto", "", None) else f"Use format: {fmt}.")
    dl = ("Difficulty: VERY HARD — a multi-step scenario with subtle, plausible distractors; prefer mcq with multiple correct (select_all), domc, or build_list."
          if difficulty == "uber-hard" else f"Difficulty: {difficulty}.")
    sources = "\n\n".join(f"### SOURCE: {p['title']} ({p['url']})\n{p['text']}" for p in picks)
    ex = ""
    if example:
        ex = "\n\nSTYLE EXAMPLE (match this JSON shape, do NOT reuse its content):\n" + json.dumps(
            {k: example[k] for k in example if k not in ("rationale",)}, ensure_ascii=False)
    schema = (
      'Return ONLY a JSON object (no markdown fences, no commentary):\n'
      '{ "format":"mcq|fitb|matching|build_list|domc|hotspot", "difficulty":"%s", "stem":"...", '
      '"rationale":"exam-accurate why the key is correct", "citations":[{"title":"<source>","url":"<url>"}], ...format fields... }\n'
      'Format fields:\n'
      '- mcq: "options":[{"id":"a","text":"...","correct":true|false}] (4-5); if >1 correct add "select_all":true.\n'
      '- domc: "options":[{"text":"...","correct":true|false}] (4-5 mix) + "present_n":2 + "unscored_after":1.\n'
      '- fitb: put {{b1}} (and optionally {{b2}}) tokens in the stem + "blanks":[{"id":"b1","type":"dropdown","options":["..."],"answer":"<one option>"} OR {"id":"b1","type":"short_answer","accepted":["...","..."]}].\n'
      '- matching: "left":[...], "right":[...], "key":{"<left>":"<right>",...} (every left present; right may add 1 distractor).\n'
      '- build_list: "items":[{"id":"1","text":"step"}], "answer":{"order":["1","2",...]}.\n'
      '- hotspot: "code":"<short multiline SQL/YAML/CLI snippet>", "hotspots":[{"id":"h1","text":"<exact substring from code>"}] (3-6), "correct":["h1"], "num_selections":1.'
    ) % difficulty
    return (f"You are an exam item writer for the dbt Analytics Engineering Certification ({VERSION_TARGET}).\n"
            f'Using ONLY facts in the SOURCES below, write exactly ONE practice question about: "{topic}".\n'
            f"{dl}\n{fl}\nGround every fact strictly in the SOURCES; use exact dbt tokens; valid JSON only.\n{schema}{ex}\n\n=== SOURCES ===\n{sources}")

# ---------------- parse / validate ----------------
def parse_item(text):
    if not isinstance(text, str):
        text = getattr(text, "text", None) or json.dumps(text)
    s = text.strip().replace("```json", "").replace("```", "").strip()
    i, j = s.find("{"), s.rfind("}")
    if i >= 0 and j > i:
        s = s[i:j+1]
    return json.loads(s)

def validate_item(item, picks=None):
    errs = []
    fmt = item.get("format")
    if fmt not in ("mcq", "fitb", "matching", "build_list", "domc", "hotspot"):
        errs.append(f"bad format {fmt!r}")
    if not item.get("stem"): errs.append("missing stem")
    if not item.get("citations"): errs.append("no citations (grounding gate)")
    if fmt == "mcq" and not any(o.get("correct") for o in item.get("options", [])): errs.append("mcq has no correct option")
    if fmt == "domc" and not any(o.get("correct") for o in item.get("options", [])): errs.append("domc has no correct option")
    if fmt == "matching":
        for l in item.get("left", []):
            if l not in item.get("key", {}): errs.append(f"matching left {l!r} missing from key")
    if fmt == "build_list":
        ids = {x.get("id") for x in item.get("items", [])}
        if set((item.get("answer", {}) or {}).get("order", [])) != ids: errs.append("build_list order must cover item ids")
    if fmt == "hotspot" and not item.get("correct"): errs.append("hotspot has no correct regions")
    return (len(errs) == 0, errs)

# ---------------- present (hide the answer) ----------------
def present(item, qid):
    f = item.get("format")
    base = {"question_id": qid, "format": f, "difficulty": item.get("difficulty", ""),
            "stem": item.get("stem", ""), "citations": item.get("citations", [])}
    if f == "mcq":
        base["options"] = [{"id": o["id"], "text": o["text"]} for o in item.get("options", [])]
        base["select_all"] = bool(item.get("select_all"))
        base["answer_format"] = '{"selected": ["a","c"]}'
    elif f == "domc":
        base["options"] = [{"text": o["text"]} for o in item.get("options", [])]
        base["present_n"] = item.get("present_n", len(item.get("options", [])))
        base["instructions"] = "Present options one at a time; for each, the candidate answers YES/NO."
        base["answer_format"] = '{"responses": {"<option text>": true_or_false, ...}}'
    elif f == "fitb":
        base["blanks"] = [{"id": b["id"], "type": b.get("type"), "options": b.get("options")} for b in item.get("blanks", [])]
        base["answer_format"] = '{"blanks": {"b1": "value", ...}}'
    elif f == "matching":
        base["left"] = item.get("left", [])
        base["right"] = list(item.get("right", []))
        random.shuffle(base["right"])
        base["answer_format"] = '{"pairs": {"<left text>": "<right text>", ...}}'
    elif f == "build_list":
        items = [{"id": x["id"], "text": x["text"]} for x in item.get("items", [])]
        random.shuffle(items)
        base["items"] = items
        base["answer_format"] = '{"order": ["id","id",...]}'
    elif f == "hotspot":
        base["code"] = item.get("code", "")
        base["hotspots"] = [{"id": h["id"], "text": h["text"]} for h in item.get("hotspots", [])]
        base["num_selections"] = item.get("num_selections", 1)
        base["answer_format"] = '{"selected": ["h1", ...]}'
    return base

# ---------------- grade (authoritative) ----------------
def _norm(x): return str(x).strip().lower()
def grade(item, answer):
    f = item.get("format"); answer = answer or {}
    if f == "mcq":
        correct = {o["id"] for o in item.get("options", []) if o.get("correct")}
        sel = set(answer.get("selected", []))
        ok = correct == sel
        return {"correct": ok, "score": 1.0 if ok else 0.0}
    if f == "fitb":
        n = 0; bs = item.get("blanks", [])
        for b in bs:
            v = (answer.get("blanks", {}) or {}).get(b["id"], "")
            if b.get("type") == "dropdown":
                n += (v == b.get("answer"))
            else:
                n += (_norm(v) in [_norm(a) for a in b.get("accepted", [])])
        return {"correct": n == len(bs), "score": (n / len(bs)) if bs else 0.0}
    if f == "matching":
        key = item.get("key", {}); pairs = answer.get("pairs", {}) or {}
        n = sum(1 for l in item.get("left", []) if pairs.get(l) == key.get(l))
        tot = len(item.get("left", []))
        return {"correct": n == tot, "score": (n / tot) if tot else 0.0}
    if f == "build_list":
        order = answer.get("order", []); key = (item.get("answer", {}) or {}).get("order", [])
        ok = order == key
        n = sum(1 for i, v in enumerate(key) if i < len(order) and order[i] == v)
        return {"correct": ok, "score": 1.0 if ok else (n / len(key) if key else 0.0)}
    if f == "domc":
        resp = answer.get("responses", {}) or {}
        bytext = {o["text"]: bool(o.get("correct")) for o in item.get("options", [])}
        need = item.get("present_n", len(bytext))
        if len(resp) < need:
            return {"correct": False, "score": 0.0, "note": f"answer at least {need} options"}
        ok = all(bool(v) == bytext.get(t, not v) for t, v in resp.items())
        return {"correct": ok, "score": 1.0 if ok else 0.0}
    if f == "hotspot":
        correct = set(item.get("correct", [])); sel = set(answer.get("selected", []))
        ok = correct == sel
        return {"correct": ok, "score": 1.0 if ok else 0.0}
    return {"correct": False, "score": 0.0, "note": "unknown format"}

def reveal(item):
    """Full answer key + rationale, returned after grading."""
    f = item.get("format")
    out = {"rationale": item.get("rationale", ""), "citations": item.get("citations", [])}
    if f == "mcq": out["correct_options"] = [o["id"] for o in item.get("options", []) if o.get("correct")]
    elif f == "domc": out["correct_map"] = {o["text"]: bool(o.get("correct")) for o in item.get("options", [])}
    elif f == "fitb": out["answers"] = {b["id"]: (b.get("answer") or b.get("accepted")) for b in item.get("blanks", [])}
    elif f == "matching": out["key"] = item.get("key", {})
    elif f == "build_list": out["order"] = (item.get("answer", {}) or {}).get("order", [])
    elif f == "hotspot": out["correct"] = item.get("correct", [])
    return out

def new_id(seed=""):
    return "q-" + hashlib.sha1((seed + str(random.random())).encode()).hexdigest()[:10]
