# CRUD Minimum Fields Reference

**Created**: 2026-04-14T01:40:00Z
**Owner**: AI Assistant
**Status**: Reference
**Version**: 0.1.0

---

## 📋 Overview

This document summarizes the **minimum required fields** for creating, updating, and deleting resources in the Plane Python SDK.

Based on our testing with `plane-python-sdk` v0.2.8.

---

## 🗂️ Resource Hierarchy

```
Workspace (Teamspace)
└── Project
    ├── Work Items (Issues/Tasks)
    │   ├── Labels
    │   ├── Modules
    │   └── States
    ├── Cycles
    ├── Pages
    └── Intake
└── Members/Users
```

---

## 🏗️ Workspace / Teamspace

### Create Workspace

**SDK Method**: `teamspaces.create()`

**Minimum Required Fields**:

- ❓ **Requires investigation** - Not fully tested in CE

**Optional Fields**:

- `name` (str)
- `description` (str)
- `icon_prop` (str)
- `cover_image` (str)

---

### Update Workspace

**SDK Method**: `teamspaces.update()`

**Minimum Required Fields**: None (partial update)

**Optional Fields**:

- `name` (str)
- `description` (str)
- `icon_prop` (str)
- `cover_image` (str)

---

### Delete Workspace

**SDK Method**: `teamspaces.delete()`

**Required Parameters**: `workspace_slug`, `teamspace_id` (UUID)

---

### List Workspaces

**SDK Method**: `teamspaces.list()`

**Required Parameters**: `workspace_slug`

---

## 📁 Project

### Create Project

**SDK Method**: `projects.create()`

**Minimum Required Fields**:

```python
from plane.models.projects import CreateProject

data = CreateProject(
    name="Project Name",      # ✅ Required
    identifier="PROJ-123"     # ✅ Required - must be unique
)
```

| Field         | Type | Required | Notes                                |
| ------------- | ---- | -------- | ------------------------------------ |
| `name`        | str  | ✅ Yes   | Human-readable name                  |
| `identifier`  | str  | ✅ Yes   | Unique identifier (e.g., "PROJ-123") |
| `description` | str  | ❌ No    | Optional description                 |
| `type`        | str  | ❌ No    | e.g., "backlog", "kanban"            |
| `lead`        | str  | ❌ No    | User ID                              |

**Test Result**: ✅ SUCCESS - Created with name + identifier

---

### Update Project

**SDK Method**: `projects.update()`

**Minimum Required Fields**: None (partial update)

**Optional Fields**:

- `name` (str)
- `description` (str)
- `type` (str)
- `lead` (str)

**Test Result**: ✅ SUCCESS - Partial updates work

---

### Delete Project

**SDK Method**: `projects.delete()`

**Required Parameters**: `workspace_slug`, `project_id` (UUID)

**Test Result**: ✅ SUCCESS

---

### List Projects

**SDK Method**: `projects.list()`

**Required Parameters**: `workspace_slug`

**Optional Parameters**: `PaginatedQueryParams(per_page=N)`

**Test Result**: ✅ SUCCESS - Returns paginated list

---

## 📝 Work Items (Tasks/Issues)

### Create Work Item

**SDK Method**: `work_items.create()`

**Minimum Required Fields**:

```python
from plane.models.work_items import CreateWorkItem

# ✅ ONLY NAME IS REQUIRED!
data = CreateWorkItem(
    name="Task Title"  # ✅ Required - everything else is optional!
)
```

| Field              | Type      | Required | Notes                                 |
| ------------------ | --------- | -------- | ------------------------------------- |
| `name`             | str       | ✅ Yes   | Title of work item                    |
| `description`      | str       | ❌ No    | Plain text description                |
| `description_html` | str       | ❌ No    | HTML description                      |
| `priority`         | str       | ❌ No    | e.g., "none", "low", "medium", "high" |
| `state`            | UUID      | ❌ No    | State UUID                            |
| `labels`           | list[str] | ❌ No    | Label UUIDs                           |
| `assignees`        | list[str] | ❌ No    | User UUIDs                            |
| `point`            | int       | ❌ No    | Story points                          |
| `parent`           | UUID      | ❌ No    | Parent work item UUID                 |

**Test Result**: ✅ SUCCESS - Created with just name field!

---

### Update Work Item

**SDK Method**: `work_items.update()`

**Minimum Required Fields**: None (partial update)

**Optional Fields**:

- `name` (str)
- `description` (str)
- `priority` (str)
- `state` (UUID)
- `labels` (list[str])
- `assignees` (list[str])
- `point` (int)
- `parent` (UUID)

**Test Result**: ✅ SUCCESS - Partial updates work

---

### Delete Work Item

**SDK Method**: `work_items.delete()`

**Required Parameters**: `workspace_slug`, `project_id`, `work_item_id` (UUID)

**Test Result**: ✅ SUCCESS

---

### List Work Items

**SDK Method**: `work_items.list()`

**Required Parameters**: `workspace_slug`, `project_id`

**Optional Parameters**: `WorkItemQueryParams(state, labels, assignees, priority, point, parent)`

**Test Result**: ✅ SUCCESS

---

### Search Work Items

**SDK Method**: `work_items.search()`

**Required Parameters**: `workspace_slug`, `query` (text)

**Test Result**: ✅ SUCCESS

---

## 🏷️ Labels

### Create Label

**SDK Method**: `labels.create()`

**Minimum Required Fields**:

```python
from plane.models.labels import CreateLabel

# ✅ ONLY NAME IS REQUIRED!
label = client.labels.create(
    workspace_slug=workspace_slug,
    project_id=project_id,
    data=CreateLabel(name="Bug")  # ✅ Required!
)
```

| Field         | Type  | Required | Notes                       |
| ------------- | ----- | -------- | --------------------------- |
| `name`        | str   | ✅ Yes   | Label name                  |
| `color`       | str   | ❌ No    | Hex color (e.g., "#FF0000") |
| `description` | str   | ❌ No    | Optional description        |
| `sort_order`  | float | ❌ No    | Display order               |

**Test Result**: ✅ SUCCESS - Created with just name field

---

### Update Label

**SDK Method**: `labels.update()`

**Minimum Required Fields**: None (partial update)

**Optional Fields**:

- `name` (str)
- `color` (str)
- `description` (str)
- `sort_order` (float)

**Test Result**: ✅ SUCCESS

---

### Delete Label

**SDK Method**: `labels.delete()`

**Required Parameters**: `workspace_slug`, `project_id`, `label_id` (UUID)

**Test Result**: ✅ SUCCESS

---

### List Labels

**SDK Method**: `labels.list()`

**Required Parameters**: `workspace_slug`, `project_id`

**Test Result**: ✅ SUCCESS

---

### Assign Label to Work Item

**SDK Method**: `work_items.update()` with `labels` field

```python
from plane.models.work_items import UpdateWorkItem

# Assign label to work item
work_item = client.work_items.update(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    work_item_id=work_item_uuid,
    data=UpdateWorkItem(labels=["label-uuid"])
)
```

**Test Result**: ✅ SUCCESS - Can assign same label to multiple items

---

## 📦 Modules

### Create Module

**SDK Method**: `modules.create()`

**Minimum Required Fields**:

```python
from plane.models.modules import CreateModule

# Requires module_view: true on project
data = CreateModule(
    name="Module Name",      # ✅ Required
    identifier="MOD-123"     # ✅ Required
)
```

| Field         | Type | Required | Notes                |
| ------------- | ---- | -------- | -------------------- |
| `name`        | str  | ✅ Yes   | Module name          |
| `identifier`  | str  | ✅ Yes   | Unique identifier    |
| `description` | str  | ❌ No    | Optional description |

**Test Result**: ⚠️ Requires `module_view: true` on project

---

### Update Module

**SDK Method**: `modules.update()`

**Minimum Required Fields**: None (partial update)

**Optional Fields**:

- `name` (str)
- `description` (str)

**Test Result**: ✅ SUCCESS

---

### Delete Module

**SDK Method**: `modules.delete()`

**Required Parameters**: `workspace_slug`, `project_id`, `module_id` (UUID)

**Test Result**: ✅ SUCCESS

---

### Add Work Items to Module

**SDK Method**: `modules.add_work_items()`

**Required Parameters**: `workspace_slug`, `project_id`, `module_id`, `issue_ids` (list[UUID])

**Test Result**: ✅ SUCCESS

---

## 🔄 Cycles

### Create Cycle

**SDK Method**: `cycles.create()`

**Minimum Required Fields**:

```python
from plane.models.cycles import CreateCycle

# Requires cycle_view: true on project
data = CreateCycle(
    name="Cycle Name",      # ✅ Required
    owned_by="user-uuid",   # ✅ Required
    project_id="project-uuid"  # ✅ Required
)
```

| Field        | Type | Required | Notes                       |
| ------------ | ---- | -------- | --------------------------- |
| `name`       | str  | ✅ Yes   | Cycle name                  |
| `owned_by`   | UUID | ✅ Yes   | Owner UUID                  |
| `project_id` | UUID | ✅ Yes   | Parent project UUID         |
| `cycle_type` | str  | ❌ No    | e.g., "sprint", "milestone" |

**Test Result**: ⚠️ Returns HTTP 400 (needs validation)

---

### Update Cycle

**SDK Method**: `cycles.update()`

**Minimum Required Fields**: None (partial update)

**Optional Fields**:

- `name` (str)

**Test Result**: ⏳ Not tested

---

### Delete Cycle

**SDK Method**: `cycles.delete()`

**Required Parameters**: `workspace_slug`, `project_id`, `cycle_id` (UUID)

**Test Result**: ⏳ Not tested

---

## 🖼️ Pages

**Status**: ⚠️ Returns HTTP 404 (Docker configuration issue)

**Not available in current setup**

---

## 👥 Members / Users

### Create Member

**SDK Method**: `users.create()`

**Minimum Required Fields**:

- ❓ **Requires investigation** - Not fully tested

**Optional Fields**:

- `email` (str)
- `name` (str)

---

### Update Member

**SDK Method**: `users.update()`

**Minimum Required Fields**: None (partial update)

**Optional Fields**:

- `email` (str)
- `name` (str)

---

### Delete Member

**SDK Method**: `users.delete()`

**Required Parameters**: `workspace_slug`, `user_id` (UUID)

---

## 📊 States

### Create State

**SDK Method**: `states.create()`

**Minimum Required Fields**:

- ❓ **Requires investigation** - Not fully tested

**Optional Fields**:

- `name` (str)
- `sort_order` (float)

---

### Update State

**SDK Method**: `states.update()`

**Minimum Required Fields**: None (partial update)

**Optional Fields**:

- `name` (str)
- `sort_order` (float)

---

## 🚀 MCP Tool Design Patterns

### 1. Project Commands

```python
@mcp.tool(description="Create a new project")
async def project_create(
    workspace_id: str,
    name: str,
    identifier: str  # ✅ Required
) -> dict:
    """Create project with name and identifier."""
    data = CreateProject(name=name, identifier=identifier)
    return client.projects.create(...)
```

### 2. Work Item Commands

```python
@mcp.tool(description="Add a new work item (task/issue)")
async def work_add(
    workspace_id: str,
    project_id: str,
    title: str  # ✅ ONLY REQUIRED FIELD!
) -> dict:
    """Create work item - just the title needed!"""
    data = CreateWorkItem(name=title)
    return client.work_items.create(...)
```

### 3. Label Commands

```python
@mcp.tool(description="Create a new label")
async def label_create(
    workspace_id: str,
    project_id: str,
    name: str  # ✅ ONLY REQUIRED FIELD!
) -> dict:
    """Create label with just the name."""
    data = CreateLabel(name=name)
    return client.labels.create(...)
```

### 4. Module Commands

```python
@mcp.tool(description="Create a new module")
async def module_create(
    workspace_id: str,
    project_id: str,
    name: str,
    identifier: str  # ✅ Required
) -> dict:
    """Create module with name and identifier."""
    data = CreateModule(name=name, identifier=identifier)
    return client.modules.create(...)
```

---

## 📝 Important Notes

### Key Findings

1. **Work Items**: Can be created with just `name` field - API auto-generates everything else
2. **Labels**: Can be created with just `name` field - very flexible
3. **Projects**: Require both `name` AND `identifier` - identifier must be unique
4. **Modules**: Require `name` AND `identifier` - similar to projects
5. **Cycles**: Require `name`, `owned_by`, and `project_id` - more complex

### UUID Management Pattern

```python
# 1. List to get UUID
projects = client.projects.list(workspace_slug=workspace_slug)
project_uuid = projects.results[0].id

# 2. Create resource (needs minimal fields)
data = CreateWorkItem(name="Task Title")
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

### Common Patterns

| Resource  | Create Min Fields            | Update Fields | Delete Params |
| --------- | ---------------------------- | ------------- | ------------- |
| Project   | name + identifier            | Partial       | UUID          |
| Work Item | name                         | Partial       | UUID          |
| Label     | name                         | Partial       | UUID          |
| Module    | name + identifier            | Partial       | UUID          |
| Cycle     | name + owned_by + project_id | Partial       | UUID          |

---

## 🔗 Related Documentation

- [Projects API](workspace/projects/README.md)
- [Work Items API](workspace/projects/WORK_ITEMS.md)
- [Labels API](workspace/projects/LABELS.md)
- [Modules API](workspace/projects/MODULES.md)
- [Cycles API](workspace/projects/CYCLES.md)
- [UUID Management Guide](../planning/UUID_AND_DEPENDENCY_GUIDE.md)

---

**Last Updated**: 2026-04-14T01:40:00Z
**Version**: 0.1.0
