# UUID Management and Dependency Guide

**Created**: 2026-04-13T18:57:00Z
**Last Updated**: 2026-04-13T19:10:00Z
**Owner**: AI Assistant
**Status**: Active
**Version**: 1.0.0

---

## 🎯 Overview

When building MCP tools for Plane, we need to understand **dependency chains** and **UUID management**. Many operations require specific identifiers that must be looked up from previous operations or user input.

---

## 🔑 UUID Management Strategy

### Two Types of Identifiers

| Type           | Example                                | When to Use                          | How to Get                    |
| -------------- | -------------------------------------- | ------------------------------------ | ----------------------------- |
| **Identifier** | `TEST1`, `PLANEMCPSE`, `PROJ-123`      | User-friendly, display, search       | User input, API responses     |
| **UUID**       | `85daba3a-2882-44dc-b5d6-04eae907b7a3` | API calls (retrieve, update, delete) | List responses, API responses |

### UUID Lookup Patterns

#### Pattern 1: List → Get UUID → Modify

```python
# Step 1: List projects to get UUID
projects = client.projects.list(workspace_slug="your-workspace-slug")
projects[0].id  # This is the UUID!

# Step 2: Use UUID for modify operations
project = client.projects.retrieve(
    workspace_slug="your-workspace-slug",
    project_id=projects[0].id  # UUID, not identifier!
)
```

#### Pattern 2: Search → Get UUID → Modify

```python
# Step 1: Search work items
results = client.work_items.search(
    workspace_slug="your-workspace-slug",
    query="bug"
)

# Step 2: Extract UUID from results
work_item_id = results[0].id

# Step 3: Update using UUID
client.work_items.update(
    workspace_slug="your-workspace-slug",
    project_id=results[0].project_id,
    work_item_id=work_item_id,
    data={"state": "done"}
)
```

#### Pattern 3: Identifier → Lookup → UUID

```python
# Some APIs allow lookup by identifier
work_item = client.work_items.retrieve_by_identifier(
    workspace_slug="your-workspace-slug",
    project_identifier="TESTI",  # Identifier, not UUID
    issue_identifier=123  # Sequence number
)
```

---

## 📋 Dependency Chains for Each Operation Type

### 1. Project Operations

| Operation          | Required Info                           | How to Get    | Dependencies        |
| ------------------ | --------------------------------------- | ------------- | ------------------- |
| **list_projects**  | workspace_slug                          | Config        | None                |
| **get_project**    | workspace_slug, project_id (UUID)       | list_projects | ✅ Needs list first |
| **create_project** | workspace_slug, name, identifier        | Config        | None                |
| **update_project** | workspace_slug, project_id (UUID), data | list_projects | ✅ Needs list first |
| **delete_project** | workspace_slug, project_id (UUID)       | list_projects | ✅ Needs list first |

**Example Workflow:**

```python
# User wants to update a project
1. List projects to find the one to update
2. Get UUID from list response
3. Update project with UUID
```

### 2. Work Item (Issue) Operations

| Operation         | Required Info                                      | How to Get                   | Dependencies               |
| ----------------- | -------------------------------------------------- | ---------------------------- | -------------------------- |
| **search_issues** | workspace_slug, query                              | Config                       | None                       |
| **list_issues**   | workspace_slug, project_id (UUID)                  | list_projects                | ✅ Needs list first        |
| **get_issue**     | workspace_slug, project_id (UUID), issue_id (UUID) | search_issues OR list_issues | ✅ Needs search/list first |
| **update_issue**  | workspace_slug, project_id (UUID), issue_id (UUID) | search_issues OR list_issues | ✅ Needs search/list first |
| **delete_issue**  | workspace_slug, project_id (UUID), issue_id (UUID) | search_issues OR list_issues | ✅ Needs search/list first |

**Example Workflow:**

```python
# User wants to update an issue
1. Search for issue by query
2. Get issue UUID from search results
3. Update issue with UUID
```

### 3. Label Operations

| Operation        | Required Info                               | How to Get    | Dependencies        |
| ---------------- | ------------------------------------------- | ------------- | ------------------- |
| **list_labels**  | workspace_slug, project_id (UUID)           | list_projects | ✅ Needs list first |
| **get_label**    | workspace_slug, project_id (UUID), label_id | list_labels   | ✅ Needs list first |
| **create_label** | workspace_slug, project_id (UUID), data     | list_projects | ✅ Needs list first |

### 4. State Operations

| Operation              | Required Info                                             | How to Get                   | Dependencies               |
| ---------------------- | --------------------------------------------------------- | ---------------------------- | -------------------------- |
| **list_states**        | workspace_slug, project_id (UUID)                         | list_projects                | ✅ Needs list first        |
| **get_state**          | workspace_slug, project_id (UUID), state_id               | list_states                  | ✅ Needs list first        |
| **update_issue_state** | workspace_slug, project_id (UUID), issue_id (UUID), state | search_issues OR list_issues | ✅ Needs search/list first |

### 5. Cycle Operations

| Operation        | Required Info                               | How to Get    | Dependencies        |
| ---------------- | ------------------------------------------- | ------------- | ------------------- |
| **list_cycles**  | workspace_slug, project_id (UUID)           | list_projects | ✅ Needs list first |
| **get_cycle**    | workspace_slug, project_id (UUID), cycle_id | list_cycles   | ✅ Needs list first |
| **create_cycle** | workspace_slug, project_id (UUID), data     | list_projects | ✅ Needs list first |

### 6. Module Operations

| Operation         | Required Info                                | How to Get    | Dependencies        |
| ----------------- | -------------------------------------------- | ------------- | ------------------- |
| **list_modules**  | workspace_slug, project_id (UUID)            | list_projects | ✅ Needs list first |
| **get_module**    | workspace_slug, project_id (UUID), module_id | list_modules  | ✅ Needs list first |
| **create_module** | workspace_slug, project_id (UUID), data      | list_projects | ✅ Needs list first |

---

## 🔄 User Interaction Patterns

### Pattern 1: Search → Update

```
User: "Find all bugs and mark them as done"
1. Search issues with query="bug"
2. For each result, update state to "done"
Dependencies: search_issues → update_issue_state
```

### Pattern 2: List → Get Details

```
User: "Show me all projects in workspace"
1. List projects
2. For each project, get details
Dependencies: list_projects → get_project
```

### Pattern 3: Create → Retrieve

```
User: "Create a new project called 'Alpha'"
1. Create project with name="Alpha"
2. Get newly created project details
Dependencies: create_project → get_project
```

### Pattern 4: Navigate Hierarchy

```
User: "Show me all issues in the first project"
1. List projects
2. Get UUID of first project
3. List issues in that project
Dependencies: list_projects → list_issues
```

---

## 💾 Data Collection Strategy

### What to Cache/Store

| Data Type      | When to Cache       | Why                           | How Long           |
| -------------- | ------------------- | ----------------------------- | ------------------ |
| **Projects**   | After list_projects | Used for many operations      | Until session ends |
| **Work Items** | After search/list   | Used for updates/deletes      | Until session ends |
| **Labels**     | After list_labels   | Used for filtering            | Until session ends |
| **States**     | After list_states   | Used for state changes        | Until session ends |
| **Cycles**     | After list_cycles   | Used for work item management | Until session ends |

### Cache Structure

```python
# Session cache
session_data = {
    "workspace_slug": "your-workspace-slug",
    "projects": [
        {
            "name": "Project A",
            "id": "uuid-123",  # UUID for API calls
            "identifier": "PROJ-A",  # For display
            "issues": []  # Can cache issues too
        }
    ],
    "labels": {
        "uuid-123": ["Bug", "Feature"],
        "uuid-456": ["High Priority"]
    },
    "states": {
        "uuid-123": ["Backlog", "Todo", "Done"]
    }
}
```

---

## 🛠️ Tool Implementation Strategy

### Tool Design Principles

1. **Minimize UUID Handling in User Interface**
    - Users don't need to know UUIDs
    - Tools should hide complexity
    - Use identifiers in prompts

2. **Chain Operations Automatically**
    - `list_projects` → `get_project`
    - `search_issues` → `update_issue`
    - Don't make users do manual lookups

3. **Provide Clear Error Messages**
    - "Project not found" vs "404 error"
    - "Issue not found" vs "work_item not retrieved"

### Example: Enhanced search_issues Tool

```python
@mcp.tool(description="Search for issues and return details")
async def search_issues(
    workspace_id: str,
    project_id: str,
    query: str,
    limit: int = 20
) -> dict:
    """
    Search for issues and return full details.

    Args:
        workspace_id: Workspace slug (e.g., "your-workspace-slug")
        project_id: Project identifier or UUID
        query: Search query text
        limit: Maximum results to return

    Returns:
        List of issues with full details
    """
    # Step 1: Ensure project_id is UUID
    project_id = await ensure_project_uuid(
        workspace_id=workspace_id,
        project_id=project_id
    )

    # Step 2: Search for issues
    results = client.search_work_items(
        workspace_slug=workspace_id,
        project_id=project_id,
        query=query,
        limit=limit
    )

    # Step 3: Cache results for potential updates
    cache_results(results, workspace_id, project_id)

    return {
        "results": results,
        "count": len(results),
        "query": query
    }
```

---

## ⚠️ Error Handling Strategy

### Common Errors and Solutions

| Error              | Cause                     | Solution                             |
| ------------------ | ------------------------- | ------------------------------------ |
| **404 Not Found**  | UUID doesn't exist        | Verify UUID from list response       |
| **404 Not Found**  | Wrong endpoint            | Use correct API endpoint             |
| **409 Conflict**   | Identifier already exists | Generate unique identifier           |
| **TypeError**      | Wrong parameter name      | Use workspace_slug, not workspace_id |
| **AttributeError** | Method doesn't exist      | Use alternative approach             |

### UUID Validation

```python
def validate_uuid(uuid_string: str) -> bool:
    """Validate UUID format."""
    import re
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(pattern, uuid_string.lower()))

def ensure_project_uuid(
    workspace_slug: str,
    project_id: str
) -> str:
    """Ensure project_id is UUID, lookup if identifier."""
    if not validate_uuid(project_id):
        # Try to find project by identifier
        projects = client.projects.list(workspace_slug=workspace_slug)
        for proj in projects:
            if proj.identifier == project_id:
                return proj.id
        # If not found, raise error
        raise ValueError(f"Project '{project_id}' not found")
    return project_id
```

---

## 📊 Information Collection Checklist

### Before Any Operation

- [ ] **Workspace Slug**: Collected from config or user input
- [ ] **Project UUID**: Collected from list_projects or user input
- [ ] **Work Item UUID**: Collected from search_issues or list_issues
- [ ] **Labels**: Available from list_labels
- [ ] **States**: Available from list_states
- [ ] **User Permissions**: Verify API key has access

### For Each Tool

- [ ] **Inputs**: What does user need to provide?
- [ ] **Dependencies**: What prior operations are needed?
- [ ] **Cache**: What data should be cached for next operations?
- [ ] **Error Handling**: What errors can occur and how to handle?
- [ ] **Validation**: What inputs need validation?

---

## 🎯 Next Steps

### Phase 1: Basic Tools

1. ✅ list_projects (working)
2. ✅ search_issues (working)
3. 🔄 get_project (needs UUID from list)
4. 🔄 list_issues (needs project UUID)

### Phase 2: Enhanced Tools

1. get_issue (needs issue UUID from search/list)
2. update_issue_state (needs issue UUID + state)
3. list_labels (needs project UUID)
4. list_states (needs project UUID)

### Phase 3: Advanced Tools

1. update_issue (needs issue UUID + update data)
2. delete_issue (needs issue UUID)
3. get_cycle (needs project UUID + cycle UUID)
4. list_modules (needs project UUID)

---

**This guide provides the foundation for building tools that properly manage UUID dependencies and data flow.**
