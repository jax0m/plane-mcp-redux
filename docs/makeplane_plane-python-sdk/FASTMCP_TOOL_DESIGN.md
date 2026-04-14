# FastMCP Tool Design: Stickies & Work Items

**Created**: 2026-04-13T20:25:00Z
**Last Updated**: 2026-04-13T20:25:00Z
**Owner**: AI Assistant
**Status**: Active
**Version**: 1.0.0

---

## 📋 Overview

This document outlines the complete design for FastMCP tools and CLI commands for Stickies and Work Items, including all operations, parameters, error handling, and edge cases.

---

## 🎯 Current Capabilities (Verified)

### Stickies

- ✅ List (workspace-level)
- ✅ Create (workspace-level)
- ✅ Retrieve (workspace-level, requires ID)
- ✅ Update (workspace-level)
- ✅ Delete (workspace-level)

### Work Items

- ✅ List/Search (project-level)
- ✅ Create (project-level, minimal fields)
- ✅ Retrieve (project-level, requires UUID)
- ✅ Update (project-level)
- ✅ Delete (project-level)
- ✅ Link (parent reference)

---

## 🔍 Missing Capabilities to Verify

### Stickies - Unknown Operations

| Operation             | Status | Notes                               |
| --------------------- | ------ | ----------------------------------- |
| Bulk operations       | ❓     | Can we create multiple at once?     |
| Filter by state       | ❓     | Can we filter stickies by state?    |
| Filter by labels      | ❓     | Can we filter by labels?            |
| Search                | ❓     | Does search work?                   |
| Move between projects | ❓     | Can stickies move between projects? |
| Export                | ❓     | Can we export stickies?             |

### Work Items - Unknown Operations

| Operation       | Status | Notes                          |
| --------------- | ------ | ------------------------------ |
| Bulk operations | ❓     | Can we create/update multiple? |
| Advanced search | ❓     | What filters are available?    |
| Grouping        | ❓     | Can we group by state/label?   |
| Bulk delete     | ❓     | Can we delete multiple?        |
| Archive         | ❓     | Is there an archive operation? |
| Clone           | ❓     | Can we clone work items?       |
| Add comments    | ❓     | How to add comments?           |
| Add relations   | ❓     | Can we add relations?          |
| Add attachments | ❓     | How to attach files?           |
| Add activities  | ❓     | How to log activities?         |

---

## 🛠️ FastMCP Tool Design

### Stickies Tools

```python
from fastmcp import FastMCP
from plane.models.stickies import CreateSticky, UpdateSticky

@mcp.tool(description="List all stickies in workspace")
async def list_stickies(
    workspace_id: str,
    project_id: str | None = None,
    state_id: str | None = None,
    page: int = 1,
    per_page: int = 20
) -> list[dict]:
    """List stickies with optional filtering and pagination."""
    pass

@mcp.tool(description="Create a new sticky note")
async def create_sticky(
    workspace_id: str,
    project_id: str,
    title: str,
    description: str = "",
    state_id: str | None = None,
    color: str | None = None,
    label: str | None = None,
    position: dict | None = None
) -> dict:
    """Create a new sticky note."""
    pass

@mcp.tool(description="Get a sticky note by ID")
async def get_sticky(
    workspace_id: str,
    sticky_id: str
) -> dict:
    """Get sticky details."""
    pass

@mcp.tool(description="Update a sticky note")
async def update_sticky(
    workspace_id: str,
    sticky_id: str,
    title: str | None = None,
    description: str | None = None,
    state_id: str | None = None,
    color: str | None = None,
    label: str | None = None,
    position: dict | None = None
) -> dict:
    """Update sticky properties."""
    pass

@mcp.tool(description="Delete a sticky note")
async def delete_sticky(
    workspace_id: str,
    sticky_id: str
) -> dict:
    """Delete a sticky note."""
    pass

@mcp.tool(description="Search stickies by text")
async def search_stickies(
    workspace_id: str,
    query: str,
    page: int = 1,
    per_page: int = 20
) -> list[dict]:
    """Search stickies by text query."""
    pass
```

### Work Items Tools

```python
from fastmcp import FastMCP
from plane.models.work_items import CreateWorkItem, UpdateWorkItem

@mcp.tool(description="List work items in project")
async def list_work_items(
    workspace_id: str,
    project_id: str,
    state_id: str | None = None,
    priority: str | None = None,
    page: int = 1,
    per_page: int = 20
) -> list[dict]:
    """List work items with optional filtering."""
    pass

@mcp.tool(description="Search work items by text")
async def search_work_items(
    workspace_id: str,
    project_id: str,
    query: str,
    page: int = 1,
    per_page: int = 20
) -> list[dict]:
    """Search work items by text query."""
    pass

@mcp.tool(description="Create a new work item")
async def create_work_item(
    workspace_id: str,
    project_id: str,
    title: str,
    description: str | None = None,
    priority: str | None = None,
    point: int | None = None,
    assignee_id: str | None = None,
    labels: list[str] | None = None,
    parent_id: str | None = None
) -> dict:
    """Create a work item with minimal required fields."""
    pass

@mcp.tool(description="Get work item details")
async def get_work_item(
    workspace_id: str,
    project_id: str,
    work_item_id: str
) -> dict:
    """Get work item with all properties."""
    pass

@mcp.tool(description="Update work item properties")
async def update_work_item(
    workspace_id: str,
    project_id: str,
    work_item_id: str,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    point: int | None = None,
    assignee_id: str | None = None,
    labels: list[str] | None = None,
    parent_id: str | None = None,
    start_date: str | None = None,
    target_date: str | None = None
) -> dict:
    """Update work item properties."""
    pass

@mcp.tool(description="Delete a work item")
async def delete_work_item(
    workspace_id: str,
    project_id: str,
    work_item_id: str
) -> dict:
    """Delete a work item."""
    pass

@mcp.tool(description="Link work items (set parent)")
async def link_work_items(
    workspace_id: str,
    project_id: str,
    child_id: str,
    parent_id: str
) -> dict:
    """Link work items by setting parent reference."""
    pass

@mcp.tool(description="Get work item by identifier")
async def get_work_item_by_identifier(
    workspace_id: str,
    project_id: str,
    identifier: str
) -> dict:
    """Get work item using identifier instead of UUID."""
    pass
```

---

## 🧩 CLI Command Design

### Stickies CLI Commands

```bash
# List stickies
plane-rex sticky list --workspace WORKSPACE --project PROJECT

# List stickies with filters
plane-rex sticky list --workspace WORKSPACE --project PROJECT --state STATE_ID

# Create sticky
plane-rex sticky create --workspace WORKSPACE --project PROJECT \
  --title "My Sticky" --description "Description"

# Get sticky
plane-rex sticky get --workspace WORKSPACE --sticky STICKY_ID

# Update sticky
plane-rex sticky update --workspace WORKSPACE --sticky STICKY_ID \
  --title "Updated Title" --color "#FF0000"

# Delete sticky
plane-rex sticky delete --workspace WORKSPACE --sticky STICKY_ID

# Search stickies
plane-rex sticky search --workspace WORKSPACE --query "urgent"
```

### Work Items CLI Commands

```bash
# List work items
plane-rex issue list --workspace WORKSPACE --project PROJECT

# List work items with filters
plane-rex issue list --workspace WORKSPACE --project PROJECT \
  --state STATE_ID --priority HIGH

# Create issue
plane-rex issue create --workspace WORKSPACE --project PROJECT \
  --title "New Issue" --priority HIGH

# Get issue
plane-rex issue get --workspace WORKSPACE --project PROJECT \
  --id WORK_ITEM_ID

# Get issue by identifier
plane-rex issue get --workspace WORKSPACE --project PROJECT \
  --identifier "ISSUE-123"

# Update issue
plane-rex issue update --workspace WORKSPACE --project PROJECT \
  --id WORK_ITEM_ID --title "Updated" --priority URGENT

# Search issues
plane-rex issue search --workspace WORKSPACE --project PROJECT \
  --query "bug fix"

# Delete issue
plane-rex issue delete --workspace WORKSPACE --project PROJECT \
  --id WORK_ITEM_ID

# Link issues
plane-rex issue link --workspace WORKSPACE --project PROJECT \
  --child CHILD_ID --parent PARENT_ID
```

---

## 📊 Error Handling Patterns

### Error Categories

| Error Type   | HTTP Code | Pattern                | Example                                   |
| ------------ | --------- | ---------------------- | ----------------------------------------- |
| Not Found    | 404       | Resource doesn't exist | `project_id`, `sticky_id`, `work_item_id` |
| Bad Request  | 400       | Invalid parameters     | Missing required fields                   |
| Unauthorized | 401       | Invalid API key        | API key expired/invalid                   |
| Forbidden    | 403       | Permission denied      | Missing workspace access                  |
| Conflict     | 409       | Duplicate identifier   | Creating with existing `identifier`       |
| Rate Limit   | 429       | Too many requests      | Slow down operations                      |
| Server Error | 500       | Internal server error  | Retry operation                           |

### Error Handling in Tools

```python
import httpx
from pydantic import ValidationError

async def handle_sticky_error(operation: str, error: Exception) -> dict:
    """Standard error handler for sticky operations."""
    if isinstance(error, httpx.HTTPStatusError):
        response = error.response
        if response.status_code == 404:
            return {"error": "not_found", "message": f"Sticky not found"}
        elif response.status_code == 400:
            return {"error": "bad_request", "message": str(error)}
        elif response.status_code == 401:
            return {"error": "unauthorized", "message": "Invalid API key"}
        elif response.status_code == 403:
            return {"error": "forbidden", "message": "Access denied"}
        elif response.status_code == 409:
            return {"error": "conflict", "message": str(error)}
        elif response.status_code == 429:
            return {"error": "rate_limit", "message": "Too many requests"}
    return {"error": "unknown", "message": str(error)}
```

---

## 🔄 Pagination Handling

### Pattern

```python
def paginate_results(
    client,
    list_method,
    workspace_id: str,
    project_id: str | None = None,
    page: int = 1,
    per_page: int = 20
) -> list[dict]:
    """Paginate through results."""
    params = PaginatedQueryParams(
        page=page,
        per_page=per_page
    )

    response = list_method(
        workspace_slug=workspace_id,
        project_id=project_id,
        params=params
    )

    return response.results
```

---

## 🎯 UUID vs Identifier Handling

### Work Items

```python
# Can use either UUID or identifier
work_item = client.work_items.retrieve(
    workspace_slug=workspace_id,
    project_id=project_id,
    work_item_id="ISSUE-123"  # Identifier format
)

# Also works with UUID
work_item = client.work_items.retrieve(
    workspace_slug=workspace_id,
    project_id=project_id,
    work_item_id="uuid-here"  # UUID format
)
```

### Stickies

```python
# Stickies use UUID only
sticky = client.stickies.retrieve(
    workspace_slug=workspace_id,
    sticky_id="uuid-here"  # UUID only
)
```

---

## 📝 Field Reference

### Stickies - Full Properties

| Field              | Type | Required | Description             |
| ------------------ | ---- | -------- | ----------------------- |
| `id`               | UUID | Yes      | Unique identifier       |
| `title`            | str  | Yes      | Sticky title            |
| `description`      | str  | No       | Description             |
| `description_html` | str  | No       | HTML description        |
| `state_id`         | UUID | No       | State UUID              |
| `color`            | str  | No       | Color (e.g., "#FF0000") |
| `label`            | str  | No       | Label                   |
| `position`         | dict | No       | Position (x, y)         |
| `created_at`       | str  | Yes      | Creation timestamp      |
| `updated_at`       | str  | Yes      | Update timestamp        |

### Work Items - Full Properties

| Field              | Type      | Required | Description        |
| ------------------ | --------- | -------- | ------------------ |
| `id`               | UUID      | Yes      | Unique identifier  |
| `name`             | str       | Yes      | Title (required)   |
| `type`             | str       | No       | Type (auto)        |
| `description`      | str       | No       | Plain text         |
| `description_html` | str       | No       | HTML description   |
| `priority`         | str       | No       | Priority level     |
| `state`            | UUID      | No       | State UUID         |
| `labels`           | list[str] | No       | Label UUIDs        |
| `assignees`        | list[str] | No       | Assignee UUIDs     |
| `point`            | int       | No       | Story points       |
| `parent`           | str       | No       | Parent UUID        |
| `created_at`       | str       | Yes      | Creation timestamp |
| `updated_at`       | str       | Yes      | Update timestamp   |

---

## 🚀 Next Steps - What to Test

### Stickies Testing Checklist

- [ ] Test list with pagination
- [ ] Test create with all optional fields
- [ ] Test retrieve by UUID
- [ ] Test update with all optional fields
- [ ] Test delete
- [ ] Test search functionality
- [ ] Test filter by state
- [ ] Test filter by labels
- [ ] Test bulk operations

### Work Items Testing Checklist

- [ ] Test list with pagination
- [ ] Test create with minimal fields
- [ ] Test create with all optional fields
- [ ] Test retrieve by UUID
- [ ] Test retrieve by identifier
- [ ] Test update with all optional fields
- [ ] Test delete
- [ ] Test search with various queries
- [ ] Test filter by state
- [ ] Test filter by priority
- [ ] Test filter by labels
- [ ] Test filter by assignee
- [ ] Test parent linking
- [ ] Test bulk operations
- [ ] Test export functionality

---

## 📚 Related Documentation

- [Stickies API](../workspace/STICKIES.md)
- [Work Items API](../workspace/WORK_ITEMS.md)
- [Work Item Properties](../workspace/work_items/WORK_ITEM_PROPERTIES_REFERENCE.md)
- [UUID Management Guide](../../../.pi/plans/UUID_AND_DEPENDENCY_GUIDE.md)

---

**Last Updated**: 2026-04-13T20:25:00Z
**Document Version**: 1.0.0
