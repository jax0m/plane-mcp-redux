# Pages API Documentation

**Document Version**: 1.0.0
**Created**: 2026-04-13T23:57:00Z
**Last Updated**: 2026-04-13T23:58:00Z
**Owner**: AI Assistant
**Status**: Active
**Version**: 1.0.0

---

## 📋 Overview

Pages are **workspace/project-level** resources that provide visual dashboards for project overview and tracking.

**API Endpoint**: `/workspaces/{workspace_slug}/pages` or `/workspaces/{workspace_slug}/projects/{project_id}/pages`
**Level**: Workspace / Project
**Feature Flag**: `page_view: true`
**SDK Version**: plane-python-sdk
**API Instance**: https://your-plane-instance/ (Community Edition)
**Last Tested**: 2026-04-13T23:58:00Z

---

## ❌ Availability Status

**Status**: ❌ **COMMUNITY EDITION LIMITED**

- ✅ SDK API available (4 methods)
- ❌ Returns HTTP 404 on all endpoints
- ❌ Not available on Community Edition
- ⚠️ Requires Pro subscription

---

## 🎯 API Methods

### 1. Create Workspace Page

**Endpoint**: `pages.create_workspace_page()`
**Level**: Workspace
**Parameters**: `workspace_slug`, `data: CreatePage`

```python
from plane.models.pages import CreatePage

data = CreatePage(
    name="Test Workspace Page",
    description_html="<p>Test description</p>"
)

page = client.pages.create_workspace_page(
    workspace_slug="your-workspace-slug",
    data=data
)
```

**Returns**: `Page`

**Test Result**: ❌ HTTP 404 (Not Found) - CE Limited

---

### 2. Create Project Page

**Endpoint**: `pages.create_project_page()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `data: CreatePage`

```python
from plane.models.pages import CreatePage

data = CreatePage(
    name="Test Project Page",
    description_html="<p>Test description</p>"
)

page = client.pages.create_project_page(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    data=data
)
```

**Returns**: `Page`

**Test Result**: ❌ HTTP 404 (Not Found) - CE Limited

---

### 3. Retrieve Workspace Page

**Endpoint**: `pages.retrieve_workspace_page()`
**Level**: Workspace
**Parameters**: `workspace_slug`, `page_id` (UUID), `params: dict`

```python
page = client.pages.retrieve_workspace_page(
    workspace_slug="your-workspace-slug",
    page_id="page-uuid-here",
    params={"expand": "work_items"}
)
```

**Returns**: `Page`

**Test Result**: ❌ Not available (CE limited)

---

### 4. Retrieve Project Page

**Endpoint**: `pages.retrieve_project_page()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `page_id` (UUID), `params: dict`

```python
page = client.pages.retrieve_project_page(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    page_id="page-uuid-here",
    params={"expand": "work_items"}
)
```

**Returns**: `Page`

**Test Result**: ❌ Not available (CE limited)

---

## 📊 Page Data Structure

### Core Fields

| Field               | Type     | Description                         | Example                                |
| ------------------- | -------- | ----------------------------------- | -------------------------------------- |
| `id`                | UUID     | Unique page identifier              | `d5e1f425-973b-4655-a678-acf06c50a7ad` |
| `name`              | str      | Page name                           | `"Q1 Dashboard"`                       |
| `description_html`  | str      | HTML description                    | `"<p>Quarter 1 overview</p>"`          |
| `description_plain` | str      | Plain text description              | `"Quarter 1 overview"`                 |
| `type`              | str      | Page type                           | `"workspace"` or `"project"`           |
| `workspace`         | UUID     | Parent workspace ID                 | `4ef343ce-...`                         |
| `project`           | UUID     | Parent project ID (if project page) | `3adb93b5-...`                         |
| `created_at`        | datetime | Creation timestamp                  | `2026-04-13T...`                       |
| `updated_at`        | datetime | Update timestamp                    | `2026-04-13T...`                       |

---

## 🔧 MCP Tool Implementation Example

```python
from fastmcp import FastMCP
from plane.models.pages import CreatePage

mcp = FastMCP("Plane Pages")

@mcp.tool(description="Create a workspace page")
async def create_workspace_page(
    workspace_id: str,
    name: str,
    description: str
) -> dict:
    """Create a workspace-level page."""
    data = CreatePage(
        name=name,
        description_html=f"<p>{description}</p>"
    )
    page = client.pages.create_workspace_page(
        workspace_slug=workspace_id,
        data=data
    )
    return {
        "id": page.id,
        "name": page.name
    }

@mcp.tool(description="Create a project page")
async def create_project_page(
    workspace_id: str,
    project_id: str,
    name: str,
    description: str
) -> dict:
    """Create a project-level page."""
    data = CreatePage(
        name=name,
        description_html=f"<p>{description}</p>"
    )
    page = client.pages.create_project_page(
        workspace_slug=workspace_id,
        project_id=project_id,
        data=data
    )
    return {
        "id": page.id,
        "name": page.name
    }
```

---

## 🧪 Test Results

### Test Date: 2026-04-13T23:58:00Z

| Test                    | Status | Notes               |
| ----------------------- | ------ | ------------------- |
| create_workspace_page() | ❌ 404 | Not available on CE |
| create_project_page()   | ❌ 404 | Not available on CE |
| retrieve methods        | ❌ 404 | Not available on CE |

---

## 📝 Important Notes

### Key Points

1. **Community Edition Limited**: Pages API is **not available** on Community Edition
2. **HTTP 404**: All endpoints return 404 errors
3. **Pro Subscription Required**: Need Plane Pro to use Pages feature
4. **SDK Available**: SDK methods exist but backend API is disabled on CE
5. **Feature Flag**: Requires `page_view: true` on project (not checked due to 404)

### Error Pattern

- **404 Not Found**: Feature not available on Community Edition

### UUID Management Pattern

```python
# Create a project page (only works on Pro)
data = CreatePage(
    name="Dashboard",
    description_html="<p>Project dashboard</p>"
)
page = client.pages.create_project_page(
    workspace_slug=workspace_slug,
    project_id=project_id,
    data=data
)

# Retrieve the page
page = client.pages.retrieve_project_page(
    workspace_slug=workspace_slug,
    project_id=project_id,
    page_id=page.id
)
```

---

## 🔗 Related Documentation

- [Projects](README.md) - Parent resource with feature flags
- [Cycles](CYCLES.md) - Similar project-level feature (also CE limited)
- [Work Items](work_items/README.md) - Pages can show work items
- [Investigation Strategy](../../../.pi/plans/INVESTIGATION_STRATEGY.md)
- [Project Features Investigation](../../SESSION_SUMMARY.md)

---

## 📚 References

- **SDK Source**: `plane.api.pages`
- **SDK Models**: `plane.models.pages`
- **Test Script**: `/tmp/test_pages_final.py`
- **API Instance**: https://your-plane-instance/ (Community Edition)

---

**Last Updated**: 2026-04-13T23:58:00Z
**Document Version**: 1.0.0
