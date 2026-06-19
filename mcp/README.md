# dbt Cert Coach — MCP server

A Model Context Protocol server that **generates fresh, wiki-grounded** dbt
certification practice questions on demand and grades them. Questions are
written by the connected client's LLM via MCP **sampling**, grounded only in
this repo's `wiki/sources/` summaries — the static `quiz/questions.json` bank is
used only as few-shot style examples, never served as the answer.

## Tools
| Tool | What it does |
|------|--------------|
| `generate_question(topic, difficulty?, format?)` | Writes one fresh grounded question (answer hidden). difficulty: easy\|medium\|hard\|uber-hard. format: auto\|mcq\|fitb\|matching\|build_list\|domc\|hotspot. |
| `grade_answer(question_id, answer)` | Authoritative grading; reveals key + rationale + citations. |
| `start_interview(length?)` / `interview_answer(session_id, answer)` | Adaptive interview across all 7 domains; returns a per-domain gap report. |
| `exam_overview()` / `list_domains()` | Certification logistics, formats, and domain weighting. |
| `search_wiki(query, k?)` | Retrieve grounding summaries (for "explain X"). |
| `submit_question(item)` | Fallback: register a host-generated item for grading (used when the client can't sample). |

The `answer` shape per format is returned with each question in its `answer_format` field
(e.g. mcq → `{"selected":["a","c"]}`, build_list → `{"order":["1","2",...]}`).

## Install
```bash
pip install -r requirements.txt   # from the repo root
```

## Connect a client (stdio)

**Claude Desktop** — add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "dbt-cert-coach": {
      "command": "python",
      "args": ["mcp/server.py"],
      "cwd": "/ABSOLUTE/PATH/TO/dbt-certification-chatbot"
    }
  }
}
```

**Cursor** (`.cursor/mcp.json`) and other MCP clients use the same command/args/cwd.

Then ask: *"generate an uber-hard question on dbt parse"*, *"interview me to find my gaps"*, or *"give me the certification overview"*.

> **Note on sampling:** generation uses MCP sampling, so the client must support it.
> If it doesn't, `generate_question` returns the grounding and instructions for the host
> model to write the item and register it via `submit_question` — still fully grounded.
