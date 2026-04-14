# Modules API Documentation

**Document Version**: 1.0.0
**Created**: 2026-04-13T23:30:00Z
**Last Updated**: 2026-04-13T23:30:00Z
**Owner**: AI Assistant
**Status**: Active
**Version**: 1.0.0

---

## 📋 Overview

Modules are **project-level** resources that organize work items within a project. They function as "projects within a project" and track work item counts by status (backlog, started, completed).

**Important**: Modules require `module_view: true` on the parent project to be created.

**Location**: `/workspaces/{workspace_slug}/projects/{project_id}/modules`
**Level**: Project
**SDK Version**: plane-python-sdk
**API Instance**: https://your-plane-instance/ (Community Edition)
**Last Tested**: 2026-04-13T23:30:00Z

---

## ✅ Working Operations - Full CRUD + Work Item Management

### 1. Create Module

**Endpoint**: `modules.create()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `data: CreateModule`

**Minimum Required Fields**:

- `name` (string) - Module name

```python
from plane.models.modules import CreateModule

module = client.modules.create(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    data=CreateModule(name="Backend Module")
)
```

**Returns**: `Module`

**Test Result**: ✅ SUCCESS - Created with just name

---

### 2. List Modules

**Endpoint**: `modules.list()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`

```python
modules = client.modules.list(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid"
)
```

**Returns**: PaginatedModuleResponse

**Response Structure**:

```python
{
    "total_count": int,
    "total_pages": int,
    "total_results": int,
    "results": [Module, ...],
    "next_cursor": str,
    "prev_cursor": str,
    "next_page_results": bool,
    "prev_page_results": bool
}
```

**Test Result**: ✅ SUCCESS

---

### 3. Retrieve Module

**Endpoint**: `modules.retrieve()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `module_id` (UUID)

```python
module = client.modules.retrieve(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    module_id="uuid-here"
)
```

**Returns**: `Module`

**Test Result**: ✅ SUCCESS

---

### 4. Update Module

**Endpoint**: `modules.update()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `module_id`, `data: UpdateModule`

```python
from plane.models.modules import UpdateModule

module = client.modules.update(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    module_id="uuid-here",
    data=UpdateModule(name="Updated Name")
)
```

**Returns**: `Module`

**Test Result**: ✅ SUCCESS

---

### 5. Delete Module

**Endpoint**: `modules.delete()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `module_id`

```python
client.modules.delete(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    module_id="uuid-here"
)
```

**Returns**: None

**Test Result**: ✅ SUCCESS

---

### 6. Add Work Items to Module

**Endpoint**: `modules.add_work_items()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `module_id`, `issue_ids` (list)

```python
client.modules.add_work_items(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    module_id="module-uuid",
    issue_ids=["work-item-uuid-1", "work-item-uuid-2"]
)
```

**Returns**: None (HTTP 204 No Content)

**Test Result**: ✅ SUCCESS - Adds work items to module

---

### 7. List Work Items in Module

**Endpoint**: `modules.list_work_items()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `module_id`

```python
items = client.modules.list_work_items(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    module_id="module-uuid"
)
```

**Returns**: PaginatedModuleWorkItemResponse

**Test Result**: ✅ SUCCESS

---

### 8. Remove Work Item from Module

**Endpoint**: `modules.remove_work_item()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `module_id`, `work_item_id`

```python
client.modules.remove_work_item(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    module_id="module-uuid",
    work_item_id="work-item-uuid"
)
```

**Returns**: None (HTTP 204 No Content)

**Test Result**: ✅ SUCCESS

---

### 9. Archive/Unarchive Module

**Endpoint**: `modules.archive()` / `modules.unarchive()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `module_id`

```python
# Archive
client.modules.archive(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    module_id="module-uuid"
)

# Unarchive
client.modules.unarchive(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    module_id="module-uuid"
)
```

**Returns**: None (HTTP 204 No Content)

---

## 📊 Module Data Structure

### Module Model Fields

| Field              | Type     | Description              | Example                                |
| ------------------ | -------- | ------------------------ | -------------------------------------- |
| `id`               | UUID     | Unique module identifier | `28547e11-fb52-44e4-b736-d3e5b9aa598c` |
| `name`             | str      | Module name              | `"Backend Module"`                     |
| `description`      | str      | Description              | `""`                                   |
| `description_html` | str      | HTML description         | `null`                                 |
| `description_text` | str      | Plain text description   | `null`                                 |
| `status`           | str      | Module status            | `"backlog"`                            |
| `total_issues`     | int      | Total work items         | `2`                                    |
| `backlog_issues`   | int      | Items in backlog         | `1`                                    |
| `started_issues`   | int      | In progress items        | `0`                                    |
| `completed_issues` | int      | Done items               | `0`                                    |
| `cancelled_issues` | int      | Cancelled items          | `0`                                    |
| `unstarted_issues` | int      | Unstarted items          | `1`                                    |
| `sort_order`       | float    | Display order            | `65535.0`                              |
| `start_date`       | str      | Start date               | `null`                                 |
| `target_date`      | str      | Target date              | `null`                                 |
| `view_props`       | dict     | View properties          | `{}`                                   |
| `logo_props`       | dict     | Logo properties          | `{}`                                   |
| `project`          | UUID     | Parent project ID        | `7aa784cb-...`                         |
| `workspace`        | UUID     | Parent workspace ID      | `4ef343ce-...`                         |
| `lead`             | str      | Module lead UUID         | `null`                                 |
| `created_by`       | UUID     | Creator                  | `d92d49db-...`                         |
| `updated_by`       | UUID     | Last updater             | `null`                                 |
| `created_at`       | datetime | Creation timestamp       | `2026-04-13T...`                       |
| `updated_at`       | datetime | Update timestamp         | `2026-04-13T...`                       |
| `archived_at`      | datetime | Archive timestamp        | `null`                                 |
| `external_source`  | str      | External source          | `null`                                 |
| `external_id`      | str      | External ID              | `null`                                 |

---

## 🔧 MCP Tool Implementation Example

```python
from fastmcp import FastMCP
from plane.models.modules import CreateModule, UpdateModule

mcp = FastMCP("Plane Modules")

@mcp.tool(description="List modules in project")
async def list_modules(
    workspace_id: str,
    project_id: str
) -> list[dict]:
    """List all modules in project."""
    modules = client.modules.list(
        workspace_slug=workspace_id,
        project_id=project_id
    )
    return [m.model_dump() for m in modules.results]

@mcp.tool(description="Create a new module")
async def create_module(
    workspace_id: str,
    project_id: str,
    name: str
) -> dict:
    """Create a new module."""
    module = client.modules.create(
        workspace_slug=workspace_id,
        project_id=project_id,
        data=CreateModule(name=name)
    )
    return module.model_dump()

@mcp.tool(description="Add work items to module")
async def add_work_items_to_module(
    workspace_id: str,
    project_id: str,
    module_id: str,
    work_item_ids: list[str]
) -> dict:
    """Add work items to a module."""
    client.modules.add_work_items(
        workspace_slug=workspace_id,
        project_id=project_id,
        module_id=module_id,
        issue_ids=work_item_ids
    )
    return {"status": "added", "count": len(work_item_ids)}

@mcp.tool(description="List work items in module")
async def list_work_items_in_module(
    workspace_id: str,
    project_id: str,
    module_id: str
) -> list[dict]:
    """List work items assigned to module."""
    items = client.modules.list_work_items(
        workspace_slug=workspace_id,
        project_id=project_id,
        module_id=module_id
    )
    return [i.model_dump() for i in items.results]

@mcp.tool(description="Delete a module")
async def delete_module(
    workspace_id: str,
    project_id: str,
    module_id: str
) -> dict:
    """Delete a module."""
    client.modules.delete(
        workspace_slug=workspace_id,
        project_id=project_id,
        module_id=module_id
    )
    return {"status": "deleted"}
```

---

## 🧪 Test Results

### Test Date: 2026-04-13T23:30:00Z

| Test                        | Status     | Notes                    |
| --------------------------- | ---------- | ------------------------ |
| list_modules()              | ✅ SUCCESS | Found 1 module           |
| create_module()             | ✅ SUCCESS | Created with name only   |
| retrieve_module()           | ✅ SUCCESS | Retrieved by UUID        |
| update_module()             | ✅ SUCCESS | Updated name             |
| delete_module()             | ✅ SUCCESS | Deleted successfully     |
| add_work_items()            | ✅ SUCCESS | Added 2 items to module  |
| list_work_items_in_module() | ✅ SUCCESS | Found 2 items            |
| remove_work_item()          | ✅ SUCCESS | Removed item from module |

**Module Status Tracking**:

- Total Issues: 2
- Backlog Issues: 1
- Started Issues: 0
- Completed Issues: 0
- Unstarted Issues: 1

---

## 📝 Important Notes

### Key Points

1. **Project Requirement**: Modules can only be created on projects with `module_view: true`
2. **Separate API**: Work items are added to modules via a separate endpoint, not via work item fields
3. **Status Tracking**: Modules track work items by status (backlog, started, completed)
4. **No Direct Assignment**: Work items don't have `module_id` field - use `add_work_items()` endpoint
5. **Organizational**: Modules are for organization, not filtering

### UUID Management

- Modules are UUID-based
- Use UUID for all operations except create
- Work items are added via separate API call

---

## 🔗 Related Documentation

- [Projects](PROJECTS.md) - Parent resource with module_view flag
- [Work Items](WORK_ITEMS.md) - Items that can be added to modules
- [Labels](work_items/LABELS.md) - Alternative organization method
- [UUID Management Guide](../planning/UUID_AND_DEPENDENCY_GUIDE.md)

---

## 🚀 Next Steps

1. Test archive/unarchive functionality
2. Test module lead assignment
3. Test module work item state tracking
4. Test bulk operations

---

**Last Updated**: 2026-04-13T23:30:00Z
**Document Version**: 1.0.0
