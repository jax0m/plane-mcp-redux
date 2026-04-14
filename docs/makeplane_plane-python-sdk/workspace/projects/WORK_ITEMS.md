# Work Items API Documentation

**Document Version**: 1.0.0
**Created**: 2026-04-13T19:55:00Z
**Last Updated**: 2026-04-13T23:35:00Z
**Owner**: AI Assistant
**Status**: Active
**Version**: 1.0.0

---

## 📋 Overview

Work Items (Tasks/Issues) are **project-level** resources that can be created with **minimal fields**. The API auto-generates identifiers.

**API Endpoint**: `/workspaces/{workspace_slug}/projects/{project_id}/work-items`
**Level**: Project
**SDK Version**: plane-python-sdk
**API Instance**: https://your-plane-instance/ (Community Edition)
**Last Tested**: 2026-04-13T23:35:00Z

---

## ✅ Working Endpoints - Full CRUD + Search

All work item endpoints work successfully with **minimal required fields**.

### 1. Create Work Item

**Endpoint**: `work_items.create()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `data: CreateWorkItem`

**Minimum Required Fields**:

- `name` (string) - The title of the work item
- Everything else is optional!

```python
from plane.models.work_items import CreateWorkItem

# Minimal creation - just the title!
data = CreateWorkItem(
    name="Bananas Task"
    # type, description, labels - all optional!
)

work_item = client.work_items.create(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    data=data
)
```

**Returns**: `WorkItem`

**Test Result**: ✅ SUCCESS - Created with just name field

---

### 2. Retrieve Work Item

**Endpoint**: `work_items.retrieve()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `work_item_id` (UUID or identifier)

```python
work_item = client.work_items.retrieve(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    work_item_id="3147bc58-48da-490c-ba1b-951f2256d890"
)
```

**Returns**: `WorkItem`

**Test Result**: ✅ SUCCESS

**Note**: Works with both UUID and identifier formats!

---

### 3. Update Work Item

**Endpoint**: `work_items.update()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `work_item_id`, `data: UpdateWorkItem`

```python
from plane.models.work_items import UpdateWorkItem

data = UpdateWorkItem(
    name="Updated Bananas Task",
    description="This was updated via MCP"
)

work_item = client.work_items.update(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    work_item_id="3147bc58-48da-490c-ba1b-951f2256d890",
    data=data
)
```

**Returns**: `WorkItem`

**Test Result**: ✅ SUCCESS

---

### 4. Delete Work Item

**Endpoint**: `work_items.delete()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `work_item_id` (UUID)

```python
client.work_items.delete(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    work_item_id="3147bc58-48da-490c-ba1b-951f2256d890"
)
```

**Returns**: `None`

**Test Result**: ✅ SUCCESS

---

### 5. Search Work Items

**Endpoint**: `work_items.search()`
**Level**: Workspace
**Parameters**: `workspace_slug`, `query`

```python
results = client.work_items.search(
    workspace_slug="your-workspace-slug",
    query="bananas"
)
```

**Returns**: `WorkItemSearch`

**Test Result**: ✅ SUCCESS

---

### 6. Link Work Items (Parent Reference)

**Endpoint**: `work_items.update()` with `parent` field
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `work_item_id`, `UpdateWorkItem(parent=...)`

```python
from plane.models.work_items import UpdateWorkItem

# Create parent
parent = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    data=CreateWorkItem(name="Parent Task")
)

# Create child and link to parent
child = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    data=CreateWorkItem(name="Child Task")
)

# Update child to link to parent
child = client.work_items.update(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    work_item_id=child.id,
    data=UpdateWorkItem(parent=parent.id)
)

# Verify parent reference
child = client.work_items.retrieve(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    work_item_id=child.id
)
print(child.parent)  # Returns parent UUID
```

**Test Result**: ✅ SUCCESS - Parent reference stored in work item

---

## 📊 Work Item Data Structure

### Core Fields

| Field                  | Type      | Description                 | Example                                |
| ---------------------- | --------- | --------------------------- | -------------------------------------- |
| `id`                   | UUID      | Unique work item identifier | `d5e1f425-973b-4655-a678-acf06c50a7ad` |
| `name`                 | str       | Work item title (required)  | `"Bananas Task"`                       |
| `type`                 | str       | Work item type (auto)       | `"issue"`                              |
| `description`          | str       | Plain text description      | `""`                                   |
| `description_html`     | str       | HTML description            | `"<p></p>"`                            |
| `description_stripped` | str       | Plain text description      | `None`                                 |
| `priority`             | str       | Priority level              | `"none"`                               |
| `state`                | UUID      | State UUID                  | `c3715349-...`                         |
| `labels`               | list[str] | Label UUIDs                 | `[]`                                   |
| `assignees`            | list[str] | Assignee UUIDs              | `[]`                                   |
| `point`                | int       | Story points                | `None`                                 |
| `parent`               | str       | Parent work item UUID       | `None`                                 |
| `project`              | UUID      | Parent project ID           | `3adb93b5-...`                         |
| `workspace`            | UUID      | Parent workspace ID         | `4ef343ce-...`                         |
| `created_at`           | datetime  | Creation timestamp          | `2026-04-13T...`                       |
| `updated_at`           | datetime  | Update timestamp            | `2026-04-13T...`                       |
| `deleted_at`           | datetime  | Deletion timestamp          | `None`                                 |

---

## 🔧 MCP Tool Implementation Example

```python
from fastmcp import FastMCP
from plane.models.work_items import CreateWorkItem, UpdateWorkItem

mcp = FastMCP("Plane Work Items")

@mcp.tool(description="Create a new work item (task/issue)")
async def create_work_item(
    workspace_id: str,
    project_id: str,
    title: str
) -> dict:
    """Create a new work item with just the title."""
    data = CreateWorkItem(name=title)
    work_item = client.work_items.create(
        workspace_slug=workspace_id,
        project_id=project_id,
        data=data
    )
    return {
        "id": work_item.id,
        "name": work_item.name,
        "type": work_item.type
    }

@mcp.tool(description="Update a work item")
async def update_work_item(
    workspace_id: str,
    project_id: str,
    work_item_id: str,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None
) -> dict:
    """Update a work item."""
    data = UpdateWorkItem()
    if title:
        data.name = title
    if description:
        data.description = description
    if priority:
        data.priority = priority

    work_item = client.work_items.update(
        workspace_slug=workspace_id,
        project_id=project_id,
        work_item_id=work_item_id,
        data=data
    )
    return {
        "id": work_item.id,
        "name": work_item.name,
        "priority": work_item.priority
    }

@mcp.tool(description="Search work items")
async def search_work_items(
    workspace_id: str,
    project_id: str,
    query: str
) -> list[dict]:
    """Search work items by text."""
    results = client.work_items.search(
        workspace_slug=workspace_id,
        query=query
    )
    return [item.model_dump() for item in results.results]

@mcp.tool(description="Link work items")
async def link_work_items(
    workspace_id: str,
    project_id: str,
    child_id: str,
    parent_id: str
) -> dict:
    """Link work items by setting parent reference."""
    work_item = client.work_items.update(
        workspace_slug=workspace_id,
        project_id=project_id,
        work_item_id=child_id,
        data=UpdateWorkItem(parent=parent_id)
    )
    return {
        "id": work_item.id,
        "parent": work_item.parent
    }

@mcp.tool(description="Delete a work item")
async def delete_work_item(workspace_id: str, project_id: str, work_item_id: str) -> dict:
    """Delete a work item."""
    client.work_items.delete(
        workspace_slug=workspace_id,
        project_id=project_id,
        work_item_id=work_item_id
    )
    return {"message": "Work item deleted successfully"}
```

---

## 🧪 Test Results

### Test Date: 2026-04-13T23:35:00Z

| Test                 | Status     | Notes                        |
| -------------------- | ---------- | ---------------------------- |
| create_work_item()   | ✅ SUCCESS | Created with just name field |
| retrieve_work_item() | ✅ SUCCESS | Retrieved by UUID/identifier |
| update_work_item()   | ✅ SUCCESS | Updated name and description |
| delete_work_item()   | ✅ SUCCESS | Deleted successfully         |
| search_work_items()  | ✅ SUCCESS | Text search working          |
| link_work_items()    | ✅ SUCCESS | Parent reference works       |

---

## 📝 Important Notes

### Key Points

1. **Minimal Creation**: Work items can be created with just the `name` field
2. **Auto-Generated ID**: The API auto-generates the work item identifier
3. **UUID/Identifier Support**: Both UUID and identifier formats work for retrieve/update/delete
4. **Project-Level**: Work items belong to projects, not directly to workspace
5. **Linking**: Parent-child relationships supported via `parent` field

### UUID Management Pattern

```python
# 1. List project to get UUID
projects = client.projects.list(workspace_slug=workspace_slug)
project_uuid = projects.results[0].id

# 2. Create work item (just needs name)
data = CreateWorkItem(name="Bananas Task")
work_item = client.work_items.create(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    data=data
)

# 3. Use UUID for modify operations
client.work_items.update(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    work_item_id=work_item.id,  # UUID or identifier
    data=data
)
```

---

## 🔗 Related Documentation

- [Projects](projects/README.md) - Parent resource
- [Labels](LABELS.md) - Labels for work items
- [Modules](MODULES.md) - Modules for work items
- [UUID Management Guide](../../../.pi/plans/UUID_AND_DEPENDENCY_GUIDE.md)
- [SDK API Mapping](../../../.pi/plans/SDK_API_MAPPING.md)
- [FastMCP Tool Design](../../FASTMCP_TOOL_DESIGN.md)

---

## 📚 References

- **SDK Source**: `plane.api.work_items.base`
- **SDK Models**: `plane.models.work_items`
- **Test Scripts**: `/tmp/test_workitems_minimal.py`, `/tmp/test_stickies.py`, `/tmp/test_projects_deep.py`

---

**Last Updated**: 2026-04-13T23:35:00Z
**Document Version**: 1.0.0
