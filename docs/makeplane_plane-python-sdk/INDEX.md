# Plane Python SDK Documentation Index

**Created**: 2026-04-13T19:50:00Z
**Last Updated**: 2026-04-14T04:00:00Z
**Owner**: AI Assistant
**Status**: Active
**Version**: 1.1.0

---

## 📁 Documentation Structure

```
docs/makeplane_plane-python-sdk/
├── INDEX.md                                      # This file
├── CLI_COMPLETE.md                               # Complete CLI guide ⭐
├── CRUD_MINIMUM_FIELDS.md                        # Required fields reference
├── FASTMCP_IMPLEMENTATION_PLAN.md                # Implementation plan
├── FASTMCP_WORKFLOW_DESIGN.md                    # Workflow design
├── DEPRECATION_NOTES.md                          # Deprecated docs
├── planning/
│   ├── SDK_API_MAPPING.md                        # SDK method inventory
│   ├── UUID_AND_DEPENDENCY_GUIDE.md              # UUID management
│   └── INVESTIGATION_STRATEGY.md                 # Investigation approach
└── workspace/
    ├── projects/
    │   ├── README.md                             # Projects API
    │   ├── CYCLES.md                             # Cycles API
    │   ├── MODULES.md                            # Modules API
    │   ├── LABELS.md                             # Labels API
    │   └── WORK_ITEMS.md                         # Work Items API
    └── work_items/
        └── README.md
```

---

## 📚 Resource Documentation

### Workspace-Level

| Resource | Status     | Documentation                        |
| -------- | ---------- | ------------------------------------ |
| Stickies | ✅ Working | [STICKIES.md](workspace/STICKIES.md) |

### Project-Level

| Resource   | Status     | Documentation                                              |
| ---------- | ---------- | ---------------------------------------------------------- |
| Projects   | ✅ Working | [projects/README.md](workspace/projects/README.md)         |
| Labels     | ✅ Working | [projects/LABELS.md](workspace/projects/LABELS.md)         |
| Modules    | ✅ Working | [projects/MODULES.md](workspace/projects/MODULES.md)       |
| Work Items | ✅ Working | [projects/WORK_ITEMS.md](workspace/projects/WORK_ITEMS.md) |

### Project Features

| Resource | Status           | Documentation                                      |
| -------- | ---------------- | -------------------------------------------------- |
| Cycles   | ⚠️ CE Limited    | [projects/CYCLES.md](workspace/projects/CYCLES.md) |
| Pages    | ⚠️ Docker Config | [projects/PAGES.md](workspace/projects/PAGES.md)   |

---

## 🎯 CLI Commands (Complete)

**Status**: ✅ Production Ready

| Command Group | Commands                   | Status     |
| ------------- | -------------------------- | ---------- |
| Project       | list, create, info, delete | ✅ Working |
| Work          | add, list, update, delete  | ✅ Working |
| Label         | create, list               | ✅ Working |

**Quick Start**:

```bash
# List projects
plane-rex project list

# Add work item
plane-rex work add "Task" -p proj-id

# Create label
plane-rex label create "Bug" -p proj-id
```

**Documentation**: [CLI_COMPLETE.md](CLI_COMPLETE.md)

---

## 🔗 Related Documentation

- [CLI_COMPLETE.md](CLI_COMPLETE.md) - Complete CLI guide ⭐
- [CRUD_MINIMUM_FIELDS.md](CRUD_MINIMUM_FIELDS.md) - Required fields reference
- [FASTMCP_WORKFLOW_DESIGN.md](FASTMCP_WORKFLOW_DESIGN.md) - Workflow design
- [FASTMCP_IMPLEMENTATION_PLAN.md](FASTMCP_IMPLEMENTATION_PLAN.md) - Implementation plan
- [planning/SDK_API_MAPPING.md](planning/SDK_API_MAPPING.md) - SDK methods
- [planning/UUID_AND_DEPENDENCY_GUIDE.md](planning/UUID_AND_DEPENDENCY_GUIDE.md) - UUID management
- [planning/INVESTIGATION_STRATEGY.md](planning/INVESTIGATION_STRATEGY.md) - Investigation approach

---

## 📊 API Availability

| Resource   | Status           | Notes                        |
| ---------- | ---------------- | ---------------------------- |
| Projects   | ✅ Working       | All CRUD operations          |
| Work Items | ✅ Working       | Minimal fields (name only)   |
| Labels     | ✅ Working       | All CRUD operations          |
| Modules    | ⚠️ Flag Required | Requires `module_view: true` |
| Cycles     | ⚠️ CE Limited    | Requires `cycle_view: true`  |
| Pages      | ⚠️ Docker Config | 404 on CE instance           |
| Workspaces | ❌ Not Available | HTTP 404 on CE               |

---

## 🚀 Quick Links

- **Start Here**: [CLI_COMPLETE.md](CLI_COMPLETE.md)
- **API Reference**: [CRUD_MINIMUM_FIELDS.md](CRUD_MINIMUM_FIELDS.md)
- **SDK Details**: [planning/SDK_API_MAPPING.md](planning/SDK_API_MAPPING.md)
- **Workflow**: [FASTMCP_WORKFLOW_DESIGN.md](FASTMCP_WORKFLOW_DESIGN.md)

---

**Last Updated**: 2026-04-14T04:00:00Z
**Document Version**: 1.1.0
