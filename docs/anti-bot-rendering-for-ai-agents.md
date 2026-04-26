# Anti-bot Rendering for AI Agents with ProxyClaw MCP Python

Most AI web tools can fetch a URL. That is not enough when a page needs JavaScript rendering, regional residential IPs, or anti-bot-aware networking.

ProxyClaw MCP Python gives Claude Desktop, Cursor, Zed, and other MCP clients a stronger web access layer:

- residential proxy routing
- stealth fetch workflows
- Playwright rendering
- structured extraction
- country targeting
- exit IP verification

## Install

```bash
uvx proxyclaw-mcp-server[all]
```

## MCP config

```json
{
  "mcpServers": {
    "proxyclaw-python": {
      "command": "uvx",
      "args": ["proxyclaw-mcp-server[all]"],
      "env": {
        "IPLOOP_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Get a free key: https://iploop.io/signup.html

## Tools

- `proxy_fetch_stealth`
- `proxy_render`
- `proxy_scrape`
- `proxy_extract`
- `proxy_check_ip`
- `proxy_list_countries`

## Links

- Python MCP: https://github.com/Iploop/proxyclaw-mcp-py
- Node MCP: https://github.com/Iploop/proxyclaw-mcp
- Docs: https://proxyclaw.ai/docs
- PyPI: https://pypi.org/project/proxyclaw-mcp-server/
