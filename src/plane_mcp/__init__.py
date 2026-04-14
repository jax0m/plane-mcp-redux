"""Plane MCP Server - A lean, lazy-loading MCP server for Plane project management."""

__version__ = "0.1.0"
__author__ = "Your Name"

from .client import PlaneClientWrapper
from .server import mcp

__all__ = ["mcp", "PlaneClientWrapper"]
