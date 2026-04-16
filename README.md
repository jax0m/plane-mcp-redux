# Plane-MCP-Redux

A lean, lazy-loading MCP (Model Context Protocol) server and CLI for Plane project management.

[![AI-DECLARATION: AI Assistant](https://img.shields.io/badge/䷼%20AI--DECLARATION-AI-fee2e2?labelColor=fee2e2)](AI-DECLARATION.md)

## 🚀 Features

- **CLI & MCP Server**: Full-featured CLI (`plane-rex`) and MCP server for LLM integration
- **Lazy Loading**: SDK imports only when commands execute (~55% faster startup)
- **Error Handling**: Meaningful error messages with pre-checks for update/delete operations
- **Confirmation Flow**: `--autoconfirm` flag for scripting, interactive prompts for CLI
- **Type Safety**: Full mypy type checking, ruff linting
- **Test Suite**: 29 tests (7 unit + 22 integration) with real API

## 📦 Project Structure

```
plane-mcp-redux/
├── pyproject.toml          # Project configuration & dependencies
├── src/plane_mcp/          # Main package
│   ├── __init__.py
│   ├── main.py             # CLI entry point
│   ├── cli.py              # Click-based CLI (22 commands)
│   ├── server.py           # FastMCP server (13 tools)
│   └── client.py           # Plane API client wrapper
├── tests/                  # Test suite
│   ├── test_server.py      # Unit tests (7 tests)
│   └── test_integration.py # Integration tests (22 tests)
├── docs/                   # Documentation
│   ├── SDK_COVERAGE.md     # SDK coverage tracking
│   └── makeplane_plane-python-sdk/  # SDK documentation
└── IMPLEMENTATION_SUMMARY.md  # Latest session summary
```

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- Plane API credentials (see `.env.example`)

### Install Dependencies

```bash
# Using pip
pip install -e ".[dev]"

# Install globally for CLI access
pip install -e ".[dev]"
```

### Configure Environment

Create a `.env` file in the project root:

```bash
PLANE_BASE_URL=https://your-plane-instance.com
PLANE_API_KEY=your_plane_api_key_here
PLANE_WORKSPACE_SLUG=your_workspace_slug
```

## 🚦 Usage

### CLI Commands

```bash
# List projects
plane-rex project list

# Create project
plane-rex project create "My Project" -i MYPROJ

# View project
plane-rex project info <project-id>

# List work items in project
plane-rex work list -p <project-id>

# Create work item
plane-rex work add "Fix bug" -p <project-id> --priority high

# View work item details
plane-rex work info <work-item-id> -p <project-id>

# See your assigned tasks across all projects
plane-rex work my-tasks

# Create sticky note (workspace-level)
plane-rex sticky create "Remember this!" --color peach

# List states in project
plane-rex state list -p <project-id>

# Auto-confirm for scripting
plane-rex --autoconfirm project delete <id>
```

### MCP Server

```bash
# Run MCP server
python -m plane_mcp.server

# Or with fastmcp
fastmcp dev inspector src/plane_mcp/server.py
```

### MCP Client Configuration

Add to your MCP client configuration:

```json
{
    "mcpServers": {
        "plane": {
            "command": "python",
            "args": ["-m", "plane_mcp.server"],
            "env": {
                "PLANE_BASE_URL": "https://your-plane-instance.com",
                "PLANE_API_KEY": "your_api_key",
                "PLANE_WORKSPACE_SLUG": "your_workspace"
            }
        }
    }
}
```

## 📚 Available Commands

### Projects (4/8)

| Command                                 | Description         |
| --------------------------------------- | ------------------- |
| `plane-rex project list`                | List all projects   |
| `plane-rex project create "Name" -i ID` | Create new project  |
| `plane-rex project info <id>`           | Get project details |
| `plane-rex project delete <id>`         | Delete project      |

### Work Items (5/13)

| Command                                            | Description            |
| -------------------------------------------------- | ---------------------- |
| `plane-rex work list -p <project>`                 | List work items        |
| `plane-rex work add "Title" -p <project>`          | Create work item       |
| `plane-rex work info <id> -p <project>`            | View work item details |
| `plane-rex work update <id> -p <project> -n "New"` | Update work item       |
| `plane-rex work delete <id> -p <project>`          | Delete work item       |
| `plane-rex work my-tasks`                          | Your assigned tasks    |

### Labels (3/6)

| Command                                      | Description        |
| -------------------------------------------- | ------------------ |
| `plane-rex label list -p <project>`          | List labels        |
| `plane-rex label create "Name" -p <project>` | Create label       |
| `plane-rex label info <id> -p <project>`     | View label details |

### Stickies (5/5) - Workspace-level

| Command                                        | Description         |
| ---------------------------------------------- | ------------------- |
| `plane-rex sticky list`                        | List all stickies   |
| `plane-rex sticky create "Content"`            | Create sticky       |
| `plane-rex sticky info <id>`                   | View sticky details |
| `plane-rex sticky update <id> --content "New"` | Update sticky       |
| `plane-rex sticky delete <id>`                 | Delete sticky       |

### States (5/5)

| Command                                                 | Description        |
| ------------------------------------------------------- | ------------------ |
| `plane-rex state list -p <project>`                     | List states        |
| `plane-rex state create "Name" -p <project>`            | Create state       |
| `plane-rex state info <id> -p <project>`                | View state details |
| `plane-rex state update <id> -p <project> --name "New"` | Update state       |
| `plane-rex state delete <id> -p <project>`              | Delete state       |

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Unit tests only (no API calls)
pytest tests/test_server.py -v

# Integration tests only (requires .env)
pytest tests/test_integration.py -v

# With coverage
pytest tests/ -v --cov=src/plane_mcp
```

## 🔧 Development

### Type Checking

```bash
# Check all source files
mypy src/plane_mcp/ tests/

# Should pass with no errors
```

### Linting & Formatting

```bash
# Check and fix issues
ruff check --fix src/ tests/

# Format code
ruff format src/ tests/
```

### Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 📊 Coverage Status

| Resource   | CLI Commands | MCP Tools | Coverage |
| ---------- | ------------ | --------- | -------- |
| Projects   | 4/8          | 4/8       | 50%      |
| Work Items | 5/13         | 5/13      | 38%      |
| Labels     | 3/6          | 4/6       | 50%      |
| Stickies   | 5/5          | 0/5       | 100% CLI |
| States     | 5/5          | 0/5       | 100% CLI |
| **TOTAL**  | **22/50**    | **13/50** | **44%**  |

See [docs/SDK_COVERAGE.md](docs/SDK_COVERAGE.md) for detailed tracking.

## 📖 Configuration Options

| Variable               | Default                | Description            |
| ---------------------- | ---------------------- | ---------------------- |
| `PLANE_BASE_URL`       | `https://api.plane.so` | Plane API base URL     |
| `PLANE_API_KEY`        | (required)             | Your Plane API key     |
| `PLANE_WORKSPACE_SLUG` | `workspace`            | Default workspace slug |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/name`
3. Make your changes
4. Run tests: `pytest tests/ -v`
5. Format code: `ruff check --fix && ruff format`
6. Type check: `mypy src/plane_mcp/`
7. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Links

- [Plane Documentation](https://github.com/makeplane/plane)
- [Plane Python SDK](https://github.com/makeplane/plane-python-sdk)
- [FastMCP Documentation](https://github.com/aitomatic-labs/fastmcp)
- [MCP Specification](https://modelcontextprotocol.io)

---

**Last Updated**: 2026-04-14
**Version**: 0.2.0
