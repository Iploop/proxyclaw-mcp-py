# ProxyClaw MCP Server (Python)

Model Context Protocol server for [ProxyClaw](https://proxyclaw.ai). It gives AI agents controlled residential-proxy web access, optional browser rendering, and structured extraction workflows for legitimate testing, research, and automation use cases.

## ⚡ Python vs Node.js — Which One?

We ship **two** MCP servers. Choose based on what you need:

| | **This repo (Python)** | **[Node.js version](https://github.com/Iploop/proxyclaw-mcp)** |
|---|---|---|
| **What it does** | Browser rendering + structured extraction | Proxy routing + fetch |
| **Best for** | JS-rendered pages and structured extraction workflows | Simple fetches, geo-targeting |
| **Networking** | Optional TLS-compatible client libraries + Playwright rendering | Standard proxy-backed fetch |
| **Install** | `uvx proxyclaw-mcp-server[all]` | `npx proxyclaw-mcp-server` |
| **Tools** | 6 (+ stealth fetch, render, scrape, extract) | 4 (fetch, check_ip, list_countries, rotate) |

**→ Use Python** if you need JavaScript rendering or structured data extraction from supported sites.

**→ Use Node.js** if you just need to route requests through residential IPs.

Both use the same proxy network — just different levels of power.

## Install

```bash
# Core proxy workflow
pip install proxyclaw-mcp-server

# Optional compatible HTTP clients
pip install proxyclaw-mcp-server[stealth]

# With browser rendering
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
| `proxy_fetch_stealth` | Fetch URL through ProxyClaw with optional compatible HTTP clients + retry |
| `proxy_render` | Headless Chromium render for JavaScript apps and dynamic pages |
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
- **Compatible HTTP clients** — optional curl_cffi / tls_client integrations for more browser-like request behavior
- **Headless rendering** — Playwright rendering for JavaScript-heavy pages
- **Structured extraction** — 60+ site-specific parsers (eBay, Amazon, LinkedIn, Twitter, Nasdaq, etc.)
- **Smart cascade** — tries direct fetch first, escalates to stealth → render → search fallback
- **Sticky sessions** — keep same IP across requests
- **Cookie persistence** — cookies saved between requests
- **Auto-retry with rotation** — configurable retry behavior for transient proxy/network failures

## Security & Trust

- Source code: https://github.com/Iploop/proxyclaw-mcp-py
- Security page: https://proxyclaw.ai/security.html
- The package is a thin MCP adapter around the public `iploop-sdk`; it does not include install hooks, shell execution, credential exfiltration, crypto mining, or obfuscated payloads.
- Runtime credential access is limited to `IPLOOP_API_KEY`, used only to authenticate proxy/API requests.

## Links

- **Website**: [proxyclaw.ai](https://proxyclaw.ai)
- **Security**: [proxyclaw.ai/security.html](https://proxyclaw.ai/security.html)
- **Dashboard**: [iploop.io/dashboard](https://iploop.io/dashboard)
- **Python MCP source**: [Iploop/proxyclaw-mcp-py](https://github.com/Iploop/proxyclaw-mcp-py)
- **Python SDK**: [iploop on PyPI](https://pypi.org/project/iploop-sdk/)
- **Node.js SDK**: [iploop on npm](https://www.npmjs.com/package/iploop)

## License

MIT
