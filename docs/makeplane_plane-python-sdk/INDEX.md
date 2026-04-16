# Plane Python SDK Documentation Index

**Created**: 2026-04-13T19:50:00Z
**Last Updated**: 2026-04-14
**Owner**: AI Assistant
**Status**: Active
**Version**: 2.0.0

---

## 📁 Documentation Structure

```
docs/
├── SDK_COVERAGE.md                           # SDK coverage tracking ⭐
├── makeplane_plane-python-sdk/
│   ├── INDEX.md                              # This file
│   ├── CLI_COMPLETE.md                       # CLI guide (legacy)
│   ├── CRUD_MINIMUM_FIELDS.md                # Required fields reference
│   ├── planning/
│   │   ├── SDK_API_MAPPING.md                # SDK method inventory
│   │   ├── UUID_AND_DEPENDENCY_GUIDE.md      # UUID management
│   │   └── INVESTIGATION_STRATEGY.md         # Investigation approach
│   └── workspace/
│       ├── STICKIES.md                       # Stickies API ✅
│       └── projects/
│           ├── README.md                     # Projects API
│           ├── CYCLES.md                     # Cycles API
│           ├── MODULES.md                    # Modules API
│           ├── LABELS.md                     # Labels API
│           ├── PAGES.md                      # Pages API
│           └── WORK_ITEMS.md                 # Work Items API
```

---

## 📚 Resource Documentation

### Workspace-Level

| Resource | Status     | Documentation                        |
| -------- | ---------- | ------------------------------------ |
| Stickies | ✅ Working | [STICKIES.md](workspace/STICKIES.md) |

### Project-Level

| Resource   | Status           | Documentation                                              |
| ---------- | ---------------- | ---------------------------------------------------------- |
| Projects   | ✅ Working       | [projects/README.md](workspace/projects/README.md)         |
| Labels     | ✅ Working       | [projects/LABELS.md](workspace/projects/LABELS.md)         |
| Work Items | ✅ Working       | [projects/WORK_ITEMS.md](workspace/projects/WORK_ITEMS.md) |
| States     | ✅ Working       | See SDK_COVERAGE.md                                        |
| Modules    | ⚠️ Flag Required | [projects/MODULES.md](workspace/projects/MODULES.md)       |
| Cycles     | ⚠️ Flag Required | [projects/CYCLES.md](workspace/projects/CYCLES.md)         |
| Pages      | ⚠️ Docker Config | [projects/PAGES.md](workspace/projects/PAGES.md)           |

---

## 🎯 CLI Commands (Current)

**Status**: ✅ 22 Commands Implemented

| Command Group | Commands                                  | Status      |
| ------------- | ----------------------------------------- | ----------- |
| Project       | list, create, info, delete                | ✅ Complete |
| Work          | list, add, info, update, delete, my-tasks | ✅ Complete |
| Label         | list, create, info                        | ✅ Partial  |
| Sticky        | list, create, info, update, delete        | ✅ Complete |
| State         | list, create, info, update, delete        | ✅ Complete |

**Quick Start**:

```bash
# List projects
plane-rex project list

# See your assigned tasks
plane-rex work my-tasks

# Create sticky note
plane-rex sticky create "Remember this!"

# List states in project
plane-rex state list -p <project-id>
```

---

## 🔗 Related Documentation

### Primary

- [SDK_COVERAGE.md](../SDK_COVERAGE.md) - **Start here** - Coverage tracking ⭐
- [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md) - Latest session summary
- [README.md](../README.md) - Project README

### SDK Reference

- [CRUD_MINIMUM_FIELDS.md](CRUD_MINIMUM_FIELDS.md) - Required fields reference
- [planning/SDK_API_MAPPING.md](planning/SDK_API_MAPPING.md) - SDK methods
- [planning/UUID_AND_DEPENDENCY_GUIDE.md](planning/UUID_AND_DEPENDENCY_GUIDE.md) - UUID management

### Legacy (For Reference)

- [CLI_COMPLETE.md](CLI_COMPLETE.md) - Original CLI guide
- [FASTMCP_WORKFLOW_DESIGN.md](FASTMCP_WORKFLOW_DESIGN.md) - Original design

---

## 📊 API Availability

| Resource   | SDK | CLI | MCP | Notes                       |
| ---------- | --- | --- | --- | --------------------------- |
| Projects   | ✅  | ✅  | ✅  | Full CRUD                   |
| Work Items | ✅  | ✅  | ✅  | + my-tasks                  |
| Labels     | ✅  | ⚠️  | ✅  | Missing update/delete CLI   |
| Stickies   | ✅  | ✅  | ❌  | Full CLI, no MCP            |
| States     | ✅  | ✅  | ❌  | Full CLI, no MCP            |
| Modules    | ⚠️  | ❌  | ❌  | Requires `module_view` flag |
| Cycles     | ⚠️  | ❌  | ❌  | Requires `cycle_view` flag  |
| Pages      | ❌  | ❌  | ❌  | 404 on CE instance          |

---

## 🚀 Quick Links

- **Start Here**: [SDK_COVERAGE.md](../SDK_COVERAGE.md)
- **Latest Changes**: [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md)
- **Project Overview**: [README.md](../README.md)
- **SDK Details**: [planning/SDK_API_MAPPING.md](planning/SDK_API_MAPPING.md)

---

**Last Updated**: 2026-04-14
**Document Version**: 2.0.0
