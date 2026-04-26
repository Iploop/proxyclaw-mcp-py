# Security Policy

ProxyClaw MCP Server is an open-source MCP adapter for ProxyClaw/IPLoop residential proxy workflows.

## Package identity

- PyPI package: `proxyclaw-mcp-server`
- Source repository: https://github.com/Iploop/proxyclaw-mcp-py
- Website: https://proxyclaw.ai
- Security page: https://proxyclaw.ai/security.html
- Maintainer: IPLoop / ProxyClaw

## What the package does

The package exposes MCP tools that call the public `iploop-sdk` for:

- residential proxy-backed fetches
- optional browser rendering with Playwright
- structured extraction workflows
- exit IP / country listing utilities

## What the package does not do

The package does not contain:

- install-time execution hooks
- shell command execution
- obfuscated payloads
- credential harvesting
- crypto mining
- persistence mechanisms
- outbound calls unrelated to ProxyClaw/IPLoop SDK functionality

Runtime credential access is limited to `IPLOOP_API_KEY`, used to authenticate requests to IPLoop/ProxyClaw services.

## Reporting security issues

Please report security concerns privately to:

- support@iploop.io

Include package name, version, reproduction steps, and any indicators/evidence.
