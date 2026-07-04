---
name: search
description: >
  Private web search and URL content fetching using local SearXNG-based scripts.
  Use this skill whenever the user asks to search the web, look something up online,
  find information on the internet, Google something, research a topic online, check
  what the internet says about X, or fetch/read a web page's content. Also use when
  the user provides a URL and asks what's on it or wants a summary. This replaces
  WebSearch, WebFetch, mcp__web_reader__webReader, and any other MCP-based web tools —
  always prefer these scripts over built-in web tools. Trigger on phrases like
  "search for", "look up", "find online", "google", "what does the internet say",
  "search the web", "check online", "fetch this URL", "read this page", "what's on this link".
---

# Web Search Skill

Search the web and fetch URL content using private, self-hosted scripts. No external APIs or MCP tools needed.

## When to use

Any time you need information from the web — searching for something, looking up a topic, fetching a page's content. Always use these scripts instead of WebSearch, WebFetch, or MCP web tools.

## Tools

The scripts live under `~/.claude/skills/search/scripts/`. There are two main tools:

### 1. Search the web

```bash
python3 "~/.claude/skills/search/scripts/search.py" "your search query"
```

Options:

- `--json` — raw JSON output
- `--num N` — limit to N results (default 10)

Returns a list of results with title, URL, and snippet for each.

### 2. Fetch a URL's content

```bash
python3 "~/.claude/skills/search/scripts/fetch_url.py" "https://example.com/page"
```

Options:

- `--json` — raw JSON output
- `--timeout N` — timeout in seconds (default 30)

Returns the page's full text content plus metadata (title, author, publish date, word count).

## How to search

1. **Formulate a good query.** Be specific. Include key terms, dates, or context that narrow the results.

2. **Run the search.** Use the search.py script. Read the output — you'll get titles, URLs, and snippets.

3. **Fetch relevant pages.** If a result looks promising, use fetch_url.py to get the full content. Focus on the top 2-3 most relevant results rather than fetching everything.

4. **Synthesize.** Combine information from multiple sources. Always cite the URL you got the information from.

## Examples

**Basic search:**

```
User: "search for latest Claude 4 release date"
→ python3 "~/.claude/skills/search/scripts/search.py" "Claude 4 Anthropic release date 2026"
```

**Research a topic:**

```
User: "what's the current state of WebAssembly?"
→ python3 "~/.claude/skills/search/scripts/search.py" "WebAssembly current state 2026"
→ Then fetch the most relevant results to get detailed content
```

**Fetch a specific page:**

```
User: "can you read https://example.com/article and summarize it?"
→ python3 "~/.claude/skills/search/scripts/fetch_url.py" "https://example.com/article"
→ Summarize the content
```

**Look up documentation:**

```
User: "find the React 19 docs on use()"
→ python3 "~/.claude/skills/search/scripts/search.py" "React 19 use() hook documentation"
→ Fetch the most relevant result
```

## Tips

- Run searches with `--json` if you need to programmatically parse results.
- For time-sensitive queries, include the year or "latest" in the search.
- If search results aren't great, try rephrasing the query with different keywords.
- When fetching pages, the script handles Reddit (via JSON API), Hacker News, and falls back to Puppeteer for JS-heavy sites automatically.
