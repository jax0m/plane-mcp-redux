# FastMCP Workflow Design for plane-mcp-redux

**Created**: 2026-04-14T01:25:00Z
**Last Updated**: 2026-04-14T02:00:00Z
**Owner**: AI Assistant
**Status**: Draft
**Version**: 0.2.0

---

## 🎯 Design Philosophy

### Workflow-Oriented vs API-Oriented

**Current Approach (API-Oriented)**:

```
projects.list()
projects.create()
projects.update()
projects.delete()
```

**Proposed Approach (Workflow-Oriented)**:

```
plane project list
plane project create "My Project"
plane work add "Fix critical bug" --project my-project --label bug --priority high
plane work list --project my-project --label bug --state todo
```

### Key Principles

1. **Human-Readable**: Commands that make sense to end users
2. **Workflow-Based**: Organized around tasks, not API resources
3. **Lazy Loading**: Efficient client creation
4. **Prompt-Driven**: Common tasks via prompts
5. **Progressive Disclosure**: Simple defaults, advanced options available
6. **Global Workspace**: `workspace_slug` configured once, used everywhere

---

## 📋 CLI Command Structure

### Environment Configuration

**Global Configuration (`.env` file)**:

```bash
# Global workspace configuration - set once
PLANE_BASE_URL=https://your-plane-instance/
PLANE_API_KEY=your-api-key-here
PLANE_WORKSPACE_SLUG=your-workspace-slug  # Used everywhere
```

**No CLI flags needed for workspace** - it's global!

### Top-Level Commands

```
plane-rex <command> [options]

Commands:
  project          Project management
  work             Work item management
  label            Label management
  module           Module management
  cycle            Cycle management
  search           Search across resources
  user             User/Member management
  state            State management
  init             Initialize configuration
  help             Show help
```

### Command Hierarchy

```
plane-rex
├── project
│   ├── list              List all projects in workspace
│   ├── create <name>     Create new project
│   ├── delete <id>       Delete project
│   ├── info <id>         Get project details
│   ├── features <id>     Show project features
│   └── settings <id>     Update project settings
├── work
│   ├── list              List work items in project
│   ├── add <title>       Create new work item
│   ├── update <id>       Update work item
│   ├── delete <id>       Delete work item
│   ├── move <id> <state> Move to state
│   ├── assign <id> <user> Assign user
│   ├── labels <id>       Add/remove labels
│   └── cycle <id> <cycle> Add to cycle
├── label
│   ├── list              List labels
│   ├── create <name>     Create label
│   ├── delete <id>       Delete label
│   └── assign <id>       Assign label to work item
├── module
│   ├── list              List modules
│   ├── create <name>     Create module
│   ├── delete <id>       Delete module
│   └── assign <id>       Assign work items to module
├── cycle
│   ├── list              List cycles
│   ├── create <name>     Create cycle
│   └── add <id>          Add work items to cycle
├── search
│   ├── work              Search work items
│   ├── project           Search projects
│   └── label             Search labels
├── user
│   ├── list              List users
│   └── assign <id>       Assign user to work item
└── state
    ├── list              List states
    └── move <id> <state> Move work item to state
```

---

## 🔧 FastMCP Server Structure

### Main Entry Point

```
src/plane_mcp/server.py
```

```python
"""
Plane MCP Server - Workflow-Oriented Implementation

FastMCP 3.x with lazy loading and workflow commands
"""

from fastmcp import FastMCP
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP
mcp = FastMCP("plane-mcp-redux")

# Settings - Global workspace configuration
class Settings(BaseSettings):
    """Global Plane MCP configuration."""

    # Global workspace configuration
    PLANE_BASE_URL: str = "https://api.plane.so"
    PLANE_API_KEY: str
    PLANE_WORKSPACE_SLUG: str  # ✅ Global - used everywhere

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# Lazy-loaded client
_plane_client: None = None

def get_plane_client() -> PlaneClientWrapper:
    """Lazy client initialization using global workspace_slug."""
    global _plane_client
    if _plane_client is None:
        from plane_mcp.client import PlaneClientWrapper
        _plane_client = PlaneClientWrapper(
            base_url=settings.PLANE_BASE_URL,
            api_key=settings.PLANE_API_KEY,
        )
    return _plane_client
```

---

## 📁 Project Commands

```python
from fastmcp import FastMCP
from plane.models.projects import CreateProject, UpdateProject

mcp = FastMCP("plane-projects")

@mcp.tool(description="List all projects in workspace")
async def project_list() -> list[dict]:
    """List all projects - workspace_slug from .env."""
    client = get_plane_client()
    projects = client.projects.list(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG  # ✅ Global
    )

    result = []
    for p in projects.results:
        result.append({
            "id": p.id,
            "identifier": p.identifier,
            "name": p.name,
            "workspace": p.workspace,
        })
    return result

@mcp.tool(description="Create a new project")
async def project_create(name: str, identifier: str | None = None) -> dict:
    """Create a new project."""
    from plane.models.projects import CreateProject

    client = get_plane_client()

    if identifier is None:
        import uuid
        identifier = f"PROJ-{uuid.uuid4().hex[:8]}"

    data = CreateProject(
        name=name,
        identifier=identifier
    )

    project = client.projects.create(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG,  # ✅ Global
        data=data
    )

    return {
        "id": project.id,
        "identifier": project.identifier,
        "name": project.name,
    }
```

---

## 📝 Work Item Commands

```python
from fastmcp import FastMCP
from plane.models.work_items import CreateWorkItem, UpdateWorkItem

mcp = FastMCP("plane-work")

@mcp.tool(description="List work items in project")
async def work_list(
    project_id: str,
    state: str | None = None,
    label: str | None = None,
) -> list[dict]:
    """List work items with optional filters."""
    client = get_plane_client()

    from plane.models.work_items import WorkItemQueryParams

    params = WorkItemQueryParams()
    if state:
        params.state = state
    if label:
        params.labels = [label]

    work_items = client.work_items.list(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG,  # ✅ Global
        project_id=project_id,
        params=params
    )

    result = []
    for w in work_items.results:
        result.append({
            "id": w.id,
            "identifier": w.identifier,
            "name": w.name,
            "state": w.state,
            "labels": w.labels,
            "priority": w.priority,
        })
    return result

@mcp.tool(description="Create a new work item")
async def work_add(
    project_id: str,
    name: str,
    description: str | None = None,
    priority: str = "medium",
    labels: list[str] | None = None,
) -> dict:
    """Create a new work item."""
    from plane.models.work_items import CreateWorkItem

    client = get_plane_client()

    # ✅ Minimal creation - just name required!
    data = CreateWorkItem(
        project_id=project_id,
        name=name,
        description=description,
        priority=priority,
        labels=labels or []
    )

    work_item = client.work_items.create(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG,  # ✅ Global
        project_id=project_id,
        data=data
    )

    return {
        "id": work_item.id,
        "identifier": work_item.identifier,
        "name": work_item.name,
        "priority": work_item.priority,
        "labels": work_item.labels,
    }
```

---

## 🏷️ Label Commands

```python
from fastmcp import FastMCP
from plane.models.labels import CreateLabel, UpdateLabel

mcp = FastMCP("plane-labels")

@mcp.tool(description="List labels in project")
async def label_list(project_id: str) -> list[dict]:
    """List all labels in project."""
    client = get_plane_client()
    labels = client.labels.list(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG,  # ✅ Global
        project_id=project_id
    )
    return [l.model_dump() for l in labels.results]

@mcp.tool(description="Create a new label")
async def label_create(project_id: str, name: str, color: str = "#0088FE") -> dict:
    """Create a new label."""
    from plane.models.labels import CreateLabel

    client = get_plane_client()
    label = client.labels.create(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG,  # ✅ Global
        project_id=project_id,
        data=CreateLabel(name=name, color=color)
    )
    return label.model_dump()

@mcp.tool(description="Assign label to work item")
async def label_assign(
    project_id: str,
    work_item_id: str,
    label_id: str,
) -> dict:
    """Assign a label to a work item."""
    from plane.models.work_items import UpdateWorkItem

    client = get_plane_client()
    work_item = client.work_items.update(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG,  # ✅ Global
        project_id=project_id,
        work_item_id=work_item_id,
        data=UpdateWorkItem(labels=[label_id])
    )
    return {"status": "assigned", "labels": work_item.labels}
```

---

## 🎨 CLI Interface Design

### Using `plane-rex` CLI

```bash
# Initialize configuration
plane-rex init

# List projects
plane-rex project list

# Create project
plane-rex project create "My Project"

# List work items in project
plane-rex work list --project my-project

# Add work item (workspace_slug is global!)
plane-rex work add "Fix critical bug" \
    --project my-project \
    --label bug \
    --priority high \
    --description "We need to fix this ASAP"

# Update work item
plane-rex work update 12345 \
    --name "Updated task" \
    --priority high

# Assign label to work item
plane-rex label assign 12345 --label bug --project my-project

# Move work item to state
plane-rex state move 12345 --state done
```

### Interactive Mode

```bash
# Start interactive session
plane-rex --interactive

# Or use prompts
plane-rex work add --prompt "create-work-item"
```

---

## 📦 Module Structure

```
src/plane_mcp/
├── __init__.py
├── main.py              # Entry point
├── client.py            # Lazy client wrapper
├── server.py            # FastMCP server with tools
├── commands/            # Command handlers
│   ├── __init__.py
│   ├── project.py       # Project commands
│   ├── work.py          # Work item commands
│   ├── label.py         # Label commands
│   ├── module.py        # Module commands
│   └── cycle.py         # Cycle commands
├── prompts/             # Interactive prompts
│   ├── __init__.py
│   ├── create_work.py   # Work item creation
│   └── list_work.py     # Work item listing
└── utils/               # Utilities
    ├── __init__.py
    └── lazy.py          # Lazy loading utilities
```

---

## 🚀 Lazy Loading Implementation

### Client Initialization

```python
# src/plane_mcp/client.py

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

### Tool-Level Lazy Loading

```python
# src/plane_mcp/server.py

@mcp.tool(description="List projects")
async def project_list() -> list[dict]:
    """List all projects."""
    # Client is initialized on first use
    client = get_plane_client()
    # ... rest of implementation
```

---

## 🧪 Testing Strategy

### Unit Tests

```python
# tests/test_project_commands.py

import pytest
from plane_mcp.client import get_plane_client

def test_project_list():
    """Test project list command."""
    client = get_plane_client()
    projects = client.projects.list(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG
    )
    assert len(projects.results) >= 0
```

### Integration Tests

```python
# tests/test_integration.py

@pytest.mark.integration
async def test_work_item_workflow():
    """Test complete work item workflow."""
    # Create project
    project = await create_project("Test Project")

    # Create work item
    work_item = await create_work_item(project.id, "Test task")

    # Update work item
    work_item = await update_work_item(project.id, work_item.id, name="Updated")

    # Cleanup
    await delete_work_item(project.id, work_item.id)
    await delete_project(project.id)
```

---

## 📚 Documentation Structure

```
docs/makeplane_plane-python-sdk/
├── INDEX.md
├── INVESTIGATION_STRATEGY.md
├── SESSION_SUMMARY.md
├── FASTMCP_TOOL_DESIGN.md
├── FASTMCP_WORKFLOW_DESIGN.md       # This file
├── FASTMCP_IMPLEMENTATION_PLAN.md
├── CRUD_MINIMUM_FIELDS.md
├── planning/
│   ├── SDK_API_MAPPING.md
│   ├── UUID_AND_DEPENDENCY_GUIDE.md
│   └── INVESTIGATION_STRATEGY.md
└── workspace/
    ├── projects/
    │   ├── README.md
    │   ├── CYCLES.md
    │   ├── MODULES.md
    │   ├── LABELS.md
    │   ├── PAGES.md
    │   └── WORK_ITEMS.md
    └── work_items/
        └── README.md
```

---

## 🎯 Key Benefits

### 1. Human-Readable Commands

```bash
# API-oriented (hard to remember)
plane project list --workspace my-workspace

# Workflow-oriented (intuitive)
plane project list
```

### 2. Progressive Disclosure

```bash
# Simple
plane work add "Fix bug"

# Advanced
plane work add "Fix bug" \
    --project my-project \
    --label bug \
    --priority high \
    --description "Detailed description..." \
    --assign user-123
```

### 3. Lazy Loading

- Client initialized only when needed
- Faster startup time
- Better memory usage

### 4. Global Workspace Configuration

- `workspace_slug` configured once in `.env`
- No CLI flags needed for workspace
- Consistent across all commands
- Easier to manage multi-project workflows

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
| Workspace | ❓ Requires investigation          | Partial       | Not available on CE (HTTP 404)      |

---

## 🚀 Quick Start

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env with your credentials:
# PLANE_BASE_URL=https://your-plane-instance/
# PLANE_API_KEY=your-api-key-here
# PLANE_WORKSPACE_SLUG=your-workspace-slug

# 2. Install dependencies
pip install -e ".[dev]"

# 3. Run server with inspector
fastmcp dev inspector src/plane_mcp/server.py

# 4. Test CLI (once CLI wrapper is built)
plane-rex project list
plane-rex work add "Test task" --project my-project
```

---

## 🎯 Next Steps

1. ✅ **Define command structure** - Complete
2. ⏳ **Implement core tools** - Project, Work, Label
3. ⏳ **Add lazy loading** - Client wrapper
4. ⏳ **Create prompts** - Interactive forms
5. ⏳ **Build CLI wrapper** - argparse or click
6. ⏳ **Add tests** - Unit and integration
7. ⏳ **Document** - User guide and API reference

---

**Last Updated**: 2026-04-14T02:00:00Z
**Version**: 0.2.0
