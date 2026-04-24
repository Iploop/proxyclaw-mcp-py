"""ProxyClaw MCP Server — Python adapter around the iploop SDK."""

__version__ = "1.0.0"

from .server import main_sync as main

__all__ = ["main"]
