# Plane SDK Coverage Status

**Last Updated**: 2026-04-14
**SDK Version**: v0.2.8
**Status**: Active Development

---

## Coverage Summary

| Category             | MCP Tools  | CLI Commands | Notes                       |
| -------------------- | ---------- | ------------ | --------------------------- |
| Projects             | 4/8        | 4/8          | Pre-checks enabled          |
| Work Items           | 4/13       | 4/13         | Pre-checks enabled          |
| Labels               | 3/6        | 2/6          | Pre-checks enabled          |
| Cycles               | 0/10       | 0/10         | Requires `cycle_view` flag  |
| Modules              | 0/10       | 0/10         | Requires `module_view` flag |
| States               | 0/5        | 0/5          | -                           |
| Work Item Types      | 0/5        | 0/5          | -                           |
| Work Item Properties | 0/5        | 0/5          | -                           |
| Comments             | 0/5        | 0/5          | -                           |
| Attachments          | 0/4        | 0/4          | -                           |
| Links                | 0/5        | 0/5          | -                           |
| Work Logs            | 0/5        | 0/5          | -                           |
| Epics                | 0/2        | 0/2          | -                           |
| Intake               | 0/5        | 0/5          | -                           |
| Pages                | 0/4        | 0/4          | 404 on CE instance          |
| Customers            | 0/7        | 0/7          | -                           |
| Teamspaces           | 0/4        | 0/4          | -                           |
| Stickies             | 0/5        | 0/5          | -                           |
| Initiatives          | 0/5        | 0/5          | -                           |
| Users                | 0/3        | 0/3          | -                           |
| **TOTAL**            | **11/106** | **10/106**   | **~10%**                    |

---

## Features Implemented

### Error Handling ✅

- ConfigurationError - Missing/invalid API credentials
- HttpError - HTTP errors with status code-specific messages
- PlaneError - SDK-specific errors
- User-friendly error messages with context

### Pre-Checks ✅

- `project_exists()` - Verify project before operations
- `work_item_exists()` - Verify work item before update/delete
- `label_exists()` - Verify label before assignment
- Returns False gracefully for non-existent resources

### CLI Confirmation Flow ✅

- Global `--autoconfirm` / `-y` flag for scripting
- Per-command `--yes` flag for delete operations
- Interactive prompts for destructive operations
- Confirmation can be overridden by global flag

### Type Safety ✅

- Full type annotations with mypy
- No unnecessary `# type: ignore` comments
- Uses `NoReturn` for error handlers
- Clean typing for SDK incompatibilities

---

## Implemented Resources

### Projects ✅

| Method                | MCP Tool         | CLI Command                | Status |
| --------------------- | ---------------- | -------------------------- | ------ |
| `list`                | `project_list`   | `plane-rex project list`   | ✅     |
| `create`              | `project_create` | `plane-rex project create` | ✅     |
| `retrieve`            | `project_info`   | `plane-rex project info`   | ✅     |
| `delete`              | `project_delete` | `plane-rex project delete` | ✅     |
| `update`              | -                | -                          | ❌     |
| `get_members`         | -                | -                          | ❌     |
| `get_features`        | -                | -                          | ❌     |
| `get_worklog_summary` | -                | -                          | ❌     |

### Work Items ⚠️ (40%)

| Method            | MCP Tool      | CLI Command             | Status |
| ----------------- | ------------- | ----------------------- | ------ |
| `list`            | `work_list`   | `plane-rex work list`   | ✅     |
| `create`          | `work_add`    | `plane-rex work add`    | ✅     |
| `retrieve`        | -             | -                       | ❌     |
| `update`          | `work_update` | `plane-rex work update` | ✅     |
| `delete`          | `work_delete` | `plane-rex work delete` | ✅     |
| `search`          | -             | -                       | ❌     |
| `advanced_search` | -             | -                       | ❌     |
| `comments.*`      | -             | -                       | ❌     |
| `attachments.*`   | -             | -                       | ❌     |
| `links.*`         | -             | -                       | ❌     |
| `relations.*`     | -             | -                       | ❌     |
| `activities.*`    | -             | -                       | ❌     |
| `work_logs.*`     | -             | -                       | ❌     |

### Labels ⚠️ (75%)

| Method                | MCP Tool       | CLI Command              | Status |
| --------------------- | -------------- | ------------------------ | ------ |
| `list`                | `label_list`   | `plane-rex label list`   | ✅     |
| `create`              | `label_create` | `plane-rex label create` | ✅     |
| `retrieve`            | -              | -                        | ❌     |
| `update`              | -              | -                        | ❌     |
| `delete`              | -              | -                        | ❌     |
| `assign to work item` | `label_assign` | -                        | ✅     |

---

## Not Yet Implemented

### Cycles (0/10)

- `list`, `create`, `retrieve`, `update`, `delete`
- `list_archived`, `archive`, `unarchive`
- `add_work_items`, `remove_work_item`, `list_work_items`, `transfer_work_items`

### Modules (0/8)

- `list`, `create`, `retrieve`, `update`, `delete`
- `list_archived`, `archive`, `unarchive`
- `add_work_items`, `remove_work_item`, `list_work_items`

### States (0/5)

- `list`, `create`, `retrieve`, `update`, `delete`

### Work Item Types (0/5)

- `list`, `create`, `retrieve`, `update`, `delete`

### Work Item Properties (0/5)

- `list`, `create`, `retrieve`, `update`, `delete`

### Epics (0/2)

- `list`, `retrieve`

### Intake (0/5)

- `list`, `create`, `retrieve`, `update`, `delete`

### Pages (0/4)

- `list_workspace_pages`, `list_project_pages`
- `retrieve_workspace_page`, `retrieve_project_page`

### Customers (0/7)

- `list`, `create`, `retrieve`, `update`, `delete`
- `properties.*`, `requests.*`

### Teamspaces (0/4)

- `list`, `retrieve`, `get_members`

### Stickies (0/5)

- `list`, `create`, `retrieve`, `update`, `delete`

### Initiatives (0/5)

- `list`, `create`, `retrieve`, `update`, `delete`

### Users (0/3)

- `get_me`, `retrieve`, `list`

---

## Known Limitations

### CE Instance Limitations

| Resource   | Issue                                        | Status |
| ---------- | -------------------------------------------- | ------ |
| Cycles     | Requires `cycle_view: true` flag on project  | ⚠️     |
| Modules    | Requires `module_view: true` flag on project | ⚠️     |
| Pages      | Returns 404 on CE Docker instance            | ❌     |
| Workspaces | Returns 404 on CE instance                   | ❌     |

### SDK Version Notes

- SDK v0.2.8 uses `workspace_slug` not `workspace_id`
- Pagination uses `PaginatedQueryParams` with `per_page` field
- Pydantic v2: use `.model_dump()` not `.to_dict()`
- SDK has incomplete type stubs (use `# type: ignore` where necessary)

---

## Implementation Priority

### Phase 1 (Current)

- ✅ Projects CRUD
- ✅ Work Items CRUD
- ✅ Labels (partial)

### Phase 2 (Next)

- ⏳ States CRUD
- ⏳ Work Item retrieval
- ⏳ Label update/delete
- ⏳ Better error handling with pre-checks

### Phase 3 (Future)

- ⏳ Cycles (when flag enabled)
- ⏳ Modules (when flag enabled)
- ⏳ Work Item sub-resources (comments, attachments, etc.)

---

**Last Updated**: 2026-04-14

---

## Test Suite

### Unit Tests (7 tests)

- Location: `tests/test_server.py`
- No API calls required
- Tests Settings, client initialization, MCP instance

### Integration Tests (22 tests)

- Location: `tests/test_integration.py`
- Uses real API credentials from environment
- Tests pre-checks, CRUD operations, error handling

### Running Tests

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/test_server.py -v

# Integration tests only
pytest tests/test_integration.py -v

# With coverage
pytest tests/ -v --cov=src/plane_mcp
```

### Test Categories

| Category       | Tests | Description                               |
| -------------- | ----- | ----------------------------------------- |
| Pre-Checks     | 6     | Verify existence functions work correctly |
| Projects       | 6     | List, create, retrieve, delete            |
| Work Items     | 6     | Create, update, delete, existence         |
| Labels         | 4     | Create, list, existence                   |
| Error Handling | 3     | Invalid IDs, graceful failures            |

---

## Recently Added (2026-04-14)

### Stickies ✅ (100%)

Full CRUD for workspace-level sticky notes

| Method     | MCP Tool        | CLI Command                    |
| ---------- | --------------- | ------------------------------ |
| `list`     | `sticky_list`   | `plane-rex sticky list`        |
| `create`   | `sticky_create` | `plane-rex sticky create`      |
| `retrieve` | `sticky_info`   | `plane-rex sticky info <id>`   |
| `update`   | `sticky_update` | `plane-rex sticky update <id>` |
| `delete`   | `sticky_delete` | `plane-rex sticky delete <id>` |

### States ✅ (100%)

Full CRUD for project states/workflow

| Method     | MCP Tool       | CLI Command                                |
| ---------- | -------------- | ------------------------------------------ |
| `list`     | `state_list`   | `plane-rex state list -p <project>`        |
| `create`   | `state_create` | `plane-rex state create -p <project>`      |
| `retrieve` | `state_info`   | `plane-rex state info <id> -p <project>`   |
| `update`   | `state_update` | `plane-rex state update <id> -p <project>` |
| `delete`   | `state_delete` | `plane-rex state delete <id> -p <project>` |

### View Commands ✅

Added detailed view commands for all resources

| Resource  | CLI Command                              |
| --------- | ---------------------------------------- |
| Work Item | `plane-rex work info <id> -p <project>`  |
| Label     | `plane-rex label info <id> -p <project>` |
| Sticky    | `plane-rex sticky info <id>`             |
| State     | `plane-rex state info <id> -p <project>` |

### User Worklist ✅

List work items assigned to current user across all projects

| Command                   | Description                     |
| ------------------------- | ------------------------------- |
| `plane-rex work my-tasks` | List work items assigned to you |

### CLI Performance ✅

- Lazy SDK imports - only load when commands execute
- `--help` loads in ~1.1s (down from 2.5s)
- Commands show "Fetching..." message immediately
- SDK import (~1.8s) happens during command execution
