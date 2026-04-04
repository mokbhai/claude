#!/usr/bin/env python3
"""
URL Fetcher - Fetch and extract content from web URLs
Usage: python3 fetch_url.py "https://example.com/article"

This script fetches web content and extracts clean, readable text with metadata.
Returns JSON output suitable for research workflows.

Features:
- HTML to clean text/markdown conversion
- Metadata extraction (title, description, author, date, etc.)
- Content quality indicators (word count, reading time)
- Error handling with detailed messages
- SSL/TLS with certifi certificates
- Timeout handling
- User-agent rotation for better compatibility
"""

import sys
import json
import re
import subprocess
import urllib.request
import urllib.parse
import urllib.error
import ssl
import certifi
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


# Configuration
DEFAULT_TIMEOUT = 30  # seconds
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max
PUPPETEER_SCRIPT = Path(__file__).parent / 'puppeteer_fetch.js'

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

# Sites that need special handling
SPECIAL_SITES = {
    'reddit': ['reddit.com', 'www.reddit.com', 'old.reddit.com'],
    'twitter': ['twitter.com', 'x.com', 'www.twitter.com', 'www.x.com'],
    'hackernews': ['news.ycombinator.com'],
    'github': ['github.com', 'gist.github.com'],
}

# Sites known to require browser automation (heavy JS/CAPTCHA)
BROWSER_REQUIRED_SITES = [
    'medium.com',
    'substack.com',
    'quora.com',
    'stackoverflow.com',
    'stackexchange.com',
    'zhihu.com',
    'twitter.com',
    'x.com',
    'facebook.com',
    'instagram.com',
    'linkedin.com',
]


class HTMLToTextParser(HTMLParser):
    """Parse HTML and extract clean text with structure preservation"""

    # Tags that should add block-level spacing
    BLOCK_TAGS = {'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                  'ul', 'ol', 'li', 'blockquote', 'pre', 'article',
                  'section', 'header', 'footer', 'main', 'aside'}

    # Tags to skip entirely
    SKIP_TAGS = {'script', 'style', 'nav', 'footer', 'header', 'aside',
                 'noscript', 'iframe', 'svg', 'form', 'input', 'button'}

    # Tags that represent semantic structure
    HEADING_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}
    LIST_TAGS = {'ul', 'ol', 'li'}

    def __init__(self):
        super().__init__()
        self.text_parts: List[str] = []
        self.tag_stack: List[str] = []
        self.skip_depth: int = 0
        self.list_depth: int = 0
        self.current_href: Optional[str] = None
        self.links: List[Dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        tag = tag.lower()
        self.tag_stack.append(tag)

        # Skip certain tags entirely
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return

        if self.skip_depth > 0:
            return

        # Handle links
        if tag == 'a':
            attrs_dict = dict(attrs)
            self.current_href = attrs_dict.get('href')

        # Handle list nesting
        if tag in ('ul', 'ol'):
            self.list_depth += 1

        # Add newlines for block tags
        if tag in self.BLOCK_TAGS:
            self.text_parts.append('\n')

        # Add markdown-style heading prefix
        if tag in self.HEADING_TAGS:
            level = int(tag[1])  # h1 -> 1, h2 -> 2, etc.
            self.text_parts.append('\n' + '#' * level + ' ')

    def handle_endtag(self, tag: str):
        tag = tag.lower()

        # Pop from stack
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()

        # Handle skip tags
        if tag in self.SKIP_TAGS and self.skip_depth > 0:
            self.skip_depth -= 1
            return

        if self.skip_depth > 0:
            return

        # Handle links
        if tag == 'a':
            self.current_href = None

        # Handle list nesting
        if tag in ('ul', 'ol'):
            self.list_depth = max(0, self.list_depth - 1)

        # Add spacing for block tags
        if tag in self.BLOCK_TAGS:
            self.text_parts.append('\n')

        # List items
        if tag == 'li':
            self.text_parts.append('\n')

    def handle_data(self, data: str):
        if self.skip_depth > 0:
            return

        # Skip empty or whitespace-only data
        if not data.strip():
            return

        # Handle list items with proper indentation
        if self.tag_stack and 'li' in self.tag_stack:
            indent = '  ' * (self.list_depth - 1)
            if not self.text_parts or self.text_parts[-1].endswith('\n'):
                self.text_parts.append(f"{indent}- ")
            else:
                self.text_parts.append(data)
        else:
            self.text_parts.append(data)

    def get_text(self) -> str:
        """Get cleaned text"""
        text = ''.join(self.text_parts)
        # Normalize whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()


def extract_metadata(html_content: str, url: str) -> Dict[str, Any]:
    """Extract metadata from HTML content"""

    metadata = {
        'title': None,
        'description': None,
        'author': None,
        'publish_date': None,
        'modified_date': None,
        'keywords': [],
        'canonical_url': None,
        'og_type': None,
        'site_name': None,
    }

    # Extract title
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
    if title_match:
        metadata['title'] = title_match.group(1).strip()

    # Extract meta tags
    meta_patterns = {
        'description': [
            r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']',
        ],
        'author': [
            r'<meta[^>]+name=["\']author["\'][^>]+content=["\']([^"\']+)["\']',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']author["\']',
        ],
        'publish_date': [
            r'<meta[^>]+property=["\']article:published_time["\'][^>]+content=["\']([^"\']+)["\']',
            r'<meta[^>]+name=["\']publish-date["\'][^>]+content=["\']([^"\']+)["\']',
            r'<meta[^>]+name=["\']date["\'][^>]+content=["\']([^"\']+)["\']',
        ],
        'modified_date': [
            r'<meta[^>]+property=["\']article:modified_time["\'][^>]+content=["\']([^"\']+)["\']',
        ],
        'keywords': [
            r'<meta[^>]+name=["\']keywords["\'][^>]+content=["\']([^"\']+)["\']',
        ],
        'canonical_url': [
            r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        ],
        'og_type': [
            r'<meta[^>]+property=["\']og:type["\'][^>]+content=["\']([^"\']+)["\']',
        ],
        'site_name': [
            r'<meta[^>]+property=["\']og:site_name["\'][^>]+content=["\']([^"\']+)["\']',
        ],
    }

    for field, patterns in meta_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, html_content, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                if field == 'keywords':
                    metadata[field] = [k.strip() for k in value.split(',') if k.strip()]
                else:
                    metadata[field] = value
                break

    # Also check for og:title if regular title not found
    if not metadata['title']:
        og_title = re.search(
            r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']',
            html_content, re.IGNORECASE
        )
        if og_title:
            metadata['title'] = og_title.group(1).strip()

    return metadata


def estimate_reading_time(word_count: int) -> int:
    """Estimate reading time in minutes (average 200 words/minute)"""
    return max(1, round(word_count / 200))


def detect_site_type(url: str) -> Optional[str]:
    """Detect if URL is from a site that needs special handling"""
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ''

    for site_type, domains in SPECIAL_SITES.items():
        if hostname in domains:
            return site_type
    return None


def fetch_reddit_post(url: str, timeout: int) -> Dict[str, Any]:
    """Fetch Reddit post content using JSON API"""
    result = {
        'url': url,
        'fetched_at': datetime.now().isoformat(),
        'success': False,
        'title': None,
        'content': None,
        'content_format': 'text',
        'metadata': {},
        'quality': {
            'word_count': 0,
            'reading_time_minutes': 0,
            'has_substantial_content': False,
        },
        'error': None,
    }

    # Convert to JSON API URL
    json_url = url.rstrip('/')
    if not json_url.endswith('.json'):
        json_url += '.json'

    import random
    user_agent = random.choice(USER_AGENTS)

    request = urllib.request.Request(json_url)
    request.add_header('User-Agent', user_agent)
    request.add_header('Accept', 'application/json')

    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        with urllib.request.urlopen(request, timeout=timeout, context=ssl_context) as response:
            raw_data = response.read().decode('utf-8', errors='replace')
            data = json.loads(raw_data)

        # Reddit returns a list with post data at index 0
        if isinstance(data, list) and len(data) > 0:
            post_data = data[0]['data']['children'][0]['data']
        elif isinstance(data, dict) and 'data' in data:
            post_data = data['data']['children'][0]['data']
        else:
            return {**result, 'error': 'Unexpected Reddit JSON structure'}

        # Extract post information
        title = post_data.get('title', '')
        author = post_data.get('author', '')
        subreddit = post_data.get('subreddit', '')
        selftext = post_data.get('selftext', '')
        score = post_data.get('score', 0)
        num_comments = post_data.get('num_comments', 0)
        created_utc = post_data.get('created_utc', 0)
        url_post = post_data.get('url', '')
        link_flair_text = post_data.get('link_flair_text', '')

        # Build content text
        content_parts = [f"# {title}"]
        content_parts.append(f"\n**Posted by** u/{author} in r/{subreddit}")
        content_parts.append(f"**Score:** {score:,} | **Comments:** {num_comments:,}")

        if link_flair_text:
            content_parts.append(f"**Flair:** {link_flair_text}")

        if url_post and not url_post.startswith('https://www.reddit.com/'):
            content_parts.append(f"\n**Link:** {url_post}")

        if selftext:
            content_parts.append(f"\n---\n\n{selftext}")

        # Try to fetch top comments
        comments_text = fetch_reddit_comments(data, max_comments=10)
        if comments_text:
            content_parts.append(f"\n---\n\n## Top Comments\n\n{comments_text}")

        content = '\n'.join(content_parts)

        # Convert UTC timestamp to datetime
        from datetime import timezone
        publish_date = None
        if created_utc:
            try:
                dt = datetime.fromtimestamp(created_utc, tz=timezone.utc)
                publish_date = dt.isoformat()
            except:
                pass

        word_count = len(content.split())

        result.update({
            'success': True,
            'title': title,
            'content': content,
            'content_format': 'markdown',
            'metadata': {
                'author': author,
                'subreddit': subreddit,
                'score': score,
                'num_comments': num_comments,
                'publish_date': publish_date,
                'link_flair': link_flair_text,
                'external_url': url_post if url_post and not url_post.startswith('https://www.reddit.com/') else None,
            },
            'quality': {
                'word_count': word_count,
                'reading_time_minutes': estimate_reading_time(word_count),
                'has_substantial_content': word_count > 50,
            }
        })

    except urllib.error.HTTPError as e:
        return {**result, 'error': f"HTTP Error {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {**result, 'error': f"URL Error: {str(e.reason)}"}
    except json.JSONDecodeError as e:
        return {**result, 'error': f"JSON parsing error: {str(e)}"}
    except Exception as e:
        return {**result, 'error': f"Unexpected error: {str(e)}"}

    return result


def fetch_reddit_comments(data: Any, max_comments: int = 10) -> str:
    """Extract top comments from Reddit JSON response"""
    comments = []

    def extract_comments(comment_data, depth=0):
        if len(comments) >= max_comments:
            return

        if isinstance(comment_data, dict):
            if comment_data.get('kind') == 't1':  # Comment
                body = comment_data.get('data', {}).get('body', '')
                author = comment_data.get('data', {}).get('author', 'unknown')
                score = comment_data.get('data', {}).get('score', 0)

                if body and not body.startswith('[deleted]') and not body.startswith('[removed]'):
                    comments.append({
                        'author': author,
                        'score': score,
                        'body': body,
                        'depth': depth
                    })

                # Process replies
                replies = comment_data.get('data', {}).get('replies', {})
                if isinstance(replies, dict) and 'data' in replies:
                    children = replies.get('data', {}).get('children', [])
                    for child in children:
                        extract_comments(child, depth + 1)

            elif 'data' in comment_data:
                children = comment_data.get('data', {}).get('children', [])
                for child in children:
                    extract_comments(child, depth)

        elif isinstance(comment_data, list):
            for item in comment_data:
                extract_comments(item, depth)

    # Comments are usually at index 1 in the response
    if isinstance(data, list) and len(data) > 1:
        extract_comments(data[1])
    elif isinstance(data, dict):
        extract_comments(data)

    # Sort by score and format
    comments.sort(key=lambda x: x['score'], reverse=True)
    comments = comments[:max_comments]

    formatted = []
    for c in comments:
        indent = "  " * c['depth']
        body = c['body'].replace('\n', f'\n{indent}  ')
        formatted.append(f"{indent}**u/{c['author']}** ({c['score']:,} pts):\n{indent}> {body}")

    return '\n\n'.join(formatted)


def fetch_hackernews(url: str, timeout: int) -> Dict[str, Any]:
    """Fetch Hacker News content using their API"""
    result = {
        'url': url,
        'fetched_at': datetime.now().isoformat(),
        'success': False,
        'title': None,
        'content': None,
        'content_format': 'text',
        'metadata': {},
        'quality': {
            'word_count': 0,
            'reading_time_minutes': 0,
            'has_substantial_content': False,
        },
        'error': None,
    }

    # Extract item ID from URL
    import re as re_module
    match = re_module.search(r'item\?id=(\d+)', url)
    if not match:
        return {**result, 'error': 'Could not extract HN item ID from URL'}

    item_id = match.group(1)
    api_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"

    import random
    user_agent = random.choice(USER_AGENTS)

    request = urllib.request.Request(api_url)
    request.add_header('User-Agent', user_agent)

    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        with urllib.request.urlopen(request, timeout=timeout, context=ssl_context) as response:
            raw_data = response.read().decode('utf-8', errors='replace')
            data = json.loads(raw_data)

        if not data or 'error' in data:
            return {**result, 'error': 'HN item not found'}

        # Extract post information
        title = data.get('title', '')
        author = data.get('by', '')
        score = data.get('score', 0)
        descendants = data.get('descendants', 0)
        text = data.get('text', '')
        url_post = data.get('url', '')
        time_ts = data.get('time', 0)

        # Build content
        content_parts = [f"# {title}"]
        content_parts.append(f"\n**Posted by** {author}")
        content_parts.append(f"**Points:** {score} | **Comments:** {descendants}")

        if url_post:
            content_parts.append(f"\n**Link:** {url_post}")

        if text:
            # HN text is HTML, strip tags
            clean_text = re_module.sub(r'<[^>]+>', '', text)
            content_parts.append(f"\n---\n\n{clean_text}")

        content = '\n'.join(content_parts)

        # Convert timestamp
        from datetime import timezone
        publish_date = None
        if time_ts:
            try:
                dt = datetime.fromtimestamp(time_ts, tz=timezone.utc)
                publish_date = dt.isoformat()
            except:
                pass

        word_count = len(content.split())

        result.update({
            'success': True,
            'title': title,
            'content': content,
            'content_format': 'markdown',
            'metadata': {
                'author': author,
                'score': score,
                'num_comments': descendants,
                'publish_date': publish_date,
                'external_url': url_post,
            },
            'quality': {
                'word_count': word_count,
                'reading_time_minutes': estimate_reading_time(word_count),
                'has_substantial_content': word_count > 30,
            }
        })

    except Exception as e:
        return {**result, 'error': f"Error fetching HN item: {str(e)}"}

    return result


def requires_browser(url: str) -> bool:
    """Check if URL is from a site known to require browser automation"""
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname or ''

    for site in BROWSER_REQUIRED_SITES:
        if site in hostname:
            return True
    return False


def detect_captcha_or_block(html_content: str, text_content: str) -> bool:
    """Detect if page is showing CAPTCHA or blocking content"""
    lower_html = html_content.lower()
    lower_text = text_content.lower()

    captcha_indicators = [
        'captcha', 'recaptcha', 'hcaptcha', 'turnstile',
        'verify you are human', 'are you a robot', 'please verify',
        'checking your browser', 'just a moment', 'cloudflare',
        'access denied', 'blocked', 'rate limited',
        'enable javascript', 'javascript is disabled',
    ]

    for indicator in captcha_indicators:
        if indicator in lower_html or indicator in lower_text:
            return True

    # Check for very short content (likely blocked)
    if len(text_content.strip()) < 100:
        return True

    return False


def fetch_with_puppeteer(url: str, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    """
    Fetch URL using Puppeteer with stealth plugin.
    Falls back to this when urllib fails or CAPTCHA is detected.
    """
    result = {
        'url': url,
        'fetched_at': datetime.now().isoformat(),
        'success': False,
        'title': None,
        'content': None,
        'content_format': 'text',
        'metadata': {},
        'quality': {
            'word_count': 0,
            'reading_time_minutes': 0,
            'has_substantial_content': False,
        },
        'error': None,
        'method': 'puppeteer-stealth',
    }

    # Check if puppeteer script exists
    if not PUPPETEER_SCRIPT.exists():
        return {**result, 'error': 'Puppeteer script not found. Run: npm install puppeteer puppeteer-extra puppeteer-extra-plugin-stealth'}

    try:
        # Run puppeteer script
        cmd = [
            'node',
            str(PUPPETEER_SCRIPT),
            url,
            '--json',
            '--timeout', str(timeout),
            '--wait', '3'  # Wait 3 seconds for JS to load
        ]

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 30  # Extra time for browser startup
        )

        if proc.returncode != 0:
            return {**result, 'error': f'Puppeteer failed: {proc.stderr}'}

        # Parse JSON output
        puppet_result = json.loads(proc.stdout)

        # Copy results
        result.update({
            'success': puppet_result.get('success', False),
            'title': puppet_result.get('title'),
            'content': puppet_result.get('content'),
            'content_format': puppet_result.get('content_format', 'text'),
            'metadata': puppet_result.get('metadata', {}),
            'quality': puppet_result.get('quality', {}),
            'captcha_detected': puppet_result.get('captcha_detected', False),
            'final_url': puppet_result.get('final_url', url),
            'error': puppet_result.get('error'),
        })

    except subprocess.TimeoutExpired:
        return {**result, 'error': f'Puppeteer timed out after {timeout + 30} seconds'}
    except json.JSONDecodeError as e:
        return {**result, 'error': f'Failed to parse Puppeteer output: {e}'}
    except FileNotFoundError:
        return {**result, 'error': 'Node.js not found. Install Node.js to use browser automation.'}
    except Exception as e:
        return {**result, 'error': f'Puppeteer error: {str(e)}'}

    return result


def fetch_url(url: str, timeout: int = DEFAULT_TIMEOUT, force_browser: bool = False) -> Dict[str, Any]:
    """
    Fetch and parse content from a URL

    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds
        force_browser: Force use of browser automation (Puppeteer)

    Returns:
        dict: Structured content with metadata, text, and quality indicators
    """
    result = {
        'url': url,
        'fetched_at': datetime.now().isoformat(),
        'success': False,
        'title': None,
        'content': None,
        'content_format': 'text',
        'metadata': {},
        'quality': {
            'word_count': 0,
            'reading_time_minutes': 0,
            'has_substantial_content': False,
        },
        'error': None,
        'method': 'urllib',
    }

    # Validate URL
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme:
            url = 'https://' + url
            result['url'] = url
            parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return {**result, 'error': f"Unsupported URL scheme: {parsed.scheme}"}
    except Exception as e:
        return {**result, 'error': f"Invalid URL: {str(e)}"}

    # Check for special site handling
    site_type = detect_site_type(url)
    if site_type == 'reddit':
        result = fetch_reddit_post(url, timeout)
        result['method'] = 'reddit-api'
        return result
    elif site_type == 'hackernews':
        result = fetch_hackernews(url, timeout)
        result['method'] = 'hn-api'
        return result

    # Check if we should use browser from the start
    use_browser = force_browser or requires_browser(url)

    if use_browser:
        print("Using Puppeteer (site requires browser automation)...", file=sys.stderr)
        return fetch_with_puppeteer(url, timeout)

    # Try fetching with urllib first
    import random
    user_agent = random.choice(USER_AGENTS)

    request = urllib.request.Request(url)
    request.add_header('User-Agent', user_agent)
    request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request.add_header('Accept-Language', 'en-US,en;q=0.5')

    html_content = None
    fetch_error = None

    try:
        # Create SSL context with certifi
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        # Make the request
        with urllib.request.urlopen(request, timeout=timeout, context=ssl_context) as response:
            # Check content length
            content_length = response.headers.get('Content-Length')
            if content_length and int(content_length) > MAX_CONTENT_LENGTH:
                return {**result, 'error': f"Content too large: {content_length} bytes (max: {MAX_CONTENT_LENGTH})"}

            # Check content type
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type and 'application/xhtml' not in content_type:
                # For non-HTML content, just return raw text
                raw_content = response.read().decode('utf-8', errors='replace')
                result.update({
                    'success': True,
                    'content': raw_content[:50000],  # Limit to 50k chars
                    'content_format': 'raw',
                    'quality': {
                        'word_count': len(raw_content.split()),
                        'reading_time_minutes': estimate_reading_time(len(raw_content.split())),
                        'has_substantial_content': len(raw_content) > 500,
                    }
                })
                return result

            # Read HTML content
            html_content = response.read().decode('utf-8', errors='replace')

    except urllib.error.HTTPError as e:
        fetch_error = f"HTTP Error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        fetch_error = f"URL Error: {str(e.reason)}"
    except ssl.SSLError as e:
        fetch_error = f"SSL Error: {str(e)}"
    except TimeoutError:
        fetch_error = f"Request timed out after {timeout} seconds"
    except Exception as e:
        fetch_error = f"Unexpected error: {str(e)}"

    # If urllib failed, try Puppeteer as fallback
    if fetch_error:
        print(f"urllib failed ({fetch_error}), trying Puppeteer...", file=sys.stderr)
        puppet_result = fetch_with_puppeteer(url, timeout)
        if puppet_result.get('success'):
            return puppet_result
        # If Puppeteer also failed, return the original error
        return {**result, 'error': fetch_error, 'method': 'urllib-failed'}

    # Extract metadata
    metadata = extract_metadata(html_content, url) # type: ignore
    result['metadata'] = metadata
    result['title'] = metadata.get('title')

    # Parse and extract text
    parser = HTMLToTextParser()
    try:
        parser.feed(html_content) # type: ignore
        text_content = parser.get_text()
    except Exception as e:
        return {**result, 'error': f"HTML parsing error: {str(e)}"}

    # Check for CAPTCHA or blocking indicators
    if detect_captcha_or_block(html_content, text_content): # type: ignore
        print("CAPTCHA/blocking detected, falling back to Puppeteer...", file=sys.stderr)
        puppet_result = fetch_with_puppeteer(url, timeout)
        if puppet_result.get('success'):
            return puppet_result
        # If Puppeteer failed, return the content we got anyway (might still be useful)
        result['warning'] = 'CAPTCHA/blocking detected, Puppeteer fallback failed'

    # Calculate quality metrics
    word_count = len(text_content.split())

    result.update({
        'success': True,
        'content': text_content,
        'content_format': 'text',
        'quality': {
            'word_count': word_count,
            'reading_time_minutes': estimate_reading_time(word_count),
            'has_substantial_content': word_count > 100,
        }
    })

    return result


def format_output(result: Dict[str, Any], output_format: str = 'text') -> str:
    """Format the result for display"""

    if output_format == 'json':
        return json.dumps(result, indent=2, ensure_ascii=False)

    if not result.get('success'):
        return f"Error fetching {result['url']}: {result.get('error', 'Unknown error')}"

    lines = []
    lines.append(f"URL: {result['url']}")
    lines.append(f"Fetched: {result['fetched_at']}")

    if result.get('title'):
        lines.append(f"Title: {result['title']}")

    # Metadata
    meta = result.get('metadata', {})
    if meta.get('author'):
        lines.append(f"Author: {meta['author']}")
    if meta.get('publish_date'):
        lines.append(f"Published: {meta['publish_date']}")
    if meta.get('description'):
        lines.append(f"Description: {meta['description']}")

    # Quality metrics
    quality = result.get('quality', {})
    lines.append(f"\nQuality Metrics:")
    lines.append(f"  Word count: {quality.get('word_count', 0)}")
    lines.append(f"  Reading time: {quality.get('reading_time_minutes', 0)} min")
    lines.append(f"  Substantial: {'Yes' if quality.get('has_substantial_content') else 'No'}")

    # Content
    lines.append("\n" + "="*80)
    lines.append("CONTENT")
    lines.append("="*80)
    lines.append(result.get('content', ''))

    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_url.py <URL> [--json] [--timeout N]")
        print("\nOptions:")
        print("  --json        Output raw JSON results")
        print("  --timeout N   Set timeout to N seconds (default 30)")
        print("\nExamples:")
        print('  python3 fetch_url.py "https://example.com/article"')
        print('  python3 fetch_url.py "https://blog.example.com/post" --json')
        print('  python3 fetch_url.py "https://docs.example.com/api" --timeout 60')
        sys.exit(1)

    # Parse arguments
    url = None
    output_json = False
    timeout = DEFAULT_TIMEOUT

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--json':
            output_json = True
        elif arg == '--timeout':
            if i + 1 < len(sys.argv):
                timeout = int(sys.argv[i + 1])
                i += 1
        elif not arg.startswith('--'):
            url = arg
        i += 1

    if not url:
        print("Error: No URL provided", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching: {url}\n", file=sys.stderr)

    result = fetch_url(url, timeout=timeout)

    if output_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_output(result))


if __name__ == "__main__":
    main()
