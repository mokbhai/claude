#!/usr/bin/env python3
"""
Private Search - Wrapper for SearXNG instance
Usage: python3 search.py "your search query"

This script provides private web search using a SearXNG instance that aggregates
results from multiple search engines (Brave, DuckDuckGo, Startpage, Google, Wikipedia).

Returns JSON results with titles, URLs, and content snippets for research.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import ssl
import certifi
from base64 import b64encode
from pathlib import Path


def _load_env():
    """Walk up from script dir to find and load .env file."""
    current = Path(__file__).resolve().parent
    for _ in range(10):  # max 10 levels up
        env_file = current / ".env"
        if env_file.is_file():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        os.environ.setdefault(key.strip(), value.strip())
            return
        if current.parent == current:
            break
        current = current.parent


_load_env()

# Configuration (from environment variables)
API_ENDPOINT = os.environ.get("SEARXNG_API_ENDPOINT", "")
AUTH_USER = os.environ.get("SEARXNG_AUTH_USER", "")
AUTH_PASS = os.environ.get("SEARXNG_AUTH_PASS", "")


def create_basic_auth_header(username, password):
    """Create Basic Auth header"""
    credentials = f"{username}:{password}"
    encoded = b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


def search(query, num_results=10):
    """Perform search query against SearXNG instance

    Args:
        query: Search query string
        num_results: Maximum number of results to return (default 10)

    Returns:
        dict: Search results with 'results' list containing title, url, content
    """
    # URL-encode the query
    encoded_query = urllib.parse.quote(query)

    # Build the URL with format=json
    url = f"{API_ENDPOINT}?format=json&q={encoded_query}"

    # Create request with Basic Auth
    request = urllib.request.Request(url)
    request.add_header("Authorization", create_basic_auth_header(AUTH_USER, AUTH_PASS))
    request.add_header("User-Agent", "OpenClaw/1.0")

    try:
        # Create SSL context with certifi certificates
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        # Make the request
        with urllib.request.urlopen(request, timeout=30, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            # Limit results
            if "results" in data and len(data["results"]) > num_results:
                data["results"] = data["results"][:num_results]
            return data
    except urllib.error.HTTPError as e: # type: ignore
        return {"error": f"HTTP Error {e.code}: {e.reason}", "results": []}
    except urllib.error.URLError as e: # type: ignore
        return {"error": f"URL Error: {e.reason}", "results": []}
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse JSON: {e}", "results": []}
    except Exception as e:
        return {"error": f"Unexpected error: {e}", "results": []}


def format_results(results):
    """Format search results for display"""
    if "error" in results:
        return f"Error: {results['error']}\n"

    if not results.get("results"):
        return "No results found.\n"

    output = []
    output.append(f"Found {len(results['results'])} results for: {results.get('query', 'unknown')}\n")
    output.append("-" * 60)

    for i, result in enumerate(results["results"], 1):
        title = result.get("title", "No title")
        url = result.get("url", "")
        content = result.get("content", "").strip()[:300]  # Truncate long snippets

        output.append(f"\n{i}. {title}")
        if url:
            output.append(f"   URL: {url}")
        if content:
            output.append(f"   Snippet: {content}...")

    output.append("\n" + "-" * 60)
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 search.py \"your search query\" [--json] [--num N]")
        print("\nOptions:")
        print("  --json    Output raw JSON results")
        print("  --num N   Limit to N results (default 10)")
        print("\nExample:")
        print('  python3 search.py "quantum computing 2025"')
        print('  python3 search.py "AI safety research" --json --num 20')
        sys.exit(1)

    # Parse arguments
    query_parts = []
    output_json = False
    num_results = 10

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--json":
            output_json = True
        elif arg == "--num":
            if i + 1 < len(sys.argv):
                num_results = int(sys.argv[i + 1])
                i += 1
        else:
            query_parts.append(arg)
        i += 1

    query = " ".join(query_parts)
    print(f"Searching for: {query}\n", file=sys.stderr)

    results = search(query, num_results)

    if output_json:
        print(json.dumps(results, indent=2))
    else:
        print(format_results(results))


if __name__ == "__main__":
    main()
