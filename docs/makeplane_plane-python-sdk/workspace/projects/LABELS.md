# Labels API Documentation

**Document Version**: 1.0.0
**Created**: 2026-04-13T23:00:00Z
**Last Updated**: 2026-04-13T23:00:00Z
**Owner**: AI Assistant
**Status**: Active
**Version**: 1.0.0

---

## 📋 Overview

Labels are **project-level** resources used to categorize work items. Labels can be created with just a name and assigned to multiple work items.

**Location**: `/workspaces/{workspace_slug}/projects/{project_id}/labels`
**Level**: Project
**SDK Version**: plane-python-sdk
**API Instance**: https://your-plane-instance/ (Community Edition)
**Last Tested**: 2026-04-13T23:00:00Z

---

## ✅ Working Operations - Full CRUD

### 1. Create Label

**Endpoint**: `labels.create()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `data: CreateLabel`

**Minimum Required Fields**:

- `name` (string) - Label name

```python
from plane.models.labels import CreateLabel

# Minimal creation
label = client.labels.create(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    data=CreateLabel(name="Bug")
)
```

**With Color**:

```python
label = client.labels.create(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    data=CreateLabel(name="Bug", color="#FF0000")
)
```

**Returns**: `Label` with UUID

**Test Result**: ✅ SUCCESS - Created with just name field

---

### 2. List Labels

**Endpoint**: `labels.list()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`

```python
labels = client.labels.list(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid"
)
```

**Returns**: PaginatedLabelResponse

**Response Structure**:

```python
{
    "total_count": int,
    "total_pages": int,
    "total_results": int,
    "results": [Label, ...],
    "next_cursor": str,
    "prev_cursor": str,
    "next_page_results": bool,
    "prev_page_results": bool
}
```

**Test Result**: ✅ SUCCESS - Returns paginated list

---

### 3. Retrieve Label

**Endpoint**: `labels.retrieve()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `label_id` (UUID)

```python
label = client.labels.retrieve(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    label_id="uuid-here"
)
```

**Returns**: `Label`

**Test Result**: ✅ SUCCESS

---

### 4. Update Label

**Endpoint**: `labels.update()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `label_id`, `data: UpdateLabel`

```python
from plane.models.labels import UpdateLabel

label = client.labels.update(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    label_id="uuid-here",
    data=UpdateLabel(name="Updated Name", color="#0000FF")
)
```

**Returns**: `Label`

**Test Result**: ✅ SUCCESS

---

### 5. Delete Label

**Endpoint**: `labels.delete()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `label_id` (UUID)

```python
client.labels.delete(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    label_id="uuid-here"
)
```

**Returns**: None

**Test Result**: ✅ SUCCESS

---

### 6. Assign Label to Work Item

**Endpoint**: `work_items.update()` with `labels` field
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `work_item_id`, `UpdateWorkItem(labels=[...])`

```python
from plane.models.work_items import UpdateWorkItem

# Assign single label
work_item = client.work_items.update(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    work_item_id="work-item-uuid",
    data=UpdateWorkItem(labels=["label-uuid"])
)

# Assign multiple labels
work_item = client.work_items.update(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    work_item_id="work-item-uuid",
    data=UpdateWorkItem(labels=["label-uuid-1", "label-uuid-2"])
)
```

**Returns**: `WorkItem` with updated labels

**Test Result**: ✅ SUCCESS - Can assign same label to multiple items

---

## 📊 Label Data Structure

### Label Model Fields

| Field         | Type     | Description             | Example                                |
| ------------- | -------- | ----------------------- | -------------------------------------- |
| `id`          | UUID     | Unique label identifier | `503a5de4-5524-4772-b473-6d1057f93c0e` |
| `name`        | str      | Label name              | `"Bug"`                                |
| `description` | str      | Description             | `""`                                   |
| `color`       | str      | Color (hex)             | `#FF0000`                              |
| `sort_order`  | float    | Display order           | `65535.0`                              |
| `workspace`   | UUID     | Parent workspace ID     | `4ef343ce-...`                         |
| `project`     | UUID     | Parent project ID       | `3adb93b5-...`                         |
| `created_at`  | datetime | Creation timestamp      | `2026-04-13T...`                       |
| `updated_at`  | datetime | Update timestamp        | `2026-04-13T...`                       |
| `created_by`  | UUID     | Creator                 | `d92d49db-...`                         |

---

## 🔗 Label Scope

### Where Labels Work

| Resource   | Can Assign Labels? | Notes            |
| ---------- | ------------------ | ---------------- |
| Work Items | ✅ Yes             | Primary use case |
| Projects   | ❌ No              | No labels field  |
| Stickies   | ❌ No              | No labels field  |
| States     | ❌ No              | No labels field  |

### Label Characteristics

- **Created at**: Project level
- **Assigned to**: Multiple work items
- **Search**: No API-level filtering by label
- **Expand**: Use `expand="labels"` when listing work items

---

## 🔧 MCP Tool Implementation Example

```python
from fastmcp import FastMCP
from plane.models.labels import CreateLabel, UpdateLabel

mcp = FastMCP("Plane Labels")

@mcp.tool(description="List labels in project")
async def list_labels(
    workspace_id: str,
    project_id: str
) -> list[dict]:
    """List all labels in project."""
    labels = client.labels.list(
        workspace_slug=workspace_id,
        project_id=project_id
    )
    return [l.model_dump() for l in labels.results]

@mcp.tool(description="Create a new label")
async def create_label(
    workspace_id: str,
    project_id: str,
    name: str,
    color: str | None = None
) -> dict:
    """Create a new label."""
    data = CreateLabel(name=name, color=color)
    label = client.labels.create(
        workspace_slug=workspace_id,
        project_id=project_id,
        data=data
    )
    return label.model_dump()

@mcp.tool(description="Get label by ID")
async def get_label(
    workspace_id: str,
    project_id: str,
    label_id: str
) -> dict:
    """Get label details."""
    label = client.labels.retrieve(
        workspace_slug=workspace_id,
        project_id=project_id,
        label_id=label_id
    )
    return label.model_dump()

@mcp.tool(description="Update label")
async def update_label(
    workspace_id: str,
    project_id: str,
    label_id: str,
    name: str | None = None,
    color: str | None = None
) -> dict:
    """Update label properties."""
    data = UpdateLabel()
    if name:
        data.name = name
    if color:
        data.color = color

    label = client.labels.update(
        workspace_slug=workspace_id,
        project_id=project_id,
        label_id=label_id,
        data=data
    )
    return label.model_dump()

@mcp.tool(description="Delete a label")
async def delete_label(
    workspace_id: str,
    project_id: str,
    label_id: str
) -> dict:
    """Delete a label."""
    client.labels.delete(
        workspace_slug=workspace_id,
        project_id=project_id,
        label_id=label_id
    )
    return {"status": "deleted"}

@mcp.tool(description="Assign label to work item")
async def assign_label(
    workspace_id: str,
    project_id: str,
    work_item_id: str,
    label_id: str
) -> dict:
    """Assign label to work item."""
    work_item = client.work_items.update(
        workspace_slug=workspace_id,
        project_id=project_id,
        work_item_id=work_item_id,
        data=UpdateWorkItem(labels=[label_id])
    )
    return {
        "id": work_item.id,
        "labels": work_item.labels
    }
```

---

## 🧪 Test Results

### Test Date: 2026-04-13T23:00:00Z

| Test           | Status     | Notes                        |
| -------------- | ---------- | ---------------------------- |
| create_label() | ✅ SUCCESS | Works with just name         |
| list_labels()  | ✅ SUCCESS | Returns paginated list       |
| get_label()    | ✅ SUCCESS | Retrieved by UUID            |
| update_label() | ✅ SUCCESS | Updated name and color       |
| delete_label() | ✅ SUCCESS | Deleted successfully         |
| assign_label() | ✅ SUCCESS | Same label on multiple items |

---

## 📝 Important Notes

### Key Points

1. **Minimal Creation**: Labels can be created with just the `name` field
2. **Project-Level**: Labels belong to projects, not workspace
3. **Multiple Assignments**: Same label can be assigned to multiple work items
4. **No API Filtering**: Cannot filter work items by label via API
5. **Expand Option**: Use `expand="labels"` when listing work items

### UUID Management

- Labels are UUID-based
- Use UUID for retrieve/update/delete operations
- Labels are created per project

---

## 🔗 Related Documentation

- [Work Items](../WORK_ITEMS.md) - Labels assigned here
- [Work Item Properties](../work_items/WORK_ITEM_PROPERTIES_REFERENCE.md) - labels field
- [UUID Management Guide](../planning/UUID_AND_DEPENDENCY_GUIDE.md)

---

**Last Updated**: 2026-04-13T23:00:00Z
**Document Version**: 1.0.0
