"""
Plane MCP Redux CLI Entry Point

Usage:
    plane-rex <command> [options]

Examples:
    plane-rex project list
    plane-rex work add "Fix bug" --project my-project
    plane-rex label create "Bug" --project my-project
"""

from click import main as click_main

if __name__ == "__main__":
    # Run the click CLI
    click_main("plane_mcp.cli:cli")
