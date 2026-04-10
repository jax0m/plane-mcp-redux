# Plane-MCP-Redux - AGENTS.md

## Project Overview

A lean, lazy-loading MCP server for Plane project management using FastMCP 3.x and plane-sdk v0.2.8.

## Architecture

- **Tools**: 30 focused tools (72% reduction from original 109)
- **Lazy Loading**: Dependency injection pattern - client created only when needed
- **FastMCP 3.x**: Modern decorator-based tool registration
- **Type Safety**: Full type hints, mypy + ty checking

## Key Files

- `src/plane_mcp/server.py` - All tool definitions with @mcp.tool
- `src/plane_mcp/client.py` - PlaneClientWrapper (SDK adapter)
- `pyproject.toml` - Dependencies and tool configuration
- `.env` - API credentials

## Common Commands

```bash
# Install
pip install -e ".[dev]"

# Test
pytest tests/ -v

# Type check
ty check src/plane_mcp/
mypy src/plane_mcp/

# Lint/format
ruff check --fix src/ tests/
ruff format src/ tests/

# Run server
pmc

# All checks
make check
```

## Important Patterns

### Tool Definition

```python
@mcp.tool(description="...")
async def list_issues(
    workspace_id: str,
    project_id: str,
    client: PlaneClientWrapper = Depends(get_plane_client),
    ctx: Context | None = None,
) -> dict:
    """Docstring becomes tool description."""
    return client.list_work_items(...)
```

### SDK API Notes

- Use `.model_dump()` not `.to_dict()` (Pydantic v2)
- SDK uses `workspace_slug` not `workspace_id`
- Add `# type: ignore[assignment]` for SDK type stub issues
- Add `# type: ignore[no-untyped-def]` for SDK method calls

### Lazy Loading Pattern

```python
def get_plane_client() -> PlaneClientWrapper:
    """Lazy client creation."""
    config = PlaneConfig()
    return PlaneClientWrapper(
        base_url=config.PLANE_BASE_URL,
        api_key=config.PLANE_API_KEY,
    )
```

### Pre-Commit Workflow (Run occasionally during changes)

```bash
# Normal commit workflow (recommended)
git add <files>
pre-commit run
git commit -m "Your message"
```

## Context Preservation

When the conversation restarts, AGENTS.md will be reloaded with project context.
For long sessions, use `/compact` to summarize older messages.
For branching work, use `/tree` to switch branches with context summaries.
