# Workspaces / Teamspaces API Documentation

**Created**: 2026-04-14T01:50:00Z
**Owner**: AI Assistant
**Status**: Draft
**Version**: 0.1.0

---

## 📋 Overview

Workspaces (referred to as "Teamspaces" in the SDK) are **top-level resources** that contain projects. This is a workspace-level API that allows you to manage multiple workspaces and access projects within them.

**Note**: This API is less commonly used for day-to-day work, as most users work within a single workspace. However, it's useful for:

- Multi-workspace applications
- Admin/management tools
- Workspace discovery

---

## 🏗️ Resource Hierarchy

```
Teamspaces (Workspaces)
└── Projects
    ├── Work Items
    ├── Labels
    ├── Modules
    └── Cycles
```

---

## 📊 API Methods

### 1. List Teamspaces (Workspaces)

**Endpoint**: `teamspaces.list()`
**Level**: Global (requires authentication)
**Parameters**: `workspace_slug` (filter)

```python
from plane_sdk import PlaneClientWrapper

client = PlaneClientWrapper(
    base_url="https://api.plane.so",
    api_key="your-api-key"
)

# List all teamspaces
teamspaces = client.teamspaces.list()
print(f"Found {teamspaces.count} teamspace(s)")

# Filter by workspace_slug
teamspaces = client.teamspaces.list(
    workspace_slug="your-workspace-slug"
)
```

**Returns**: `PaginatedTeamspaceResponse`

**Response Structure**:

```python
class PaginatedTeamspaceResponse(BaseModel):
    count: int
    total_pages: int
    total_results: int
    results: List[Teamspace]
```

**Test Status**: ⏳ **Not Yet Tested**

---

### 2. Create Teamspace

**Endpoint**: `teamspaces.create()`
**Level**: Global
**Parameters**: `workspace_slug`, `data: CreateTeamspace`

```python
from plane.models.teamspaces import CreateTeamspace

data = CreateTeamspace(
    name="My Workspace",
    description="A workspace for my projects"
)

teamspace = client.teamspaces.create(
    workspace_slug="your-workspace-slug",
    data=data
)
```

**Returns**: `Teamspace`

**Required Fields**:

- ❓ **Requires investigation** - Not fully documented

**Optional Fields**:

- `name` (str)
- `description` (str)
- `icon_prop` (str)
- `cover_image` (str)

**Test Status**: ⏳ **Not Yet Tested**

---

### 3. Retrieve Teamspace

**Endpoint**: `teamspaces.retrieve()`
**Level**: Global
**Parameters**: `workspace_slug`, `teamspace_id` (UUID)

```python
teamspace = client.teamspaces.retrieve(
    workspace_slug="your-workspace-slug",
    teamspace_id="teamspace-uuid-here"
)
```

**Returns**: `Teamspace`

**Note**: Uses `teamspace_id` for retrieve, not `workspace_slug`

**Test Status**: ⏳ **Not Yet Tested**

---

### 4. Update Teamspace

**Endpoint**: `teamspaces.update()`
**Level**: Global
**Parameters**: `workspace_slug`, `teamspace_id`, `data: UpdateTeamspace`

```python
from plane.models.teamspaces import UpdateTeamspace

data = UpdateTeamspace(
    name="Updated Workspace Name"
)

teamspace = client.teamspaces.update(
    workspace_slug="your-workspace-slug",
    teamspace_id="teamspace-uuid-here",
    data=data
)
```

**Returns**: `Teamspace`

**Test Status**: ⏳ **Not Yet Tested**

---

### 5. Delete Teamspace

**Endpoint**: `teamspaces.delete()`
**Level**: Global
**Parameters**: `workspace_slug`, `teamspace_id` (UUID)

```python
client.teamspaces.delete(
    workspace_slug="your-workspace-slug",
    teamspace_id="teamspace-uuid-here"
)
```

**Returns**: `None`

**Test Status**: ⏳ **Not Yet Tested**

---

## 📊 Teamspace Data Structure

### Teamspace Model Fields

| Field         | Type     | Description           | Example                                |
| ------------- | -------- | --------------------- | -------------------------------------- |
| `id`          | UUID     | Unique workspace ID   | `4ef343ce-78f0-4f96-896b-b5c7fa63dd8c` |
| `name`        | str      | Workspace name        | `"My Workspace"`                       |
| `description` | str      | Workspace description | `""`                                   |
| `icon_prop`   | str      | Icon identifier       | `"128204"`                             |
| `cover_image` | str      | Cover image URL       | `""`                                   |
| `workspace`   | UUID     | Parent workspace ID   | (may be null for root)                 |
| `created_at`  | datetime | Creation timestamp    | `2026-04-13T...`                       |
| `updated_at`  | datetime | Update timestamp      | `2026-04-13T...`                       |
| `deleted_at`  | datetime | Deletion timestamp    | `None`                                 |

---

## 🔧 MCP Tool Implementation Example

```python
from fastmcp import FastMCP
from plane_sdk import PlaneClientWrapper
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Plane Workspaces")

@mcp.tool(description="List all workspaces")
async def list_workspaces() -> dict:
    """List all teamspaces (workspaces)."""
    client = PlaneClientWrapper(
        base_url=os.getenv("PLANE_BASE_URL"),
        api_key=os.getenv("PLANE_API_KEY"),
    )

    teamspaces = client.teamspaces.list()

    return {
        "count": teamspaces.count,
        "workspaces": [
            {
                "id": ts.id,
                "name": ts.name,
                "description": ts.description,
                "icon": ts.icon_prop
            }
            for ts in teamspaces.results
        ]
    }

@mcp.tool(description="Create a new workspace")
async def create_workspace(
    name: str,
    description: str | None = None,
) -> dict:
    """Create a new teamspace (workspace)."""
    from plane.models.teamspaces import CreateTeamspace

    client = PlaneClientWrapper(
        base_url=os.getenv("PLANE_BASE_URL"),
        api_key=os.getenv("PLANE_API_KEY"),
    )

    data = CreateTeamspace(
        name=name,
        description=description
    )

    workspace = client.teamspaces.create(
        workspace_slug="your-workspace-slug",
        data=data
    )

    return {
        "id": workspace.id,
        "name": workspace.name,
        "description": workspace.description
    }

@mcp.tool(description="Get workspace details")
async def get_workspace(teamspace_id: str) -> dict:
    """Get workspace details by ID."""
    client = PlaneClientWrapper(
        base_url=os.getenv("PLANE_BASE_URL"),
        api_key=os.getenv("PLANE_API_KEY"),
    )

    workspace = client.teamspaces.retrieve(
        workspace_slug="your-workspace-slug",
        teamspace_id=teamspace_id
    )

    return {
        "id": workspace.id,
        "name": workspace.name,
        "description": workspace.description
    }
```

---

## 🎯 Usage Scenarios

### 1. Multi-Workspace Application

```python
# List all workspaces for the authenticated user
workspaces = client.teamspaces.list()

for workspace in workspaces.results:
    # Get projects in each workspace
    projects = client.teamspaces.projects.list(
        workspace_slug=workspace.id
    )
```

### 2. Workspace Discovery

```python
# Find workspaces by name pattern
workspaces = client.teamspaces.list()
matching = [w for w in workspaces.results if "project" in w.name.lower()]
```

### 3. Admin Management

```python
# Create workspace for new team
workspace = client.teamspaces.create(
    workspace_slug="admin-workspace",
    data=CreateTeamspace(name="New Team Workspace")
)

# Get workspace details
workspace = client.teamspaces.retrieve(
    workspace_slug="admin-workspace",
    teamspace_id=workspace.id
)
```

---

## 📝 Important Notes

### Key Points

1. **Authentication Required**: Requires valid API key with appropriate permissions
2. **Filtering**: Can filter list by `workspace_slug`
3. **UUID Usage**: Uses `teamspace_id` (UUID) for retrieve/delete/update operations
4. **Projects Access**: Can list projects within a workspace using `teamspaces.projects.list()`
5. **Members**: Can list workspace members using `teamspaces.members.list()`

### Workspace vs Teamspace Terminology

The SDK uses "teamspace" terminology, but this refers to what is commonly called a "workspace":

- **SDK**: `teamspaces` API
- **Common**: "Workspaces"
- **Relationship**: 1:1 (teamspace = workspace)

### Feature Availability

Some workspace features may be limited in Community Edition:

- Workspace creation/deletion
- Advanced workspace settings
- Member management

---

## 🧪 Testing Status

| Test                 | Status        | Notes                         |
| -------------------- | ------------- | ----------------------------- |
| list_teamspaces()    | ⏳ Not tested | Requires proper credentials   |
| create_teamspace()   | ⏳ Not tested | Requires workspace_slug       |
| retrieve_teamspace() | ⏳ Not tested | Uses teamspace_id (UUID)      |
| update_teamspace()   | ⏳ Not tested | Partial updates supported     |
| delete_teamspace()   | ⏳ Not tested | Permanently deletes workspace |

---

## 🔗 Related Documentation

- [Projects API](workspace/projects/README.md) - Projects within workspaces
- [Work Items API](workspace/projects/WORK_ITEMS.md) - Work items within projects
- [UUID Management Guide](../planning/UUID_AND_DEPENDENCY_GUIDE.md)
- [SDK API Mapping](../planning/SDK_API_MAPPING.md)

---

## 📚 References

- **SDK Source**: `plane.api.teamspaces`
- **SDK Models**: `plane.models.teamspaces`
- **SDK File**: `plane/api/teamspaces.py`

---

**Last Updated**: 2026-04-14T01:50:00Z
**Document Version**: 0.1.0
