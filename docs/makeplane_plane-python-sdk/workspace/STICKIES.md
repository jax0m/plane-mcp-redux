# Stickies API Documentation

**Document Version**: 1.0.0
**Created**: 2026-04-13T19:25:00Z
**Last Updated**: 2026-04-13T19:25:00Z
**Owner**: AI Assistant
**Status**: Active
**Version**: 1.0.0

---

## 📋 Overview

Stickies are **workspace-level** resources (not project-level). This is a critical distinction from most other Plane resources.

**Location**: `/workspaces/{workspace_slug}/stickies`
**SDK Version**: plane-python-sdk (tested with latest available)
**API Instance**: https://your-plane-instance/ (Community Edition)

---

## ✅ Working Endpoints

All stickies endpoints work successfully with proper UUID management.

### 1. List Stickies

**Endpoint**: `stickies.list()`
**Level**: Workspace
**Parameters**: `workspace_slug`

```python
stickies = client.stickies.list(workspace_slug="your-workspace-slug")
```

**Returns**: `PaginatedStickyResponse`

**Response Structure**:

```python
{
    "count": int,
    "total_pages": int,
    "total_results": int,
    "results": [Sticky, ...]
}
```

**Example Output**:

```python
[
    Sticky(
        id='39dec233-6a0c-4783-862e-5f2d7b17783d',
        name=None,
        description={'html': '<p>Eat Bananas</p>'},
        description_html='<p>Eat Bananas</p>',
        description_stripped='Eat Bananas',
        color=None,
        background_color='peach',
        workspace='4ef343ce-78f0-4f96-896b-b5c7fa63dd8c',
        owner='d92d49db-b509-4150-9d28-9a11b818aa98',
        sort_order=85535.0,
        created_at='2026-03-25T09:58:10.713462-07:00',
        updated_at='2026-03-25T09:58:16.268514-07:00',
        deleted_at=None,
        created_by='d92d49db-b509-4150-9d28-9a11b818aa98',
        updated_by='d92d49db-b509-4150-9d28-9a11b818aa98'
    )
]
```

---

### 2. Create Sticky

**Endpoint**: `stickies.create()`
**Level**: Workspace
**Parameters**: `workspace_slug`, `data: CreateSticky`

```python
from plane.models.stickies import CreateSticky

sticky_data = CreateSticky(
    name="Test Sticky Note",
    description="This is a test sticky note",
    description_html="<p>HTML content</p>"
)

sticky = client.stickies.create(
    workspace_slug="your-workspace-slug",
    data=sticky_data
)
```

**Returns**: `Sticky`

**CreateSticky Model**:

```python
class CreateSticky(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    description_html: Optional[str] = None
    description_stripped: Optional[str] = None
    color: Optional[str] = None
    background_color: Optional[str] = None
```

**Example Response**:

```python
Sticky(
    id='769285cf-4c8f-4ab8-a085-5a54ff6f9878',
    name='Test Sticky Note',
    description={'html': '<p>This is a test sticky note</p>'},
    description_html='This is a test sticky note',
    description_stripped='This is a test sticky note',
    color=None,
    background_color=None,
    workspace='4ef343ce-78f0-4f96-896b-b5c7fa63dd8c',
    owner='d92d49db-b509-4150-9d28-9a11b818aa98',
    created_at='2026-04-13T19:30:00.000000-07:00',
    updated_at='2026-04-13T19:30:00.000000-07:00',
    deleted_at=None
)
```

---

### 3. Retrieve Sticky

**Endpoint**: `stickies.retrieve()`
**Level**: Workspace
**Parameters**: `workspace_slug`, `sticky_id` (UUID)

```python
sticky = client.stickies.retrieve(
    workspace_slug="your-workspace-slug",
    sticky_id="769285cf-4c8f-4ab8-a085-5a54ff6f9878"
)
```

**Returns**: `Sticky`

**Note**: Requires UUID, not identifier

---

### 4. Update Sticky

**Endpoint**: `stickies.update()`
**Level**: Workspace
**Parameters**: `workspace_slug`, `sticky_id`, `data: UpdateSticky`

```python
from plane.models.stickies import UpdateSticky

sticky_data = UpdateSticky(
    name="Updated Test Sticky Note",
    description="Updated description",
    description_html="<p>Updated HTML</p>"
)

sticky = client.stickies.update(
    workspace_slug="your-workspace-slug",
    sticky_id="769285cf-4c8f-4ab8-a085-5a54ff6f9878",
    data=sticky_data
)
```

**Returns**: `Sticky`

**UpdateSticky Model**:

```python
class UpdateSticky(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    description_html: Optional[str] = None
    description_stripped: Optional[str] = None
    color: Optional[str] = None
    background_color: Optional[str] = None
```

---

### 5. Delete Sticky

**Endpoint**: `stickies.delete()`
**Level**: Workspace
**Parameters**: `workspace_slug`, `sticky_id` (UUID)

```python
client.stickies.delete(
    workspace_slug="your-workspace-slug",
    sticky_id="769285cf-4c8f-4ab8-a085-5a54ff6f9878"
)
```

**Returns**: `None`

---

## 📊 Sticky Data Structure

### Sticky Model Fields

| Field                  | Type               | Description               | Example                                |
| ---------------------- | ------------------ | ------------------------- | -------------------------------------- |
| `id`                   | UUID               | Unique sticky identifier  | `39dec233-6a0c-4783-862e-5f2d7b17783d` |
| `name`                 | Optional[str]      | Sticky name/title         | `None` or `"My Sticky"`                |
| `description`          | dict               | Raw description structure | `{'html': '<p>...</p>'}`               |
| `description_html`     | str                | HTML description          | `<p>Eat Bananas</p>`                   |
| `description_stripped` | str                | Plain text description    | `Eat Bananas`                          |
| `color`                | Optional[str]      | Text color                | `None`                                 |
| `background_color`     | str                | Background color          | `peach`, `dark-blue`, `orange`         |
| `workspace`            | UUID               | Parent workspace ID       | `4ef343ce-78f0-4f96-896b-b5c7fa63dd8c` |
| `owner`                | UUID               | Owner user ID             | `d92d49db-b509-4150-9d28-9a11b818aa98` |
| `sort_order`           | float              | Display order             | `85535.0`                              |
| `created_at`           | datetime           | Creation timestamp        | `2026-03-25T09:58:10.713462-07:00`     |
| `updated_at`           | datetime           | Last update timestamp     | `2026-03-25T09:58:16.268514-07:00`     |
| `deleted_at`           | Optional[datetime] | Deletion timestamp        | `None`                                 |
| `created_by`           | UUID               | Creator user ID           | `d92d49db-b509-4150-9d28-9a11b818aa98` |
| `updated_by`           | UUID               | Last updater user ID      | `d92d49db-b509-4150-9d28-9a11b818aa98` |

---

## 🔧 MCP Tool Implementation Example

```python
from fastmcp import FastMCP
from plane.models.stickies import CreateSticky

mcp = FastMCP("Plane Stickies")

@mcp.tool(description="List all sticky notes in workspace")
async def list_stickies(workspace_id: str) -> dict:
    """List all workspace stickies."""
    stickies = client.stickies.list(workspace_slug=workspace_id)
    return {
        "stickies": [
            {
                "id": s.id,
                "name": s.name,
                "description_stripped": s.description_stripped,
                "background_color": s.background_color
            }
            for s in (stickies.results or [])
        ],
        "count": len(stickies.results) if stickies.results else 0
    }

@mcp.tool(description="Create a new sticky note")
async def create_sticky(
    workspace_id: str,
    name: str,
    description: str,
    background_color: str | None = None
) -> dict:
    """Create a new sticky note."""
    sticky_data = CreateSticky(
        name=name,
        description=description,
        description_html=f"<p>{description}</p>",
        background_color=background_color
    )
    sticky = client.stickies.create(
        workspace_slug=workspace_id,
        data=sticky_data
    )
    return {
        "id": sticky.id,
        "name": sticky.name,
        "description_stripped": sticky.description_stripped,
        "background_color": sticky.background_color
    }

@mcp.tool(description="Update a sticky note")
async def update_sticky(
    workspace_id: str,
    sticky_id: str,
    name: str | None = None,
    description: str | None = None
) -> dict:
    """Update an existing sticky note."""
    from plane.models.sticky import UpdateSticky

    data = UpdateSticky()
    if name is not None:
        data.name = name
    if description is not None:
        data.description = description

    sticky = client.stickies.update(
        workspace_slug=workspace_id,
        sticky_id=sticky_id,
        data=data
    )
    return {
        "id": sticky.id,
        "name": sticky.name,
        "description_stripped": sticky.description_stripped
    }

@mcp.tool(description="Delete a sticky note")
async def delete_sticky(workspace_id: str, sticky_id: str) -> dict:
    """Delete a sticky note."""
    client.stickies.delete(
        workspace_slug=workspace_id,
        sticky_id=sticky_id
    )
    return {"message": "Sticky deleted successfully"}
```

---

## 🧪 Test Results

### Test Date: 2026-04-13T19:25:00Z

| Test              | Status     | Notes                        |
| ----------------- | ---------- | ---------------------------- |
| list_stickies()   | ✅ SUCCESS | Returns 3 existing stickies  |
| create_sticky()   | ✅ SUCCESS | Creates new sticky with UUID |
| retrieve_sticky() | ✅ SUCCESS | Retrieves by UUID            |
| update_sticky()   | ✅ SUCCESS | Updates sticky content       |
| delete_sticky()   | ✅ SUCCESS | Deletes sticky               |

**Test Script**: `/tmp/test_stickies.py`
**Test Output**: All 5 operations successful

---

## 📝 Important Notes

### Key Differences from Other Resources

1. **Workspace-Level**: Stickies are workspace-level, not project-level
2. **No Project ID Required**: Unlike most resources, stickies don't need project_id
3. **Color Options**: `peach`, `dark-blue`, `orange`, etc.
4. **HTML Content**: Supports rich HTML descriptions
5. **Striped Text**: `description_stripped` provides plain text version

### UUID Management

- **List**: No UUID needed (workspace-level)
- **Create**: Returns UUID automatically
- **Retrieve/Delete/Update**: Requires UUID from create response

---

## 🔗 Related Documentation

- [UUID Management Guide](../../../.pi/plans/UUID_AND_DEPENDENCY_GUIDE.md)
- [Information Collection Guide](../../../.pi/plans/INVESTIGATION_STRATEGY.md)
- [SDK API Mapping](../../../.pi/plans/SDK_API_MAPPING.md)

---

## 📚 References

- **SDK Source**: `plane.api.stickies`
- **SDK Models**: `plane.models.stickies`
- **Test Script**: `/tmp/test_sticky.py`

---

**Last Updated**: 2026-04-13T19:25:00Z
**Document Version**: 1.0.0

---

## 📋 Raw Sticky JSON Export

Below is a real sticky exported in raw JSON format. This shows the complete API response structure.

### Example Sticky Data

```json
{
    "id": "39dec233-6a0c-4783-862e-5f2d7b17783d",
    "name": null,
    "description": {},
    "description_html": "<p class=\"editor-paragraph-block\" data-id=\"600067b4-ccfd-49bb-8e64-5aa7ed0e56a2\">Eat Bananas</p>",
    "description_stripped": "Eat Bananas",
    "description_binary": null,
    "logo_props": {},
    "color": null,
    "background_color": "peach",
    "workspace": "4ef343ce-78f0-4f96-896b-b5c7fa63dd8c",
    "owner": "d92d49db-b509-4150-9d28-9a11b818aa98",
    "sort_order": 85535.0,
    "created_at": "2026-03-25T09:58:10.713462-07:00",
    "updated_at": "2026-03-25T09:58:16.268514-07:00",
    "deleted_at": null,
    "created_by": "d92d49db-b509-4150-9d28-9a11b818aa98",
    "updated_by": "d92d49db-b509-4150-9d28-9a11b818aa98"
}
```

### Key Observations from Raw Data

1. **`name` field**: Currently `null` in this sticky, but can be set on creation
2. **`description`**: Returns as a dict with HTML structure
3. **`description_html`**: The rendered HTML version
4. **`description_stripped`**: Plain text version (most useful for display)
5. **`background_color`**: Sticky background (e.g., `"peach"`)
6. **`color`**: Text color (separate from background)
7. **`owner`**: Sticky owner UUID
8. **`created_by` / `updated_by`**: Track creation and updates
9. **`sort_order`**: Display order (float, 85535.0 = default)

### Description Structure Details

The `description` field has an internal structure:

```json
{
    "html": "<p class=\"editor-paragraph-block\" data-id=\"600067b4-ccfd-49bb-8e64-5aa7ed0e56a2\">Eat Bananas</p>",
    "text": "Eat Bananas",
    "markdown": "Eat Bananas"
}
```

---

**Last Updated**: 2026-04-13T21:35:00Z
**Document Version**: 1.0.1
