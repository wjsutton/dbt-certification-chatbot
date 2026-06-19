#!/usr/bin/env python3
"""dbt Cert Coach — MCP server.

Generation-first: questions are written fresh by the connected client's LLM via
MCP *sampling*, grounded ONLY in the project's wiki source summaries. The static
bank (quiz/questions.json) is used solely as few-shot style examples — never
served as the answer. Grading is authoritative (server-side); correct answers
are never exposed until after grading.

Run (stdio):  python mcp/server.py
"""
from __future__ import annotations
import json
from mcp.server.fastmcp import FastMCP, Context
from mcp import types
import quizcore as qc

mcp = FastMCP("dbt-cert-coach")

SOURCES = qc.load_sources()
EXAMPLES = qc.load_examples()
META = qc.load_meta()
STORE: dict[str, dict] = {}        # question_id -> full item (with answer key)
INTERVIEWS: dict[str, dict] = {}   # session_id -> state

async def _generate(ctx: Context, topic: str, difficulty: str, fmt: str) -> dict:
    """Use client sampling to write one grounded item; validate + store."""
    picks = qc.rank(topic, SOURCES, k=4)
    prompt = qc.gen_prompt(topic, difficulty, fmt, picks, qc.example_for(fmt, EXAMPLES))
    last_err = None
    for _ in range(2):  # one retry
        res = await ctx.session.create_message(
            messages=[types.SamplingMessage(role="user", content=types.TextContent(type="text", text=prompt))],
            max_tokens=1700,
            system_prompt="You are a precise exam-item writer. Output strict JSON only, grounded in the provided sources.",
        )
        text = res.content.text if isinstance(res.content, types.TextContent) else str(res.content)
        try:
            item = qc.parse_item(text)
        except Exception as e:
            last_err = f"parse error: {e}"; continue
        ok, errs = qc.validate_item(item, picks)
        if ok:
            qid = qc.new_id(topic)
            item["_sources"] = [{"title": p["title"], "url": p["url"]} for p in picks]
            STORE[qid] = item
            out = qc.present(item, qid)
            out["sources"] = item["_sources"]
            out["mode"] = "generated"
            return out
        last_err = "; ".join(errs)
    raise RuntimeError(last_err or "generation failed")

@mcp.tool()
async def generate_question(ctx: Context, topic: str, difficulty: str = "medium", format: str = "auto") -> dict:
    """Generate ONE fresh, wiki-grounded practice question about `topic`.
    difficulty: easy|medium|hard|uber-hard. format: auto|mcq|fitb|matching|build_list|domc|hotspot.
    Returns the question WITHOUT the answer; grade with `grade_answer(question_id, answer)`.
    If the client doesn't support sampling, returns grounding so the host can generate and call `submit_question`."""
    try:
        return await _generate(ctx, topic, difficulty, format)
    except Exception as e:
        picks = qc.rank(topic, SOURCES, k=4)
        return {"mode": "needs_host_generation", "reason": str(e),
                "instruction": "Write ONE question grounded ONLY in `grounding`, following the schema in quiz/schema/item.schema.json, then call submit_question(item).",
                "grounding": [{"title": p["title"], "url": p["url"], "content": p["text"]} for p in picks]}

@mcp.tool()
def submit_question(item: dict) -> dict:
    """Register a host-generated item (fallback path) so it can be graded. Returns the answer-hidden presentation."""
    ok, errs = qc.validate_item(item)
    if not ok:
        return {"error": "invalid item", "problems": errs}
    qid = qc.new_id(item.get("stem", ""))
    STORE[qid] = item
    out = qc.present(item, qid); out["mode"] = "registered"
    return out

@mcp.tool()
def grade_answer(question_id: str, answer: dict) -> dict:
    """Grade an answer to a previously generated question. answer shape depends on format
    (see the `answer_format` field returned with the question). Reveals the key + rationale + citations."""
    item = STORE.get(question_id)
    if not item:
        return {"error": f"unknown question_id {question_id!r}"}
    g = qc.grade(item, answer)
    g.update(qc.reveal(item))
    return g

@mcp.tool()
def get_quiz_context(topic: str, difficulty: str = "medium", format: str = "auto") -> dict:
    """Stateless grounding for a UI/artifact that generates its own question.
    Returns retrieved wiki sources + a style example so the caller's LLM can write a
    grounded item, then grade it with `grade_item(item, answer)`."""
    picks = qc.rank(topic, SOURCES, k=4)
    return {"topic": topic, "difficulty": difficulty, "format": format,
            "grounding": [{"title": p["title"], "url": p["url"], "content": p["text"]} for p in picks],
            "style_example": qc.example_for(format, EXAMPLES),
            "schema_path": "quiz/schema/item.schema.json"}

@mcp.tool()
def grade_item(item: dict, answer: dict) -> dict:
    """Stateless authoritative grading: caller passes the full item it generated +
    the candidate's answer; returns correct/score + the key + rationale + citations."""
    g = qc.grade(item, answer)
    g.update(qc.reveal(item))
    return g

@mcp.tool()
def exam_overview() -> dict:
    """Certification logistics, the six question types, and content-domain weighting."""
    return META

@mcp.tool()
def list_domains() -> list:
    """The seven exam domains with their sub-topics and approximate weighting."""
    return META.get("domains", [])

@mcp.tool()
def search_wiki(query: str, k: int = 4) -> list:
    """Retrieve the most relevant wiki source summaries for a query (for explaining a concept / grounding)."""
    return [{"title": p["title"], "url": p["url"], "content": p["text"]} for p in qc.rank(query, SOURCES, k=k)]

@mcp.tool()
async def start_interview(ctx: Context, length: int = 8) -> dict:
    """Begin an adaptive interview that asks `length` questions across all domains and reports gaps.
    Returns a session_id and the first question. Answer with `interview_answer`."""
    import uuid
    doms = list(META.get("domains", []))
    import random as _r; _r.shuffle(doms)
    sid = uuid.uuid4().hex[:8]
    INTERVIEWS[sid] = {"length": length, "n": 0, "i": 0, "order": doms, "score": {}, "current": None}
    return await _interview_next(ctx, sid)

async def _interview_next(ctx: Context, sid: str) -> dict:
    st = INTERVIEWS[sid]
    if st["n"] >= st["length"]:
        return _interview_report(sid)
    dom = st["order"][st["i"] % len(st["order"])]; st["i"] += 1; st["n"] += 1
    import random as _r
    sub = _r.choice(dom["subs"])
    q = await _generate(ctx, sub, _r.choice(["medium", "hard", "hard", "uber-hard"]), "auto")
    st["current"] = {"qid": q["question_id"], "domain": dom["id"], "domain_name": dom["name"]}
    q["interview"] = {"session_id": sid, "question": st["n"], "of": st["length"], "domain": dom["name"]}
    return q

@mcp.tool()
async def interview_answer(ctx: Context, session_id: str, answer: dict) -> dict:
    """Submit an answer in an interview; returns grading + the next question, or the gap report when done."""
    st = INTERVIEWS.get(session_id)
    if not st or not st.get("current"):
        return {"error": "no active question for this session"}
    cur = st["current"]; item = STORE.get(cur["qid"])
    g = qc.grade(item, answer); g.update(qc.reveal(item))
    s = st["score"].setdefault(cur["domain"], {"name": cur["domain_name"], "n": 0, "c": 0})
    s["n"] += 1; s["c"] += 1 if g["correct"] else 0
    st["current"] = None
    nxt = await _interview_next(ctx, session_id)
    return {"grading": g, "next": nxt}

def _interview_report(sid: str) -> dict:
    st = INTERVIEWS[sid]
    rows = list(st["score"].values())
    total = sum(r["n"] for r in rows); correct = sum(r["c"] for r in rows)
    weak = sorted([r for r in rows if r["n"] and r["c"]/r["n"] < 0.6], key=lambda r: r["c"]/r["n"])
    tested = {r["name"] for r in rows}
    untested = [d["name"] for d in META.get("domains", []) if d["name"] not in tested]
    return {"mode": "report", "overall": f"{correct}/{total}",
            "percent": round(correct/total*100) if total else 0,
            "by_domain": rows,
            "focus_on": [r["name"] for r in weak] or ["(solid across what we tested)"],
            "untested_domains": untested}

if __name__ == "__main__":
    mcp.run()
