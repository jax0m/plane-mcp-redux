# Plane-MCP-Redux - AGENTS.md

## Project Overview

A lean, lazy-loading MCP server and CLI for Plane project management using FastMCP 3.x and plane-sdk v0.2.8.

**Current Status**: Phase 2 complete - Stickies, States, View commands, User worklist implemented

## Architecture

- **CLI**: 22 Click-based commands (`plane-rex`)
- **MCP**: 13 FastMCP tools (server.py)
- **Lazy Loading**: SDK imports only when commands execute (~55% faster startup)
- **Error Handling**: Pre-checks for update/delete, meaningful error messages
- **Confirmation Flow**: `--autoconfirm` flag for scripting
- **Type Safety**: Full mypy type checking, ruff linting
- **Test Suite**: 29 tests (7 unit + 22 integration)

## Key Files

- `src/plane_mcp/cli.py` - Click-based CLI (22 commands)
- `src/plane_mcp/server.py` - FastMCP tools with error handling
- `src/plane_mcp/main.py` - CLI entry point
- `tests/test_server.py` - Unit tests (7 tests)
- `tests/test_integration.py` - Integration tests (22 tests)
- `docs/SDK_COVERAGE.md` - SDK coverage tracking
- `IMPLEMENTATION_SUMMARY.md` - Latest session summary

## Common Commands

```bash
# Install
pip install -e ".[dev]"

# CLI usage
plane-rex project list
plane-rex work my-tasks
plane-rex sticky create "Test"
plane-rex state list -p <project>

# Test
pytest tests/ -v
pytest tests/test_server.py -v
pytest tests/test_integration.py -v

# Type check
mypy src/plane_mcp/ tests/

# Lint/format
ruff check --fix src/ tests/
ruff format src/ tests/

# Run MCP server
python -m plane_mcp.server

# All checks
make check
```

## Important Patterns

### Tool Definition (MCP)

```python
@mcp.tool(description="List all projects in workspace")
async def project_list() -> list[dict]:
    """List all projects in the configured workspace."""
    try:
        client = get_plane_client()
        from plane.models.query_params import PaginatedQueryParams

        projects = client.projects.list(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            params=PaginatedQueryParams(per_page=20),
        )
        return [{"id": p.id, "name": p.name} for p in projects.results]
    except Exception as e:
        handle_api_error(e)
```

### CLI Command (Click)

```python
@project.command(name="list")
def project_list():
    """List all projects in workspace"""
    try:
        click.echo("Fetching projects...")
        projects = _get_projects()
        for p in projects[:10]:
            click.echo(f"  [{p.id}] {p.name} ({p.identifier})")
    except Exception as e:
        handle_error(e)
```

### Error Handling

```python
def handle_api_error(error: Exception) -> NoReturn:
    if isinstance(error, HttpError):
        if error.status_code == 404:
            raise ToolError("❌ Not Found\n   - Resource doesn't exist")
        # ... more status codes
    raise ToolError(f"❌ Unexpected error: {type(error).__name__}")
```

### Pre-Check Pattern

```python
def project_exists(project_id: str, client) -> bool:
    try:
        client.projects.retrieve(workspace_slug=settings.PLANE_WORKSPACE_SLUG, project_id=project_id)
        return True
    except HttpError:
        return False
    except Exception:
        return False

# Usage in command
if not project_exists(project_id, client):
    raise click.ClickException(f"❌ Project not found: {project_id}")
```

### SDK API Notes

- Use `.model_dump()` not `.to_dict()` (Pydantic v2)
- SDK uses `workspace_slug` not `workspace_id`
- Lazy imports for performance (import inside functions)
- Minimal `# type: ignore` (only for SDK incompatibilities)

### Lazy Loading Pattern

```python
def get_plane_client():
    """Lazy client initialization."""
    global _plane_client
    if _plane_client is None:
        from plane.client.plane_client import PlaneClient
        _plane_client = PlaneClient(
            base_url=settings.PLANE_BASE_URL,
            api_key=settings.PLANE_API_KEY,
        )
    return _plane_client
```

## Coverage Summary

| Resource   | CLI       | MCP       | Coverage |
| ---------- | --------- | --------- | -------- |
| Projects   | 4/8       | 4/8       | 50%      |
| Work Items | 5/13      | 5/13      | 38%      |
| Labels     | 3/6       | 4/6       | 50%      |
| Stickies   | 5/5       | 0/5       | 100% CLI |
| States     | 5/5       | 0/5       | 100% CLI |
| **TOTAL**  | **22/50** | **13/50** | **44%**  |

## Context Preservation

When the conversation restarts, AGENTS.md will be reloaded with project context.
For long sessions, use `/compact` to summarize older messages.

## Session Continuity

For development planning and session context, see:

- `.pi/plans/DEVELOPMENT_PLAN.md` - Complete development roadmap
- `.pi/plans/SESSION_CHECKLIST.md` - Session startup checklist
- `IMPLEMENTATION_SUMMARY.md` - Latest session summary
- `docs/SDK_COVERAGE.md` - SDK coverage tracking

These files are automatically loaded by the pi coding agent to maintain context across sessions.

---

**Last Updated**: 2026-04-14
**Version**: 2.0.0
