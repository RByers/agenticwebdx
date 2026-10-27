# Mining Claude Code session transcripts

These tools produced [`analysis/agent-sessions.md`](../../analysis/agent-sessions.md): how often coding agents misused web APIs, or spent a lot of tokens on them, in two real projects.

The transcripts themselves aren't in this repo. They're private sessions, read through the claude-code-remote MCP tools (`list_sessions`, `get_session`, `list_events`). Only derived data is published:
- `web/data/agent-session-incidents.csv`
- `web/data/agent-session-patterns.csv`

## Pipeline

1. **List and classify sessions.** Call `list_sessions(mine=true)` and page through the results. For each session, call `get_session` and read `session_context.sources[].git_repository.url` to get its repo. Keep the `RByers/zpcrweb` and `RByers/meshcore-web` sessions, plus 4 with no repo attached whose titles clearly belong to one of the two. Drop 6 empty sessions. That leaves 329.
2. **Pass 1: incident mining.** Fan the sessions out to subagents, 20 per batch, each following [`pass1-instructions.md`](pass1-instructions.md). Each subagent:
   - reads every transcript with `list_events`;
   - saves the large pages it got back to a work directory;
   - writes `findings/<batch>.jsonl`, with one `session` record per session and one `incident` record per problem found.
3. **Build a local corpus.** Run `build_corpus.py <workdir>`. It flattens the saved pages into `corpus/<session_id>.txt`, using the `session_id` inside each event, so pages filed in the wrong folder still land in the right session. It drops duplicate events by uuid. Pages that came back inline, rather than to a file, weren't saved, so 18 small sessions are missing from the corpus.
4. **Pass 2: frequency.** Group the incidents into 14 patterns ([`pass2-patterns.md`](pass2-patterns.md)). One subagent per pair of patterns searches the whole corpus with keywords, checks each hit by reading the text around it, and writes `freq/<label>.json`.
5. **Export CSVs.** Run `to_csv.py <workdir> web/data`. It writes the incident and pattern tables, leaving out verbatim quotes.

The prompt files still refer to the original scratch work directory; adjust the paths if you re-run them.
