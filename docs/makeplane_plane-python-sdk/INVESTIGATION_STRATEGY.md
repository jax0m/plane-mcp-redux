# Investigation Strategy for Plane Resources

**Created**: 2026-04-13T23:40:00Z
**Last Updated**: 2026-04-13T23:40:00Z
**Owner**: AI Assistant
**Status**: Active
**Version**: 1.0.0

---

## 🎯 Overview

This document captures the investigation strategy used for exploring Plane SDK resources. This approach can be applied to any new resource or feature testing.

---

## 📋 Investigation Workflow

### Phase 1: Discovery (What Exists)

**Goal**: Understand what resources exist and their basic structure.

**Steps**:

1. List all resources
2. Check for required parameters
3. Capture raw API responses
4. Identify feature flags

**Example - Modules**:

```python
# 1. List modules
modules = client.modules.list(
    workspace_slug=workspace_slug,
    project_id=project_uuid
)
print(f"Found {modules.total_count} modules")

# 2. Capture raw data
for module in modules.results:
    print(json.dumps(module.model_dump(), indent=2))
```

**Key Findings**:

- ✅ List endpoint exists and works
- ✅ Returns paginated results
- ✅ Module has status tracking (backlog, started, completed)

---

### Phase 2: CRUD Operations (Basic Functionality)

**Goal**: Verify create, read, update, delete operations.

**Steps**:

1. Test create with minimal fields
2. Test retrieve by ID
3. Test update with minimal fields
4. Test delete
5. Check error responses

**Example - Modules**:

```python
# 1. Create with minimal fields
module = client.modules.create(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    data={'name': 'Test Module'}
)
print(f"Created: {module.id}")

# 2. Retrieve
module = client.modules.retrieve(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    module_id=module.id
)

# 3. Update
module = client.modules.update(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    module_id=module.id,
    data={'name': 'Updated Module'}
)

# 4. Delete
client.modules.delete(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    module_id=module.id
)
```

**Key Findings**:

- ✅ All CRUD operations work
- ✅ Minimal fields: just `name` required

---

### Phase 3: Advanced Features (What Else?)

**Goal**: Discover advanced capabilities beyond basic CRUD.

**Steps**:

1. Check SDK source code for additional methods
2. Test methods that don't follow CRUD pattern
3. Look for relationship management
4. Test bulk operations

**Example - Modules**:

```python
# 1. Check SDK source
grep -r "module" plane/api/modules.py

# 2. Found special methods:
- add_work_items()
- list_work_items()
- remove_work_item()
- archive()
- unarchive()

# 3. Test add_work_items
client.modules.add_work_items(
    workspace_slug=workspace_slug,
    project_id=project_uuid,
    module_id=module_uuid,
    issue_ids=[work_item_id_1, work_item_id_2]
)

# 4. Verify in module status
modules = client.modules.list(
    workspace_slug=workspace_slug,
    project_id=project_uuid
)
print(f"Total Issues: {modules.results[0].total_issues}")
```

**Key Findings**:

- ✅ Modules track work items by status
- ✅ Work items added via separate endpoint (not field)
- ✅ Status: backlog, started, completed, unstarted, cancelled

---

### Phase 4: Dependencies & Requirements (What's Needed)

**Goal**: Understand prerequisites and dependencies.

**Steps**:

1. Check parent resource requirements
2. Check feature flags
3. Check permission requirements
4. Check SDK version requirements

**Example - Modules**:

```python
# 1. Check parent project
projects = client.projects.list(workspace_slug=workspace_slug)
for proj in projects.results:
    if hasattr(proj, 'module_view') and proj.module_view:
        print(f"Project {proj.name} has modules enabled")

# 2. Only test on projects with module_view=true
```

**Key Findings**:

- ✅ Requires `module_view: true` on parent project
- ✅ Not available on all projects
- ✅ Community Edition limitation check needed

---

### Phase 5: Edge Cases & Error Handling

**Goal**: Test failure modes and boundaries.

**Steps**:

1. Test with invalid IDs
2. Test missing required fields
3. Test permission errors
4. Test with empty results
5. Test with large datasets

**Example - Modules**:

```python
# 1. Invalid module ID
try:
    client.modules.retrieve(
        workspace_slug=workspace_slug,
        project_id=project_uuid,
        module_id="invalid-uuid"
    )
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

# 2. Empty results
modules = client.modules.list(
    workspace_slug=workspace_slug,
    project_id=project_uuid
)
print(f"Total: {modules.total_count}")
# Handle empty gracefully
```

**Key Findings**:

- ✅ 404 for invalid IDs
- ✅ Empty list returns pagination structure
- ✅ No special error handling needed

---

### Phase 6: FastMCP Integration (Tool Design)

**Goal**: Design FastMCP tools and CLI commands.

**Steps**:

1. Define tool signatures
2. Plan error handling
3. Design CLI commands
4. Plan pagination

**Example - Modules**:

```python
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
    return {"status": "added"}
```

---

## 🧪 Strategy Summary

### For Each Resource Type:

| Phase           | Goal             | Time   | Output            |
| --------------- | ---------------- | ------ | ----------------- |
| 1. Discovery    | What exists      | 5 min  | List of resources |
| 2. CRUD         | Basic ops        | 10 min | CRUD verification |
| 3. Advanced     | Special features | 15 min | Feature list      |
| 4. Dependencies | Requirements     | 5 min  | Prerequisites     |
| 5. Edge Cases   | Error handling   | 10 min | Error patterns    |
| 6. FastMCP      | Tool design      | 15 min | Tool signatures   |

**Total**: ~60 minutes per resource type

---

## 📝 Key Lessons Learned

### What Works Well:

1. **Start with list** - Understand what exists
2. **Test minimal create** - Know required fields
3. **Check SDK source** - Find non-CRUD methods
4. **Look for feature flags** - Understand requirements
5. **Capture raw JSON** - Document actual API response

### What to Watch For:

1. **Feature flags** - May need project configuration
2. **Separate endpoints** - Not all relationships are fields
3. **Community Edition** - Some features may be Pro-only
4. **Pagination** - Always use `total_count`
5. **Error handling** - 404 vs 400 vs other errors

---

## 🔗 Related Documentation

- [Resource Testing Plan](RESOURCE_TESTING_PLAN.md)
- [All Resources Reference](ALL_RESOURCES_REFERENCE.md)
- [Session Summary](SESSION_SUMMARY.md)
- [Implementation Roadmap](IMPLEMENTATION_ROADMAP.md)

---

**Last Updated**: 2026-04-13T23:40:00Z
**Document Version**: 1.0.0
