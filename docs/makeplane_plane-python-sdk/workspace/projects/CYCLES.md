# Cycles API Documentation

**Document Version**: 1.0.0
**Created**: 2026-04-13T23:57:00Z
**Last Updated**: 2026-04-14T00:32:00Z
**Owner**: AI Assistant
**Status**: Active
**Version**: 1.0.0

---

## 📋 Overview

Cycles are **project-level** resources that represent time-based planning periods (sprints, iterations, months, quarters).

**API Endpoint**: `/workspaces/{workspace_slug}/projects/{project_id}/cycles`
**Level**: Project
**Feature Flag**: `cycle_view: true`
**SDK Version**: plane-python-sdk
**API Instance**: https://your-plane-instance/ (Community Edition)
**Last Tested**: 2026-04-13T23:55:00Z

---

## ⚠️ Availability Status

**Status**: ⚠️ **COMMUNITY EDITION LIMITED**

- ✅ SDK API fully implemented (13 methods)
- ⚠️ Returns HTTP 400 on create (validation needed)
- ⚠️ May require `cycle_view: true` on project
- ⚠️ Requires additional fields on create

---

## 🎯 API Methods

### 1. Create Cycle

**Endpoint**: `cycles.create()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `data: CreateCycle`

**Required Fields**:

- `name` (str) - Cycle name
- `owned_by` (str) - Owner ID
- `project_id` (str) - Project ID

```python
from plane.models.cycles import CreateCycle

data = CreateCycle(
    name="Test Cycle",
    owned_by=project_uuid,
    project_id=project_uuid
)

cycle = client.cycles.create(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    data=data
)
```

**Returns**: `Cycle`

**Test Result**: ⚠️ HTTP 400 (Bad Request) - Needs validation

---

### 2. List Cycles

**Endpoint**: `cycles.list()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `params: dict`

```python
cycles = client.cycles.list(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d"
)
print(f"Found {cycles.total_count} cycles")
```

**Returns**: `PaginatedCycleResponse`

**Test Result**: ✅ SUCCESS - Returns empty list

---

### 3. Retrieve Cycle

**Endpoint**: `cycles.retrieve()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `cycle_id` (UUID)

```python
cycle = client.cycles.retrieve(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    cycle_id="cycle-uuid-here"
)
```

**Returns**: `Cycle`

**Test Result**: ⚠️ Not tested (no cycles exist)

---

### 4. Update Cycle

**Endpoint**: `cycles.update()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `cycle_id`, `data: UpdateCycle`

```python
from plane.models.cycles import UpdateCycle

data = UpdateCycle(
    name="Updated Cycle"
)

cycle = client.cycles.update(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    cycle_id="cycle-uuid-here",
    data=data
)
```

**Returns**: `Cycle`

**Test Result**: ⚠️ Not tested

---

### 5. Delete Cycle

**Endpoint**: `cycles.delete()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `cycle_id` (UUID)

```python
client.cycles.delete(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    cycle_id="cycle-uuid-here"
)
```

**Returns**: `None`

**Test Result**: ⚠️ Not tested

---

### 6. List Archived Cycles

**Endpoint**: `cycles.list_archived()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `params: dict`

```python
archived_cycles = client.cycles.list_archived(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d"
)
```

**Returns**: `PaginatedArchivedCycleResponse`

**Test Result**: ⚠️ Not tested

---

### 7. Add Work Items to Cycle

**Endpoint**: `cycles.add_work_items()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `cycle_id`, `issue_ids: list[str]`

```python
# Add work items to cycle
client.cycles.add_work_items(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    cycle_id="cycle-uuid-here",
    issue_ids=["issue-uuid-1", "issue-uuid-2"]
)
```

**Returns**: `None`

**Test Result**: ⚠️ Not tested

---

### 8. Remove Work Item from Cycle

**Endpoint**: `cycles.remove_work_item()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `cycle_id`, `work_item_id` (UUID)

```python
# Remove work item from cycle
client.cycles.remove_work_item(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    cycle_id="cycle-uuid-here",
    work_item_id="issue-uuid-here"
)
```

**Returns**: `None`

**Test Result**: ⚠️ Not tested

---

### 9. List Work Items in Cycle

**Endpoint**: `cycles.list_work_items()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `cycle_id`, `params: dict`

```python
work_items = client.cycles.list_work_items(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    cycle_id="cycle-uuid-here"
)
```

**Returns**: `PaginatedCycleWorkItemResponse`

**Test Result**: ⚠️ Not tested

---

### 10. Transfer Work Items

**Endpoint**: `cycles.transfer_work_items()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `cycle_id`, `data: TransferCycleWorkItemsRequest`

```python
from plane.models.cycles import TransferCycleWorkItemsRequest

data = TransferCycleWorkItemsRequest(
    target_cycle_id="target-cycle-uuid"
)

client.cycles.transfer_work_items(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    cycle_id="cycle-uuid-here",
    data=data
)
```

**Returns**: `None`

**Test Result**: ⚠️ Not tested

---

### 11. Archive Cycle

**Endpoint**: `cycles.archive()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `cycle_id` (UUID)

```python
# Archive cycle
result = client.cycles.archive(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    cycle_id="cycle-uuid-here"
)
print(f"Archived: {result}")
```

**Returns**: `bool`

**Test Result**: ⚠️ Not tested

---

### 12. Unarchive Cycle

**Endpoint**: `cycles.unarchive()`
**Level**: Project
**Parameters**: `workspace_slug`, `project_id`, `cycle_id` (UUID)

```python
# Unarchive cycle
result = client.cycles.unarchive(
    workspace_slug="your-workspace-slug",
    project_id="3adb93b5-6a0c-4783-862e-5f2d7b17783d",
    cycle_id="cycle-uuid-here"
)
print(f"Unarchived: {result}")
```

**Returns**: `bool`

**Test Result**: ⚠️ Not tested

---

## 📊 Cycle Data Structure

### Core Fields

| Field        | Type     | Description             | Example                                |
| ------------ | -------- | ----------------------- | -------------------------------------- |
| `id`         | UUID     | Unique cycle identifier | `d5e1f425-973b-4655-a678-acf06c50a7ad` |
| `name`       | str      | Cycle name              | `"Q1 2024"`                            |
| `owned_by`   | str      | Owner UUID              | `user-uuid-here`                       |
| `project`    | UUID     | Parent project ID       | `3adb93b5-...`                         |
| `workspace`  | UUID     | Parent workspace ID     | `4ef343ce-...`                         |
| `created_at` | datetime | Creation timestamp      | `2026-04-13T...`                       |
| `updated_at` | datetime | Update timestamp        | `2026-04-13T...`                       |
| `deleted_at` | datetime | Deletion timestamp      | `None`                                 |

---

## 🔧 MCP Tool Implementation Example

```python
from fastmcp import FastMCP
from plane.models.cycles import CreateCycle, UpdateCycle

mcp = FastMCP("Plane Cycles")

@mcp.tool(description="Create a new cycle")
async def create_cycle(
    workspace_id: str,
    project_id: str,
    name: str,
    owner_id: str
) -> dict:
    """Create a new cycle."""
    data = CreateCycle(name=name, owned_by=owner_id, project_id=project_id)
    cycle = client.cycles.create(
        workspace_slug=workspace_id,
        project_id=project_id,
        data=data
    )
    return {
        "id": cycle.id,
        "name": cycle.name
    }

@mcp.tool(description="List cycles in project")
async def list_cycles(
    workspace_id: str,
    project_id: str
) -> list[dict]:
    """List all cycles in project."""
    cycles = client.cycles.list(
        workspace_slug=workspace_id,
        project_id=project_id
    )
    return [c.model_dump() for c in cycles.results]

@mcp.tool(description="Add work items to cycle")
async def add_work_items_to_cycle(
    workspace_id: str,
    project_id: str,
    cycle_id: str,
    work_item_ids: list[str]
) -> dict:
    """Add work items to a cycle."""
    client.cycles.add_work_items(
        workspace_slug=workspace_id,
        project_id=project_id,
        cycle_id=cycle_id,
        issue_ids=work_item_ids
    )
    return {"status": "added"}

@mcp.tool(description="List work items in cycle")
async def list_work_items_in_cycle(
    workspace_id: str,
    project_id: str,
    cycle_id: str
) -> list[dict]:
    """List work items in cycle."""
    work_items = client.cycles.list_work_items(
        workspace_slug=workspace_id,
        project_id=project_id,
        cycle_id=cycle_id
    )
    return [w.model_dump() for w in work_items.results]
```

---

## 🧪 Test Results

### Test Date: 2026-04-13T23:55:00Z

| Test           | Status        | Notes                         |
| -------------- | ------------- | ----------------------------- |
| list_cycles()  | ✅ SUCCESS    | Returns empty list            |
| create_cycle() | ⚠️ PARTIAL    | Returns HTTP 400 (validation) |
| Other methods  | ⏳ NOT TESTED | No cycles exist to test       |

---

## 📝 Important Notes

### Key Points

1. **Feature Flag**: Requires `cycle_view: true` on project
2. **Minimal Creation**: Requires `name`, `owned_by`, `project_id`
3. **Work Item Integration**: Full work item lifecycle management
4. **Archive Support**: Archive/unarchive cycles
5. **CE Limitation**: May be Community Edition limited

### UUID Management Pattern

```python
# 1. List cycles to get UUID
cycles = client.cycles.list(
    workspace_slug=workspace_slug,
    project_id=project_id
)

# 2. Create cycle (needs name, owned_by, project_id)
data = CreateCycle(
    name="Q1 2024",
    owned_by=owner_uuid,
    project_id=project_id
)
cycle = client.cycles.create(
    workspace_slug=workspace_slug,
    project_id=project_id,
    data=data
)

# 3. Use UUID for modify operations
client.cycles.update(
    workspace_slug=workspace_slug,
    project_id=project_id,
    cycle_id=cycle.id,
    data=data
)
```

---

## 🔗 Related Documentation

- [Projects](README.md) - Parent resource with feature flags
- [Modules](MODULES.md) - Similar project-level organization
- [Work Items](work_items/README.md) - Work items can be assigned to cycles
- [Investigation Strategy](../planning/INVESTIGATION_STRATEGY.md)
- [Project Features Investigation](../../SESSION_SUMMARY.md)

---

## 📚 References

- **SDK Source**: `plane.api.cycles` (installed package)
- **SDK Models**: `plane.models.cycles` (installed package)
- **Test Script**: `/tmp/test_cycles_discovery.py`

---

**Last Updated**: 2026-04-14T00:32:00Z
**Document Version**: 1.0.0
