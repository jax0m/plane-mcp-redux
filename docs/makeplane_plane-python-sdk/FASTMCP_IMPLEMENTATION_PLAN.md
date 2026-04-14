# FastMCP Implementation Plan for plane-mcp-redux

**Created**: 2026-04-14T01:30:00Z
**Owner**: AI Assistant
**Status**: Planning
**Version**: 0.1.0

---

## Goals

1. **Workflow-Oriented CLI**: Intuitive commands like `plane work add "Fix bug"`
2. **Lazy Loading**: Efficient client initialization
3. **FastMCP 3.x**: Modern decorator-based tool registration
4. **Interactive Prompts**: User-friendly input collection
5. **Type Safety**: Full type hints with mypy + ty

---

## Implementation Phases

### Phase 1: Core Infrastructure

#### 1.1 Project Structure

```
src/plane_mcp/
├── __init__.py
├── main.py              # Entry point
├── client.py            # Lazy client wrapper
├── server.py            # FastMCP server
├── commands/
│   ├── __init__.py
│   ├── project.py
│   ├── work.py
│   ├── label.py
│   ├── module.py
│   └── cycle.py
├── prompts/
│   ├── __init__.py
│   ├── create_work.py
│   └── list_work.py
└── utils/
    ├── __init__.py
    └── lazy.py
```

#### 1.2 Client Wrapper

**File**: `src/plane_mcp/client.py`

```python
"""Plane SDK client wrapper with lazy initialization."""

from typing import Optional
from plane_sdk import PlaneClientWrapper
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PLANE_BASE_URL: str = "https://api.plane.so"
    PLANE_API_KEY: str
    PLANE_WORKSPACE_SLUG: str

    class Config:
        env_file = ".env"

class PlaneClientWrapper:
    """Lazy Plane SDK client wrapper."""

    _instance: Optional[PlaneClientWrapper] = None
    _settings: Optional[Settings] = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern with lazy initialization."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, base_url: str, api_key: str):
        """Initialize client lazily."""
        if self._initialized:
            return

        self._client = PlaneClientWrapper(
            base_url=base_url,
            api_key=api_key,
        )
        self._initialized = True

    @property
    def client(self) -> PlaneClientWrapper:
        """Get underlying SDK client."""
        return self._client
```

### Phase 2: Core Tools

#### 2.1 Project Commands

**File**: `src/plane_mcp/commands/project.py`

```python
"""Project management commands."""

from typing import List
from fastmcp import FastMCP
from plane.models.projects import CreateProject, UpdateProject
from plane_mcp.client import get_plane_client

mcp = FastMCP("plane-projects")

@mcp.tool(description="List all projects in workspace")
async def project_list() -> List[dict]:
    """List all projects."""
    client = get_plane_client()
    projects = client.projects.list(workspace_slug=settings.PLANE_WORKSPACE_SLUG)
    return [p.model_dump() for p in projects.results]

@mcp.tool(description="Create a new project")
async def project_create(name: str, identifier: str | None = None) -> dict:
    """Create a new project."""
    data = CreateProject(name=name, identifier=identifier)
    project = client.projects.create(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG,
        data=data
    )
    return project.model_dump()
```

#### 2.2 Work Item Commands

**File**: `src/plane_mcp/commands/work.py`

```python
"""Work item management commands."""

from typing import List, Optional
from fastmcp import FastMCP
from plane.models.work_items import CreateWorkItem, UpdateWorkItem
from plane_mcp.client import get_plane_client

mcp = FastMCP("plane-work")

@mcp.tool(description="Create a new work item")
async def work_add(
    project_id: str,
    name: str,
    description: str | None = None,
    priority: str = "medium",
    labels: List[str] | None = None,
) -> dict:
    """Create a new work item."""
    client = get_plane_client()

    data = CreateWorkItem(
        project_id=project_id,
        name=name,
        description=description,
        priority=priority,
        labels=labels or []
    )

    work_item = client.work_items.create(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG,
        project_id=project_id,
        data=data
    )
    return work_item.model_dump()
```

### Phase 3: Prompts & CLI

#### 3.1 Interactive Prompts

**File**: `src/plane_mcp/prompts/create_work.py`

```python
"""Prompts for work item creation."""

from fastmcp import FastMCP

mcp = FastMCP("plane-prompts")

@mcp.prompt("create-work-item")
def create_work_item_prompt(
    project_name: str = "Select project...",
    task_name: str = "Enter task name...",
    description: str = "Brief description...",
    priority: str = "medium",
    labels: list[str] = [],
) -> str:
    """Interactive prompt to create a work item."""
    return f"""
# Create Work Item

**Project**: {project_name}
**Task**: {task_name}
**Description**: {description}
**Priority**: {priority}
**Labels**: {', '.join(labels)}

Ready to create? Type 'confirm' to create this work item.
"""
```

#### 3.2 CLI Wrapper

**File**: `src/plane_mcp/main.py`

```python
"""Plane MCP CLI entry point."""

import click
from plane_mcp.client import get_plane_client

@click.group()
@click.option("--workspace", envvar="PLANE_WORKSPACE_SLUG", required=True)
@click.option("--api-key", envvar="PLANE_API_KEY", required=True)
@click.option("--base-url", envvar="PLANE_BASE_URL", default="https://api.plane.so")
def main(workspace, api_key, base_url):
    """Plane MCP Redux CLI."""
    get_plane_client.__init__(base_url, api_key)
    click.echo("Plane MCP Redux initialized")

@main.group()
def project():
    """Project management commands."""
    pass

@project.command("list")
def project_list():
    """List all projects."""
    client = get_plane_client()
    projects = client.projects.list(workspace_slug=workspace)
    for p in projects.results:
        click.echo(f"{p.identifier}: {p.name}")

@project.command("create")
@click.argument("name")
@click.option("--identifier", "-i")
def project_create(name, identifier):
    """Create a new project."""
    data = CreateProject(name=name, identifier=identifier)
    project = client.projects.create(
        workspace_slug=workspace,
        data=data
    )
    click.echo(f"Created: {project.identifier}")

@main.group()
def work():
    """Work item management commands."""
    pass

@work.command("add")
@click.argument("name")
@click.option("--project", "-p", required=True)
@click.option("--description", "-d")
@click.option("--priority", "-P", default="medium")
@click.option("--label", "-L", multiple=True)
def work_add(name, project, description, priority, label):
    """Create a new work item."""
    client = get_plane_client()
    labels = list(label) if label else []

    data = CreateWorkItem(
        project_id=project,
        name=name,
        description=description,
        priority=priority,
        labels=labels
    )

    work_item = client.work_items.create(
        workspace_slug=workspace,
        project_id=project,
        data=data
    )
    click.echo(f"Created: {work_item.identifier}")
```

### Phase 4: Testing & Documentation

#### 4.1 Test Structure

```
tests/
├── test_client.py
├── test_project.py
├── test_work.py
├── test_integration.py
└── conftest.py
```

---

## Quick Start

```bash
# 1. Install dependencies
pip install -e ".[dev]"

# 2. Set up environment
cp .env.example .env

# 3. Run server
fastmcp dev inspector src/plane_mcp/server.py

# 4. Test CLI
plane-rex --workspace my-workspace --api-key my-key project list

# 5. Add work item
plane-rex --workspace my-workspace --api-key my-key work add "Fix bug" -p my-project
```

---

**Last Updated**: 2026-04-14T01:30:00Z
**Version**: 0.1.0

---

## 📋 Minimum Required Fields by Resource

Based on testing with `plane-python-sdk` v0.2.8:

| Resource  | Create Min Fields                  | Update Fields | Notes                               |
| --------- | ---------------------------------- | ------------- | ----------------------------------- |
| Project   | `name` + `identifier`              | Partial       | Identifier must be unique           |
| Work Item | `name`                             | Partial       | **Everything else auto-generated!** |
| Label     | `name`                             | Partial       | **Very flexible!**                  |
| Module    | `name` + `identifier`              | Partial       | Requires `module_view: true`        |
| Cycle     | `name` + `owned_by` + `project_id` | Partial       | Requires `cycle_view: true`         |
| Workspace | ❓ Requires investigation          | Partial       | Not fully tested in CE              |

---

## Example: Creating Work Items

```python
# ✅ Minimal - just the title!
data = CreateWorkItem(name="Bananas Task")
work_item = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    data=data
)
```

## Example: Creating Labels

```python
# ✅ Minimal - just the name!
data = CreateLabel(name="Bug")
label = client.labels.create(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    data=data
)
```

## Example: Creating Projects

```python
# ✅ Requires name + unique identifier
data = CreateProject(name="My Project", identifier="PROJ-123")
project = client.projects.create(
    workspace_slug=workspace_slug,
    data=data
)
```

---

**Last Updated**: 2026-04-14T01:45:00Z
**Version**: 0.1.1
