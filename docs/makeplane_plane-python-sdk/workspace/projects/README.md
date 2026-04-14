# Projects API Documentation

**Document Version**: 1.0.0
**Created**: 2026-04-13T19:45:00Z
**Last Updated**: 2026-04-13T19:45:00Z
**Owner**: AI Assistant
**Status**: Active
**Version**: 1.0.0

---

## 📋 Overview

Projects are **project-level** resources within a workspace. Unlike Stickies which are workspace-level, projects require a project context for most operations.

**API Endpoint**: `/workspaces/{workspace_slug}/projects`
**Level**: Project
**SDK Version**: plane-python-sdk
**API Instance**: https://your-plane-instance/ (Community Edition)
**Last Tested**: 2026-04-13T19:45:00Z

---

## ✅ Working Endpoints

All project endpoints work successfully with proper UUID management.

### 1. List Projects

**Endpoint**: `projects.list()`
**Level**: Workspace
**Parameters**: `workspace_slug`, `params: PaginatedQueryParams`

```python
projects = client.projects.list(
    workspace_slug="your-workspace-slug",
    params=PaginatedQueryParams(per_page=20)
)
```

**Returns**: `PaginatedProjectResponse`

**Response Structure**:

```python
{
    "count": int,
    "total_pages": int,
    "total_results": int,
    "results": [Project, ...]
}
```

**Example Output**:

```python
[
    Project(
        id='3adb93b5-6a0c-4783-862e-5f2d7b17783d',
        name='Test Project',
        identifier='TEST1',
        description='',
        total_members=1,
        total_cycles=0,
        total_modules=0,
        is_member=True,
        sort_order=85535.0,
        created_at='2026-03-25T09:58:10.713462-07:00',
        updated_at='2026-03-25T09:58:16.268514-07:00',
        deleted_at=None,
        workspace='4ef343ce-78f0-4f96-896b-b5c7fa63dd8c'
    )
]
```

---

### 2. Create Project

**Endpoint**: `projects.create()`
**Level**: Workspace
**Parameters**: `workspace_slug`, `data: CreateProject`

```python
from plane.models.projects import CreateProject

data = CreateProject(
    name="New Project",
    identifier="PROJ-123"  # Required!
)

project = client.projects.create(
    workspace_slug="your-workspace-slug",
    data=data
)
```

**Returns**: `Project`

**CreateProject Model**:

```python
class CreateProject(BaseModel):
    name: str
    identifier: str  # Required - unique identifier
    description: Optional[str] = None
    type: Optional[str] = None  # e.g., "backlog", "kanban"
    lead: Optional[str] = None  # User ID
```

**Example Response**:

```python
Project(
    id='2f5a5048-09df-471d-9692-4b38016e9f13',
    name='Test Project for MCP',
    identifier='TESTPROJ',
    description='',
    total_members=1,
    total_cycles=0,
    total_modules=0,
    created_at='2026-04-13T19:45:00.000000-07:00',
    updated_at='2026-04-13T19:45:00.000000-07:00',
    deleted_at=None,
    workspace='4ef343ce-78f0-4f96-896b-b5c7fa63dd8c'
)
```

**Test Result**: ✅ SUCCESS - Created project successfully

---

### 3. Retrieve Project

**Endpoint**: `projects.retrieve()`
**Level**: Workspace
**Parameters**: `workspace_slug`, `project_id` (UUID)

```python
project = client.projects.retrieve(
    workspace_slug="your-workspace-slug",
    project_id="2f5a5048-09df-471d-9692-4b38016e9f13"
)
```

**Returns**: `Project`

**Note**: Requires UUID, not identifier

---

### 4. Update Project

**Endpoint**: `projects.update()`
**Level**: Workspace
**Parameters**: `workspace_slug`, `project_id`, `data: UpdateProject`

```python
from plane.models.projects import UpdateProject

data = UpdateProject(
    name="Updated Project Name",
    description="Updated description"
)

project = client.projects.update(
    workspace_slug="your-workspace-slug",
    project_id="2f5a5048-09df-471d-9692-4b38016e9f13",
    data=data
)
```

**Returns**: `Project`

**UpdateProject Model**:

```python
class UpdateProject(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    lead: Optional[str] = None
```

**Test Result**: ✅ SUCCESS - Updated project successfully

---

### 5. Delete Project

**Endpoint**: `projects.delete()`
**Level**: Workspace
**Parameters**: `workspace_slug`, `project_id` (UUID)

```python
client.projects.delete(
    workspace_slug="your-workspace-slug",
    project_id="2f5a5048-09df-471d-9692-4b38016e9f13"
)
```

**Returns**: `None`

**Test Result**: ✅ SUCCESS - Deleted project successfully

---

## 📊 Project Data Structure

### Project Model Fields

| Field           | Type               | Description               | Example                                |
| --------------- | ------------------ | ------------------------- | -------------------------------------- |
| `id`            | UUID               | Unique project identifier | `2f5a5048-09df-471d-9692-4b38016e9f13` |
| `name`          | str                | Project name              | `"Test Project"`                       |
| `identifier`    | str                | Human-readable identifier | `"TEST1"`                              |
| `description`   | str                | Project description       | `""`                                   |
| `total_members` | int                | Number of members         | `1`                                    |
| `total_cycles`  | int                | Number of cycles          | `0`                                    |
| `total_modules` | int                | Number of modules         | `0`                                    |
| `is_member`     | bool               | Is current user a member  | `True`                                 |
| `sort_order`    | float              | Display order             | `85535.0`                              |
| `created_at`    | datetime           | Creation timestamp        | `2026-03-25T09:58:10.713462-07:00`     |
| `updated_at`    | datetime           | Last update timestamp     | `2026-03-25T09:58:16.268514-07:00`     |
| `deleted_at`    | Optional[datetime] | Deletion timestamp        | `None`                                 |
| `workspace`     | UUID               | Parent workspace ID       | `4ef343ce-78f0-4f96-896b-b5c7fa63dd8c` |

---

## 🔧 MCP Tool Implementation Example

```python
from fastmcp import FastMCP
from plane.models.projects import CreateProject

mcp = FastMCP("Plane Projects")

@mcp.tool(description="List all projects in workspace")
async def list_projects(workspace_id: str) -> dict:
    """List all workspace projects."""
    projects = client.projects.list(workspace_slug=workspace_id)
    return {
        "projects": [
            {
                "id": p.id,
                "name": p.name,
                "identifier": p.identifier,
                "total_members": p.total_members
            }
            for p in (projects.results or [])
        ],
        "count": len(projects.results) if projects.results else 0
    }

@mcp.tool(description="Create a new project")
async def create_project(
    workspace_id: str,
    name: str,
    identifier: str
) -> dict:
    """Create a new project."""
    data = CreateProject(name=name, identifier=identifier)
    project = client.projects.create(
        workspace_slug=workspace_id,
        data=data
    )
    return {
        "id": project.id,
        "name": project.name,
        "identifier": project.identifier
    }

@mcp.tool(description="Get project details")
async def get_project(workspace_id: str, project_id: str) -> dict:
    """Get project details by UUID."""
    project = client.projects.retrieve(
        workspace_slug=workspace_id,
        project_id=project_id
    )
    return {
        "id": project.id,
        "name": project.name,
        "identifier": project.identifier,
        "total_members": project.total_members
    }
```

---

## 🧪 Test Results

### Test Date: 2026-04-13T19:45:00Z

| Test               | Status     | Notes                            |
| ------------------ | ---------- | -------------------------------- |
| list_projects()    | ✅ SUCCESS | Returns 6 existing projects      |
| create_project()   | ✅ SUCCESS | Creates new project with UUID    |
| retrieve_project() | ✅ SUCCESS | Retrieves by UUID                |
| update_project()   | ✅ SUCCESS | Updates project name/description |
| delete_project()   | ✅ SUCCESS | Deletes project                  |

**Test Script**: `/tmp/test_projects_deep.py`
**Test Output**: All 5 operations successful

---

## 📝 Important Notes

### Key Points

1. **Identifier Required**: Create project requires unique identifier
2. **UUID Management**: Use UUID for retrieve/update/delete operations
3. **Workspace-Level**: Projects are created in workspace, accessed by UUID
4. **Pagination**: Use `PaginatedQueryParams(per_page=N)` for list operations

### UUID Management Pattern

```python
# 1. List to get UUID
projects = client.projects.list(workspace_slug=workspace_slug)
project_uuid = projects.results[0].id

# 2. Use UUID for modify operations
client.projects.update(
    workspace_slug=workspace_slug,
    project_id=project_uuid,  # UUID, not identifier!
    data=data
)
```

---

## 🔗 Related Documentation

- [Stickies Documentation](STICKIES.md) - Workspace-level resource
- [UUID Management Guide](../planning/UUID_AND_DEPENDENCY_GUIDE.md)
- [SDK API Mapping](../planning/SDK_API_MAPPING.md)

---

## 📚 References

- **SDK Source**: `plane.api.projects`
- **SDK Models**: `plane.models.projects`
- **Test Script**: `/tmp/test_projects_deep.py`

---

**Last Updated**: 2026-04-13T19:45:00Z
**Document Version**: 1.0.0

---

## 📊 Project Feature Flags

Projects have several feature flags that control what is available:

| Flag                       | Description                               | Default | Example Value |
| -------------------------- | ----------------------------------------- | ------- | ------------- |
| `module_view`              | Enable modules (projects within projects) | False   | True/False    |
| `cycle_view`               | Enable cycles (timeboxes)                 | False   | True/False    |
| `page_view`                | Enable kanban board view                  | True    | True/False    |
| `intake_view`              | Enable intake form                        | False   | True/False    |
| `is_time_tracking_enabled` | Enable time tracking                      | False   | True/False    |
| `is_issue_type_enabled`    | Enable custom issue types                 | False   | True/False    |
| `guest_view_all_features`  | Guest access to all features              | False   | True/False    |

### Example: Project with Modules Enabled

```json
{
    "module_view": true,
    "cycle_view": true,
    "page_view": true,
    "total_modules": 1,
    "total_cycles": 0
}
```

**Note**: Modules and Cycles cannot be created if their respective view flags are `false`.

---

## 🎨 Project Branding & Customization

Projects support custom branding:

- **Emoji**: Project emoji identifier (e.g., `"128204"`)
- **Icon Prop**: Icon property settings
- **Logo Props**: Logo/icon configuration
- **Cover Image**: Custom cover image URL
- **Cover Image Asset**: Cover image asset ID

---

## 📊 Project Configuration

- **Network**: Network ID (e.g., `2`)
- **Sort Order**: Display order (e.g., `15535.0`)
- **Member Role**: Current user's role (e.g., `20` = member)
- **Is Member**: Whether current user is a member
- **Timezone**: Project timezone (e.g., `"UTC"`)
- **Default Assignee**: Default assignee UUID
- **Project Lead**: Project lead UUID
- **Default State**: Default state UUID
- **Estimate**: Budget/estimate value

---

## 🔗 Related Documentation

- [Labels](work_items/LABELS.md) - Label features
- [Work Items](WORK_ITEMS.md) - Work item features
- [UUID Management](../planning/UUID_AND_DEPENDENCY_GUIDE.md)

---

**Last Updated**: 2026-04-13T23:05:00Z
**Document Version**: 1.0.1

## 🎯 Project Features

Projects have several feature flags that control what capabilities are available:

### Feature Flags

| Flag                       | Description                  | Type    |
| -------------------------- | ---------------------------- | ------- |
| `module_view`              | Enable modules feature       | Boolean |
| `cycle_view`               | Enable cycles feature        | Boolean |
| `page_view`                | Enable pages feature         | Boolean |
| `intake_view`              | Enable intake feature        | Boolean |
| `is_time_tracking_enabled` | Enable time tracking         | Boolean |
| `is_issue_type_enabled`    | Enable issue types           | Boolean |
| `guest_view_all_features`  | Guest access to all features | Boolean |

### Available Features

#### 1. Modules ✅ Working

- **Level**: Project
- **Feature Flag**: `module_view: true`
- **Description**: Projects within projects for organizing work
- **API Methods**:
    - `modules.create()` - Create module
    - `modules.list()` - List modules
    - `modules.retrieve()` - Get module by ID
    - `modules.update()` - Update module
    - `modules.delete()` - Delete module
    - `modules.add_work_items()` - Add work items to module
    - `modules.list_work_items()` - List work items in module
    - `modules.remove_work_item()` - Remove work item from module
    - `modules.archive()` - Archive module
    - `modules.unarchive()` - Unarchive module

**See**: [Modules](MODULES.md) for full documentation.

#### 2. Cycles ⚠️ CE Limited

- **Level**: Project
- **Feature Flag**: `cycle_view: true`
- **Description**: Time-based planning cycles (sprints/iterations)
- **API Methods**:
    - `cycles.create()` - Create cycle
    - `cycles.list()` - List cycles
    - `cycles.retrieve()` - Get cycle by ID
    - `cycles.update()` - Update cycle
    - `cycles.delete()` - Delete cycle
    - `cycles.list_archived()` - List archived cycles
    - `cycles.add_work_items()` - Add work items to cycle
    - `cycles.remove_work_item()` - Remove work item from cycle
    - `cycles.list_work_items()` - List work items in cycle
    - `cycles.transfer_work_items()` - Transfer work items
    - `cycles.archive()` - Archive cycle
    - `cycles.unarchive()` - Unarchive cycle

**Required Fields for CreateCycle**:

- `name` (str) - Cycle name
- `owned_by` (str) - Owner ID
- `project_id` (str) - Project ID

**Status**: API fully implemented, may be CE limited or require project configuration.

#### 3. Pages ⚠️ CE Limited

- **Level**: Workspace / Project
- **Feature Flag**: `page_view: true`
- **Description**: Visual dashboards for project overview
- **API Methods**:
    - `pages.create_workspace_page()` - Create workspace page
    - `pages.create_project_page()` - Create project page
    - `pages.retrieve_workspace_page()` - Get workspace page
    - `pages.retrieve_project_page()` - Get project page

**Required Fields for CreatePage**:

- `name` (str) - Page name
- `description_html` (str) - HTML description

**Status**: API available, may be CE limited or require additional configuration.

#### 4. Intake ⚠️ Unknown

- **Level**: Project
- **Feature Flag**: `intake_view: true`
- **Description**: Intake for new work items
- **API File**: `plane/api/intake.py`
- **Status**: Requires investigation

---

## 🔗 Related Features

- [Work Items](../work_items/README.md) - Core work items with labels and modules
- [Labels](LABELS.md) - Categorize work items
- [Modules](MODULES.md) - Organize work items
- [Cycles](../SESSION_SUMMARY.md) - Time-based planning
- [Pages](../SESSION_SUMMARY.md) - Visual dashboards
- [States](../STATES.md) - Work item states

---

**Last Updated**: 2026-04-13T23:57:00Z
**Document Version**: 1.0.0
