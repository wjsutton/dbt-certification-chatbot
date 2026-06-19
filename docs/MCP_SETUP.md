# Setup & architecture — connecting to the dbt Cert Coach

This explains how a teammate connects, and how a **UI (artifact) can run on top of
the MCP server** so Claude "builds the quiz and runs the engine underneath."

## The pieces

```
 wiki/sources/*  ── grounding corpus (56 summaries, version-pinned to dbt 1.11)
        │
        ▼
 mcp/server.py  ── dbt-cert-coach MCP server (the ENGINE)
   tools: generate_question · grade_answer · start_interview/interview_answer
          get_quiz_context · grade_item · exam_overview · list_domains · search_wiki
        │
   ┌────┴───────────────────────────────────────────┐
   ▼                                                 ▼
 CHAT-NATIVE client                          ARTIFACT / UI front-end
 (Claude Desktop, Cursor)                    (Cowork canvas, or static HTML)
 quiz happens in the chat                    calls the server's tools for
 via the MCP tools                           grounding + grading; renders the
                                             six exam formats visually
```

The server is the single source of truth for **grounding** (which dbt facts) and
**grading** (authoritative, answers never exposed early). A front-end just renders
and collects answers.

## Two ways it runs

### A) Chat-native (Claude Desktop / Cursor) — simplest, no UI canvas
You chat; Claude calls the tools. `generate_question` uses **MCP sampling** (your
client's own model writes the question, grounded in retrieved wiki sources), and
`grade_answer` scores it. Interview mode walks all seven domains and reports gaps.
Nothing to render — the conversation *is* the quiz.

### B) Artifact UI over the MCP (Cowork) — "Claude builds the artifact, MCP underneath"
In Cowork, an HTML **artifact** can call connected MCP tools from inside the page:

```js
// inside the artifact (Cowork injects window.cowork)
const ctx  = await window.cowork.callMcpTool('mcp__dbt-cert-coach__get_quiz_context',
                {topic, difficulty, format});           // grounding from the server
const item = JSON.parse(await window.cowork.askClaude(  // generate, grounded in ctx
                buildPrompt(topic, difficulty, format), ctx.grounding));
renderQuestion(item);                                    // draw the exam-format UI
// on submit:
const result = await window.cowork.callMcpTool('mcp__dbt-cert-coach__grade_item',
                {item, answer});                         // authoritative grading
```

So the flow is: **you connect the MCP server → ask Claude "open the dbt quiz coach"
→ Claude calls `create_artifact` to render the UI → the artifact calls the server's
`get_quiz_context` / `grade_item` tools.** The bundled `quiz/generator.html` is the
self-contained version of this UI (it uses `askClaude` for generation today; the two
stateless tools above let an artifact delegate grounding + grading to the server).

**Honest caveats:** the artifact *canvas* is a Cowork feature (Claude Desktop/Cursor
have no equivalent — there you use chat-native, or open `quiz/player/index.html` in a
browser). MCP **sampling** support varies by client; if a client can't sample,
`generate_question` returns grounding for the host to generate via `submit_question`.

## Getting teammates connected (increasing turnkey-ness)

**1. Clone + stdio config (works everywhere, a little technical)**
```bash
git clone <repo> dbt-certification-chatbot
cd dbt-certification-chatbot && pip install -r requirements.txt
```
Claude Desktop `claude_desktop_config.json` (Cursor `.cursor/mcp.json` is the same):
```json
{ "mcpServers": { "dbt-cert-coach": {
  "command": "python", "args": ["mcp/server.py"],
  "cwd": "/ABSOLUTE/PATH/TO/dbt-certification-chatbot" } } }
```

**2. `uvx`/`pipx` (no manual venv)** — publish the server (with data) as a package, then:
```json
{ "mcpServers": { "dbt-cert-coach": { "command": "uvx", "args": ["dbt-cert-coach"] } } }
```

**3. Desktop Extension bundle (`.mcpb`/`.dxt`) — one-click, no terminal**
Package `mcp/` + data + a `manifest.json` into a bundle; teammates double-click to
install in Claude Desktop. Best for non-technical folks. (Build step lives in the repo;
the bundle embeds Python deps + the wiki corpus.)

**4. Hosted remote MCP (one URL, zero local setup)** — run the server once (streamable
-HTTP) behind SSO/VPN; teammates add a single remote-server URL. Most turnkey; needs
hosting + the version bump in `server.py` to expose an HTTP transport (`mcp.run(transport="streamable-http")`).

## Recommendation
- Start with **(1)** for yourself and pilot users today.
- For broad rollout to the team, build the **(3) .mcpb bundle** (one-click) or stand up
  the **(4) hosted remote** — both remove the clone/pip step.
- Use the **Cowork artifact (B)** when you want the visual exam-format experience;
  **chat-native (A)** everywhere else.

## Keeping content current
The server reads `wiki/sources/` and `quiz/exam_meta.json` at startup, so after the
weekly refresh pipeline merges new docs, **restart the server** (or redeploy the bundle/
remote) to pick them up. No code changes needed for routine dbt-doc updates; a dbt
*major* version bump means retargeting `version_target` and re-running the pipeline.
