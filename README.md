# Plane-MCP-Redux

A lean, lazy-loading MCP (Model Context Protocol) server for Plane project management. This implementation focuses on reducing context size by only loading tools on-demand, making it much more efficient than the original 109-tool implementation.

[![AI-DECLARATION: copilot](https://img.shields.io/badge/䷼%20AI--DECLARATION-copilot-fee2e2?labelColor=fee2e2)](https://ai-declaration.md)

## 🚀 Features

- **Lazy Loading**: Tools are only loaded when needed, significantly reducing LLM context size
- **Tool Categories**: Organized tools by category (workspace, project, issue, cycle, etc.)
- **Modern Python**: Built with FastMCP 2.0+ and the latest Plane SDK
- **Type Safety**: Full type hints and pydantic validation
- **Modular Design**: Easy to extend with new tools

## 📦 Project Structure

```
plane-mcp-redux/
├── pyproject.toml          # Project configuration & dependencies
├── src/plane_mcp/   # Main package
│   ├── __init__.py
│   ├── main.py             # Entry point
│   ├── server.py           # Core MCP server with lazy loading
│   ├── client.py           # Plane API client wrapper
│   └── tools/              # Tool implementations
│       ├── __init__.py
│       ├── base.py         # Base tool classes & registry
│       ├── workspace.py    # Workspace tools
│       ├── project.py      # Project tools
│       ├── issue.py        # Issue tracking tools
│       ├── cycle.py        # Cycle/sprint tools
│       ├── module.py       # Module tools
│       ├── page.py         # Page tools
│       ├── state.py        # State management tools
│       └── member.py       # Member tools
└── tests/                  # Test suite
    ├── __init__.py
    └── test_server.py
```

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- Plane API credentials (see `.env.example`)

### Install Dependencies

```bash
# Using pip
pip install -e ".[dev]"

# Using uv (recommended)
uv sync --all-extras
```

### Configure Environment

Create a `.env` file in the project root:

```bash
PLANE_BASE_URL=https://api.plane.so
PLANE_API_KEY=your_plane_api_key_here
PLANE_WORKSPACE_SLUG=your_workspace_slug
```

## 🚦 Usage

### Running the Server

```bash
# Standard mode
python -m plane_mcp

# Or using the entry point
pmc
```

### MCP Client Configuration

Add to your MCP client configuration:

```json
{
    "mcpServers": {
        "plane": {
            "command": "python",
            "args": ["-m", "plane_mcp"],
            "env": {
                "PLANE_BASE_URL": "https://api.plane.so",
                "PLANE_API_KEY": "your_api_key",
                "PLANE_WORKSPACE_SLUG": "your_workspace"
            }
        }
    }
}
```

## 📚 Available Tools

### Workspace

- `list_workspaces` - List all accessible workspaces
- `get_workspace` - Get workspace details

### Project

- `list_projects` - List projects in a workspace
- `get_project` - Get project details
- `create_project` - Create a new project
- `update_project` - Update project settings

### Issue (Most Commonly Used)

- `list_issues` - List issues with filters
- `get_issue` - Get issue details
- `create_issue` - Create a new issue
- `update_issue` - Update issue properties
- `delete_issue` - Delete an issue
- `assign_issue` - Assign issue to user
- `link_issue` - Link related issues
- `search_issues` - Search across issues
- `update_issue_state` - Change issue status

### Cycle (Sprints)

- `list_cycles` - List project cycles
- `get_cycle` - Get cycle details
- `create_cycle` - Create a new cycle
- `update_cycle` - Update cycle

### Module

- `list_modules` - List project modules
- `get_module` - Get module details

### Page (Documentation)

- `list_pages` - List workspace pages
- `get_page` - Get page content
- `create_page` - Create documentation page
- `update_page` - Update page

### State

- `list_states` - List available issue states

### Member

- `list_members` - List workspace members
- `get_member` - Get member details

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/plane_mcp

# Run specific test file
pytest tests/test_server.py -v
```

## 🔧 Extending with New Tools

1. Create a new file in `src/plane_mcp/tools/`

```python
# src/plane_mcp/tools/label.py
from .base import PlaneTool

class LabelTool(PlaneTool):
    name = "list_labels"
    description = "List all labels in a project"
    categories = ["label"]

    async def execute(self, workspace_id: str, project_id: str):
        # Implement your tool logic
        return {"labels": []}
```

2. Update `pyproject.toml` to include your tool

```toml
[tool.pmc]
enabled_tools = [
    # ... existing tools
    "list_labels",
]
```

3. Register the tool in `server.py`

```python
from .tools.label import ListLabelsTool, list_labels as list_labels_handler

# In PlaneMCP.__init__:
self._registry.register_handler("list_labels", list_labels_handler)
```

## 📖 Configuration Options

| Variable               | Default                | Description            |
| ---------------------- | ---------------------- | ---------------------- |
| `PLANE_BASE_URL`       | `https://api.plane.so` | Plane API base URL     |
| `PLANE_API_KEY`        | (required)             | Your Plane API key     |
| `PLANE_WORKSPACE_SLUG` | `workspace`            | Default workspace slug |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Format code: `ruff check --fix && ruff format`
6. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Links

- [Plane Documentation](https://github.com/makeplane/plane)
- [FastMCP Documentation](https://github.com/bytebase/mcp)
- [MCP Specification](https://modelcontextprotocol.io)
