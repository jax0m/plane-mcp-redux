# Plane SDK API Mapping & Guide

**Created**: 2026-04-13T20:15:00Z
**Last Updated**: 2026-04-13T20:18:00Z
**Owner**: AI Assistant
**Status**: Active
**Version**: 1.1.0
**Based On**: SDK_API_MAPPING.md + SDK_AND_CLI_GUIDE.md (Merged)

---

## 📋 Complete API Method Inventory

### WORKSPACES / TEAMSPACES

| Method                       | Parameters                                | Purpose                    |
| ---------------------------- | ----------------------------------------- | -------------------------- |
| `teamspaces.create()`        | `workspace_slug`, `data: CreateTeamspace` | Create new workspace       |
| `teamspaces.retrieve()`      | `workspace_slug`, `teamspace_id`          | Get workspace by ID        |
| `teamspaces.update()`        | `workspace_slug`, `teamspace_id`, `data`  | Update workspace           |
| `teamspaces.delete()`        | `workspace_slug`, `teamspace_id`          | Delete workspace           |
| `teamspaces.list()`          | `workspace_slug`                          | List workspaces            |
| `teamspaces.projects.list()` | `workspace_slug`                          | List projects in workspace |
| `teamspaces.members.list()`  | `workspace_slug`                          | List workspace members     |

**Key Insight**: Uses `teamspace_id` for retrieve, not `workspace_slug`

---

### PROJECTS

| Method                           | Parameters                                            | Purpose              |
| -------------------------------- | ----------------------------------------------------- | -------------------- |
| `projects.create()`              | `workspace_slug`, `data: CreateProject`               | Create project       |
| `projects.retrieve()`            | `workspace_slug`, `project_id` (UUID)                 | Get project          |
| `projects.update()`              | `workspace_slug`, `project_id`, `data: UpdateProject` | Update project       |
| `projects.delete()`              | `workspace_slug`, `project_id` (UUID)                 | Delete project       |
| `projects.list()`                | `workspace_slug`, `params: PaginatedQueryParams`      | List projects        |
| `projects.get_worklog_summary()` | `workspace_slug`, `project_id`                        | Get worklog stats    |
| `projects.get_members()`         | `workspace_slug`, `project_id`                        | List project members |
| `projects.get_features()`        | `workspace_slug`, `project_id`                        | Get project features |
| `projects.update_features()`     | `workspace_slug`, `project_id`, `data`                | Update features      |

**Key Insights**:

- `project_id` is UUID, not identifier
- Uses `PaginatedQueryParams(per_page=N)` for pagination
- Has additional methods for members, features, worklogs

---

### WORK ITEMS

| Method                         | Parameters                                             | Purpose           |
| ------------------------------ | ------------------------------------------------------ | ----------------- |
| `work_items.create()`          | `workspace_slug`, `project_id`, `data: CreateWorkItem` | Create work item  |
| `work_items.retrieve()`        | `workspace_slug`, `project_id`, `work_item_id`         | Get work item     |
| `work_items.update()`          | `workspace_slug`, `project_id`, `work_item_id`, `data` | Update work item  |
| `work_items.delete()`          | `workspace_slug`, `project_id`, `work_item_id`         | Delete work item  |
| `work_items.list()`            | `workspace_slug`, `project_id`, `params`               | List work items   |
| `work_items.search()`          | `workspace_slug`, `query`, `params`                    | Search work items |
| `work_items.advanced_search()` | `workspace_slug`, `data: AdvancedSearchWorkItem`       | Advanced search   |

**Key Insights**:

- `work_item_id` can be identifier (e.g., "TESTI") or UUID
- Uses `WorkItemQueryParams` for filters
- Has sub-resources: `comments`, `activities`, `work_logs`, `relations`, `links`, `attachments`

---

### MEMBERS / USERS

| Method             | Parameters                                      | Purpose       |
| ------------------ | ----------------------------------------------- | ------------- |
| `users.create()`   | `workspace_slug`, `data: CreateUser`            | Create member |
| `users.retrieve()` | `workspace_slug`, `user_id`                     | Get member    |
| `users.update()`   | `workspace_slug`, `user_id`, `data: UpdateUser` | Update member |
| `users.delete()`   | `workspace_slug`, `user_id`                     | Delete member |
| `users.list()`     | `workspace_slug`, `params`                      | List members  |

---

### STATES

| Method              | Parameters                                          | Purpose      |
| ------------------- | --------------------------------------------------- | ------------ |
| `states.create()`   | `workspace_slug`, `project_id`, `data: CreateState` | Create state |
| `states.retrieve()` | `workspace_slug`, `project_id`, `state_id`          | Get state    |
| `states.update()`   | `workspace_slug`, `project_id`, `state_id`, `data`  | Update state |
| `states.delete()`   | `workspace_slug`, `project_id`, `state_id`          | Delete state |
| `states.list()`     | `workspace_slug`, `project_id`, `params`            | List states  |

---

### LABELS

| Method              | Parameters                                          | Purpose      |
| ------------------- | --------------------------------------------------- | ------------ |
| `labels.create()`   | `workspace_slug`, `project_id`, `data: CreateLabel` | Create label |
| `labels.retrieve()` | `workspace_slug`, `project_id`, `label_id`          | Get label    |
| `labels.update()`   | `workspace_slug`, `project_id`, `label_id`, `data`  | Update label |
| `labels.delete()`   | `workspace_slug`, `project_id`, `label_id`          | Delete label |
| `labels.list()`     | `workspace_slug`, `project_id`, `params`            | List labels  |

---

## 🛠️ SDK Source Code Reference

**Location**: `plane.`

### SDK Import Patterns

```python
import plane
from plane import PlaneClient

# Initialize
client = PlaneClient(
    base_url="https://api.plane.so",
    api_key="your-api-key"
)

# Use sub-resources
client.projects.list(...)
client.work_items.list(...)
client.users.list(...)
client.cycles.list(...)
```

### Important SDK Patterns

#### 1. Paginated Responses

```python
projects = client.projects.list(workspace_slug="my-workspace")
print(projects.count)      # Total count
print(projects.results)    # List of Project objects
print(projects.total_pages) # Pagination info
```

#### 2. Pydantic Models Required

```python
# ❌ Don't use dicts for create/update
data = {"name": "Project"}  # ❌ Fails

# ✅ Use Pydantic models
from plane.models.projects import CreateProject
data = CreateProject(name="Project", identifier="PROJ-1")  # ✅ Works
```

#### 3. Identifier vs UUID

```python
# Identifier: Human-readable (e.g., "PROJ-123", "TESTI")
project.identifier  # "TESTI"

# UUID: Internal ID (e.g., "85daba3a-2882-44dc-b5d6-04eae907b7a3")
project.id  # UUID string

# API calls use UUID for retrieve/delete/update
client.projects.retrieve(workspace_slug="...", project_id="UUID")  # ✅
client.projects.retrieve(workspace_slug="...", project_id="TESTI")  # ❌
```

---

## 🔧 Fixing SDK Issues

### Issue 1: Create Project Returns 409 Conflict

**Possible Causes**:

- Identifier already exists
- Workspace has identifier restrictions
- API rate limiting
- Permission issue

**Solutions to Try**:

1. Use unique identifiers: `f"TEST-{timestamp}"`
2. Try different identifier formats:
    - `TEST1` ✅
    - `TEST-1` ❌
    - `TEST123` ❌
3. Check workspace settings for identifier rules

### Issue 2: Retrieve Returns 404

**Root Cause**: SDK expects UUID, not identifier

**Fix**:

```python
# ❌ Wrong - uses identifier
project = client.projects.retrieve(
    workspace_slug="your-workspace-slug",
    project_id="TESTI"  # Identifier
)

# ✅ Correct - uses UUID
projects = client.projects.list(workspace_slug="your-workspace-slug")
project = projects.results[0]  # Get first project
uuid = project.id  # Extract UUID

project = client.projects.retrieve(
    workspace_slug="your-workspace-slug",
    project_id=uuid  # Use UUID
)
```

### Issue 3: Work Items List Returns 404

**Possible Causes**:

- Project has no work items
- API endpoint format issue
- Permission restriction

**Solution**:

```python
# Try with specific filters
work_items = client.work_items.list(
    workspace_slug="your-workspace-slug",
    project_id="project-uuid",
    params=WorkItemQueryParams(state="todo-state-uuid")
)

# Try search instead
results = client.work_items.search(
    workspace_slug="your-workspace-slug",
    query="bug"
)
```

---

## 🛠️ FastMCP CLI Capabilities

**Location**: `/workspaces/fastmcp/`

FastMCP provides several CLI tools for development and testing:

### 1. Inspector - Test MCP Server Locally

```bash
# Run server with inspector UI
fastmcp dev inspector src/plane_mcp/server.py

# With custom port
fastmcp dev inspector --ui-port 3000 --server-port 8000 src/plane_mcp/server.py

# With additional packages
fastmcp dev inspector --with fastmcp-cli src/plane_mcp/server.py
```

**Features**:

- Interactive MCP testing UI
- Real-time tool invocation
- No MCP client needed

### 2. Run - Test as MCP Server

```bash
# Run as stdio transport (MCP client connection)
fastmcp run src/plane_mcp/server.py

# Run as HTTP transport (browser-based)
fastmcp run --transport http src/plane_mcp/server.py

# Run with specific host/port
fastmcp run --host 0.0.0.0 --port 8000 src/plane_mcp/server.py
```

**Use Cases**:

- Test server locally before MCP client integration
- Debug tool definitions
- Verify lazy loading works

### 3. Generate CLI Commands

```bash
# Generate CLI command for a FastMCP server
fastmcp generate src/plane_mcp/server.py --output cli_commands.py
```

### 4. MCP Client Commands

```bash
# List available tools
fastmcp call list-tools

# Call a specific tool
fastmcp call list-workspaces --workspace my-workspace

# Call with arguments
fastmcp call list-projects --workspace my-workspace --limit 10
```

---

## 🎯 Testing Strategy

### Phase 1: Local Testing with FastMCP CLI

```bash
# 1. Run server with inspector
cd /workspaces/plane-mcp-redux
fastmcp dev inspector src/plane_mcp/server.py

# 2. Test tools interactively through UI
# - List workspaces
# - List projects
# - Create issue
# - Update state
```

### Phase 2: MCP Client Testing

```bash
# 3. Test with MCP client (VS Code, Claude Desktop, etc.)
# Configure client to connect to your server
# Test tools through MCP interface
```

### Phase 3: Script Testing

```bash
# 4. Create test scripts
python /tmp/test_plane_connection.py

# 5. Test with environment variables
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)
fastmcp run src/plane_mcp/server.py
```

---

## 📝 Quick Reference

### Environment Variables

```bash
# .env file
PLANE_BASE_URL=your-plane-instance.com
PLANE_API_KEY=your-api-key-here
PLANE_WORKSPACE_SLUG=your-workspace-slug

# Load in script
from dotenv import load_dotenv
load_dotenv()
```

---

## 🚀 Next Steps

1. ✅ **Use FastMCP CLI for testing** - `fastmcp dev inspector src/plane_mcp/server.py`
2. 🔍 **Investigate create() 409 error** - Check API documentation
3. 🔍 **Test retrieve() with UUID** - Extract from list response
4. 🧪 **Test work items API** - Try different projects
5. 📚 **Study SDK source** - `plane.plane/`

---

## 📖 Additional Resources

- **SDK Docs**: `plane.README.md`
- **FastMCP Docs**: `/workspaces/fastmcp/docs/`
- **Examples**: `/workspaces/fastmcp/examples/`
- **SDK Examples**: `plane.examples/`

---

**Last Updated**: 2026-04-13T20:18:00Z
**Document Version**: 1.1.0
