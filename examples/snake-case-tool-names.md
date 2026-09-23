# Example: snake_case tool-name check

Full output of `/ai-pm-skills:build-or-not`, run with Claude Sonnet on 2026-09-22.

Prompt: *"Add a check to mcp-doctor that flags MCP servers whose tool names aren't snake_case. Keep the sample to 6 repos from GitHub (use gh search), and keep the answer to the decision record only."*

---

## Build or not: mcp-doctor check for non-snake_case MCP tool names

**Claim checked:** Real, actively-used MCP servers define at least one tool name that isn't snake_case (camelCase, kebab-case, PascalCase, or mixed), making a naming-convention check in mcp-doctor useful.
**Sample:** 6 real MCP server repos, chosen by: `gh search repos --topic mcp --sort stars`, taking single-purpose MCP server implementations in descending star order (excluding curated lists like `awesome-mcp-servers`, SDKs/frameworks for *building* servers like `fastmcp`, and platforms where MCP is one feature among many like `activepieces`/`dbx`). `googleapis/mcp-toolbox` (16.5k★) was the 4th pick but was scored **N/A** on inspection — it's config-driven, so tool names come from a user-authored `tools.yaml`, not the server's own code — and was replaced with the next-highest-starred qualifying repo, `idosal/git-mcp` (8.4k★).
**Bar (set before checking):** hit = the server's own tool definitions contain at least one tool name that isn't snake_case; build if 3+/6 reachable hits (naming-convention check, not safety-critical, so no single-hit override).

| # | Example | Result | Evidence | Reachable? |
|---|---|---|---|---|
| 1 | DeusData/codebase-memory-mcp (C) | Miss | `src/mcp/mcp.c:466` `TOOLS[]` array — `index_repository`, `search_graph`, `query_graph`, `trace_path`, `get_code_snippet`, `get_file_outline`, `get_graph_schema` | Yes |
| 2 | microsoft/playwright-mcp (TS) | Miss | `README.md` tool list, ~70 tools — `browser_click`, `browser_cookie_clear`, `browser_take_screenshot`, etc. | Yes |
| 3 | github/github-mcp-server (Go) | Miss | `cmd/mcpcurl/README.md` — `get_issue`, `create_pull_request`, `search_code`, `list_commits`, etc. | Yes |
| 4 | idosal/git-mcp (TS) | Miss | `src/api/tools/commonTools.ts` — `generateSearchToolName`/`generateFetchToolName` explicitly replace non-alphanumeric chars with `_`; e.g. `fetch_generic_url_content`, `search_documentation` | Yes |
| 5 | GLips/Figma-Context-MCP (TS) | Miss | `src/mcp/tools/get-figma-data-tool.ts`, `download-figma-images-tool.ts` — `get_figma_data`, `download_figma_images` | Yes |
| 6 | wonderwhy-er/DesktopCommanderMCP (TS) | Miss | `src/server.ts:309-1156`, 24 tools — `get_config`, `read_file`, `edit_block`, `start_process`, `give_feedback_to_desktop_commander`, etc. | Yes |

**Result:** 0/6 reachable hits.
**Decision:** Don't build.
**Why, in one sentence:** 0 of 6 real MCP servers sampled — spanning C, TypeScript, and Go across code-intelligence, browser-automation, GitHub, docs-fetch, design, and filesystem/process-control use cases — had a single non-snake_case tool name, so the check would report "clean" on virtually every real server.
**What would reopen this:** evidence that config-driven MCP servers (where tool names come from user-authored YAML/JSON rather than fixed source, like `mcp-toolbox`) commonly produce non-snake_case names in practice — its own README example tool is `search-hotels-by-name` (kebab-case) — which suggests the real risk sits in user config, not server source, and wasn't tested by this sample.
