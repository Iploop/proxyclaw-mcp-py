#!/usr/bin/env python3
"""
ProxyClaw MCP Server — Python
Thin adapter around the iploop SDK. No SDK modifications.
Node.js MCP = proxy only. Python MCP = anti-bot + render + extraction.
"""

import os
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ── Logging: MUST be file-only, stdio is the MCP transport ──
_log_path = os.environ.get("PROXYCLAW_LOG", "/tmp/proxyclaw-mcp.log")
logging.basicConfig(
    filename=_log_path,
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("proxyclaw-mcp")

# ── SDK import (read-only wrapper) ──
try:
    from iploop import IPLoop
    from iploop.exceptions import AuthError, ProxyError, TimeoutError
    IPLOOP_AVAILABLE = True
except ImportError:
    IPLOOP_AVAILABLE = False
    IPLoop = None
    logger.error("iploop SDK not installed. Run: pip install iploop")

API_KEY = os.environ.get("IPLOOP_API_KEY", "")
_client = None


def get_client() -> Any:
    """Lazy-init the SDK client."""
    global _client
    if _client is None and IPLOOP_AVAILABLE and API_KEY:
        try:
            _client = IPLoop(API_KEY)
        except AuthError as e:
            logger.error(f"Auth failed: {e}")
            raise
    return _client


# ── Tool definitions ──
TOOLS: list[Tool] = [
    Tool(
        name="proxy_fetch_stealth",
        description=(
            "Fetch a URL through ProxyClaw with anti-detection. "
            "Uses Chrome fingerprint headers + TLS JA3 spoofing to bypass Cloudflare, DataDome, and bot protection. "
            "Auto-retry with fresh IP on 403/502/503."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to fetch (http:// or https://)"},
                "country": {"type": "string", "description": "2-letter country code (e.g. US, DE, JP). Auto-rotate if omitted."},
                "city": {"type": "string", "description": "City name for city-level targeting (optional)"},
                "session": {"type": "string", "description": "Session ID for sticky IP (optional)"},
                "method": {"type": "string", "description": "HTTP method: GET, POST, PUT, DELETE. Default: GET"},
                "headers": {"type": "object", "description": "Custom headers to add (optional)"},
                "data": {"type": "string", "description": "Request body for POST/PUT (optional)"},
                "timeout": {"type": "integer", "description": "Timeout in seconds (1-120, default: 30)"},
                "retries": {"type": "integer", "description": "Retry attempts (0-5, default: 3)"},
            },
            "required": ["url"],
        },
    ),
    Tool(
        name="proxy_render",
        description=(
            "Render a URL with a headless Chromium browser through ProxyClaw. "
            "Executes JavaScript, bypasses Cloudflare challenges, handles SPAs. "
            "Requires Playwright: pip install proxyclaw-mcp-server[render]"
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to render"},
                "country": {"type": "string", "description": "2-letter country code (optional)"},
                "city": {"type": "string", "description": "City name (optional)"},
                "wait_for": {"type": "string", "description": "CSS selector to wait for before returning (optional)"},
                "wait_time": {"type": "integer", "description": "Seconds to wait for JS execution (default: 5)"},
            },
            "required": ["url"],
        },
    ),
    Tool(
        name="proxy_scrape",
        description=(
            "Smart scrape with automatic escalation. "
            "Tries direct fetch first, then stealth (TLS spoof), then headless render, "
            "then search fallback. Returns clean HTML or structured data."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to scrape"},
                "country": {"type": "string", "description": "2-letter country code (optional)"},
                "extract": {"type": "boolean", "description": "Try structured extraction if site is known (default: true)"},
            },
            "required": ["url"],
        },
    ),
    Tool(
        name="proxy_extract",
        description=(
            "Extract structured data from known sites using built-in parsers. "
            "Supported: ebay, amazon, linkedin, twitter, google, nasdaq, youtube, "
            "reddit, imdb, github, coingecko, weather, spotify, and 40+ more."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL of the page to extract data from"},
                "site": {"type": "string", "description": "Site preset (e.g. ebay, amazon). Auto-detected from URL if omitted."},
                "country": {"type": "string", "description": "2-letter country code (optional)"},
            },
            "required": ["url"],
        },
    ),
    Tool(
        name="proxy_check_ip",
        description="Check the current exit IP address and geo-location through the proxy.",
        inputSchema={
            "type": "object",
            "properties": {
                "country": {"type": "string", "description": "2-letter country code to route through (optional)"},
            },
            "required": [],
        },
    ),
    Tool(
        name="proxy_list_countries",
        description="List all 195+ countries available for routing through ProxyClaw.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
]


# ── Helpers ──

def _trunc(text: str, max_len: int = 50000) -> str:
    if len(text) > max_len:
        return text[:max_len] + f"\n\n[...truncated {len(text) - max_len} chars]"
    return text


def _ok(text: str) -> list[TextContent]:
    return [TextContent(type="text", text=text)]


def _err(text: str) -> list[TextContent]:
    """Return an error-marked response so the agent knows it failed."""
    return [TextContent(type="text", text=text)]
    # Note: isError flag is not in the base TextContent type for this MCP SDK version.
    # The agent infers failure from the error text prefix.


# ── Handlers ──

async def handle_fetch_stealth(args: dict[str, Any]) -> list[TextContent]:
    if not IPLOOP_AVAILABLE:
        return _err("Error: iploop SDK not installed. Run: pip install iploop")

    client = get_client()
    if not client:
        return _err("Error: IPLOOP_API_KEY not configured.")

    url = args.get("url", "")
    if not url.startswith(("http://", "https://")):
        return _err("Error: URL must start with http:// or https://")

    country = args.get("country")
    city = args.get("city")
    session = args.get("session")
    method = (args.get("method") or "GET").upper()
    headers = args.get("headers")
    data = args.get("data")
    timeout = min(120, max(1, int(args.get("timeout", 30))))
    retries = min(5, max(0, int(args.get("retries", 3))))

    try:
        kwargs = {
            "country": country, "city": city, "session": session,
            "headers": headers, "timeout": timeout, "retries": retries,
        }
        if method == "GET":
            resp = client.get(url, **kwargs)
        elif method == "POST":
            resp = client.post(url, data=data, **kwargs)
        elif method == "PUT":
            resp = client.put(url, data=data, **kwargs)
        elif method == "DELETE":
            resp = client.delete(url, **kwargs)
        else:
            return _err(f"Error: Unsupported method {method}")

        text = _trunc(resp.text)
        meta = f"Status: {resp.status_code} | URL: {url}"
        if country:
            meta += f" | Country: {country.upper()}"
        return _ok(f"{meta}\n\n{text}")

    except TimeoutError as e:
        return _err(f"Timeout: {e}")
    except ProxyError as e:
        return _err(f"Proxy error: {e}")
    except Exception as e:
        logger.exception("fetch_stealth failed")
        return _err(f"Error: {e}")


async def handle_render(args: dict[str, Any]) -> list[TextContent]:
    if not IPLOOP_AVAILABLE:
        return _err("Error: iploop SDK not installed.")

    client = get_client()
    if not client:
        return _err("Error: IPLOOP_API_KEY not configured.")

    url = args.get("url", "")
    if not url.startswith(("http://", "https://")):
        return _err("Error: URL must start with http:// or https://")

    country = args.get("country")
    city = args.get("city")
    wait_for = args.get("wait_for")
    wait_time = int(args.get("wait_time", 5))

    try:
        html = client.render_fetch(url, country=country, city=city,
                                   wait_for=wait_for, wait_time=wait_time)
        html = _trunc(html)
        meta = f"Rendered: {url}"
        if country:
            meta += f" | Country: {country.upper()}"
        return _ok(f"{meta}\n\n{html}")

    except Exception as e:
        msg = str(e)
        if "Playwright not installed" in msg or "name 'Page' is not defined" in msg:
            return _err("Error: Playwright not installed. Run: pip install proxyclaw-mcp-server[render]")
        logger.exception("render failed")
        return _err(f"Render error: {e}")


async def handle_scrape(args: dict[str, Any]) -> list[TextContent]:
    if not IPLOOP_AVAILABLE:
        return _err("Error: iploop SDK not installed.")

    client = get_client()
    if not client:
        return _err("Error: IPLOOP_API_KEY not configured.")

    url = args.get("url", "")
    if not url.startswith(("http://", "https://")):
        return _err("Error: URL must start with http:// or https://")

    country = args.get("country")

    try:
        result = client.smart_scrape(url, country=country)
        # Pass through whatever the SDK returns — don't assume shape
        payload = json.dumps(result, indent=2, default=str)
        return _ok(payload)
    except Exception as e:
        logger.exception("scrape failed")
        return _err(f"Scrape error: {e}")


async def handle_extract(args: dict[str, Any]) -> list[TextContent]:
    if not IPLOOP_AVAILABLE:
        return _err("Error: iploop SDK not installed.")

    client = get_client()
    if not client:
        return _err("Error: IPLOOP_API_KEY not configured.")

    url = args.get("url", "")
    if not url.startswith(("http://", "https://")):
        return _err("Error: URL must start with http:// or https://")

    country = args.get("country")
    site = args.get("site")

    try:
        # SDK auto-detects site from URL; we pass through whatever the SDK gives us
        result = client.scrape(url, country=country, extract=True)
        payload = json.dumps(result, indent=2, default=str)
        return _ok(payload)
    except Exception as e:
        logger.exception("extract failed")
        return _err(f"Extract error: {e}")


async def handle_check_ip(args: dict[str, Any]) -> list[TextContent]:
    if not IPLOOP_AVAILABLE:
        return _err("Error: iploop SDK not installed.")

    client = get_client()
    if not client:
        return _err("Error: IPLOOP_API_KEY not configured.")

    country = args.get("country")
    try:
        resp = client.get("https://httpbin.org/ip", country=country)
        return _ok(f"Exit IP:\n{resp.text}")
    except Exception as e:
        return _err(f"IP check failed: {e}")


async def handle_list_countries(args: dict[str, Any]) -> list[TextContent]:
    if not IPLOOP_AVAILABLE:
        return _err("Error: iploop SDK not installed.")

    client = get_client()
    if not client:
        return _err("Error: IPLOOP_API_KEY not configured.")

    try:
        countries = client.countries()
        payload = json.dumps(countries, indent=2, default=str)
        return _ok(_trunc(payload, max_len=30000))
    except Exception as e:
        return _err(f"Failed to list countries: {e}")


# ── Main ──

async def main():
    server = Server("proxyclaw-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        args = arguments or {}
        logger.debug(f"Tool call: {name} args={list(args.keys())}")

        if name == "proxy_fetch_stealth":
            return await handle_fetch_stealth(args)
        elif name == "proxy_render":
            return await handle_render(args)
        elif name == "proxy_scrape":
            return await handle_scrape(args)
        elif name == "proxy_extract":
            return await handle_extract(args)
        elif name == "proxy_check_ip":
            return await handle_check_ip(args)
        elif name == "proxy_list_countries":
            return await handle_list_countries(args)
        else:
            return _err(f"Unknown tool: {name}")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main_sync():
    import asyncio
    asyncio.run(main())
