# ProxyClaw MCP Server (Python)

Model Context Protocol server for [ProxyClaw](https://proxyclaw.ai) — the most powerful web access tool for AI agents. Route requests through 175M+ residential IPs with TLS fingerprint spoofing, headless browser rendering, and structured data extraction.

## ⚡ Python vs Node.js — Which One?

We ship **two** MCP servers. Choose based on what you need:

| | **This repo (Python)** | **[Node.js version](https://github.com/Iploop/proxyclaw-mcp)** |
|---|---|---|
| **What it does** | Full anti-bot + headless render + structured extraction | Proxy routing + fetch |
| **Best for** | Scraping protected sites (Amazon, eBay, LinkedIn), JS-rendered pages | Simple fetches, geo-targeting |
| **Anti-detection** | TLS JA3 spoofing + Playwright anti-detection | Chrome fingerprint headers |
| **Install** | `uvx proxyclaw-mcp-server[all]` | `npx proxyclaw-mcp-server` |
| **Tools** | 6 (+ stealth fetch, render, scrape, extract) | 4 (fetch, check_ip, list_countries, rotate) |

**→ Use Python** if you're scraping hard targets (Cloudflare, SPAs, React sites) or need structured data extraction from 60+ supported sites.

**→ Use Node.js** if you just need to route requests through residential IPs.

Both use the same proxy network — just different levels of power.

## Install

```bash
# Core (proxy + stealth headers + auto-retry)
pip install proxyclaw-mcp-server[stealth]

# With rendering (Playwright anti-detection)
pip install proxyclaw-mcp-server[all]

# Or via uv (Claude Desktop recommended)
uv tool install proxyclaw-mcp-server[all]
```

## Claude Desktop Config

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "proxyclaw": {
      "command": "uvx",
      "args": ["proxyclaw-mcp-server[all]"],
      "env": {
        "IPLOOP_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Tools

| Tool | What it does |
|------|-------------|
| `proxy_fetch_stealth` | Fetch URL with Chrome fingerprint + TLS JA3 spoofing + auto-retry |
| `proxy_render` | Full headless Chromium render — bypasses Cloudflare, JS apps, SPAs |
| `proxy_scrape` | Smart cascade: direct → stealth → render → search fallback |
| `proxy_extract` | Structured data from 60+ sites (eBay, Amazon, LinkedIn, Google, Nasdaq, etc.) |
| `proxy_check_ip` | Verify exit IP and geo-location |
| `proxy_list_countries` | List 195+ available countries |

## Quick Start

Get your API key at [iploop.io/signup](https://iploop.io/signup.html).

Then ask Claude:

> "Fetch https://example.com through a German IP with stealth headers"

> "Render https://spa-site.com and extract the product title"

> "Scrape eBay search results for 'laptop' and return structured data"

## Features

- **Residential proxy network** — 175M+ real IPs across 195+ countries
- **TLS fingerprint spoofing** — curl_cffi / tls_client for JA3 bypass (Cloudflare can't detect you)
- **Headless rendering** — Playwright with anti-detection (removes webdriver, mocks plugins, fake Chrome runtime)
- **Structured extraction** — 60+ site-specific parsers (eBay, Amazon, LinkedIn, Twitter, Nasdaq, etc.)
- **Smart cascade** — tries direct fetch first, escalates to stealth → render → search fallback
- **Sticky sessions** — keep same IP across requests
- **Cookie persistence** — cookies saved between requests
- **Auto-retry with rotation** — 403/502/503 automatically retries with fresh IP

## Links

- **Website**: [proxyclaw.ai](https://proxyclaw.ai)
- **Dashboard**: [iploop.io/dashboard](https://iploop.io/dashboard)
- **Python SDK**: [iploop on PyPI](https://pypi.org/project/iploop-sdk/)
- **Node.js SDK**: [iploop on npm](https://www.npmjs.com/package/iploop)

## License

MIT
