# Session Startup Checklist

**Created**: 2026-04-13T23:00:0Z
**Last Updated**: 2026-04-14
**Owner**: AI Assistant
**Status**: Active
**Version**: 2.0.0

---

## 📋 Session Startup

### 1. Read Context Files

- [ ] Read `AGENTS.md` - Project overview and patterns
- [ ] Read `.pi/plans/DEVELOPMENT_PLAN.md` - Main roadmap
- [ ] Read `IMPLEMENTATION_SUMMARY.md` - Latest session summary
- [ ] Read `docs/SDK_COVERAGE.md` - SDK coverage tracking
- [ ] Read `docs/makeplane_plane-python-sdk/INDEX.md` - SDK documentation

### 2. Verify Environment

```bash
# Check CLI is available
which plane-rex
plane-rex --help

# Check API credentials (do not share these!)
grep PLANE_BASE_URL .env
grep PLANE_API_KEY .env
grep PLANE_WORKSPACE_SLUG .env
```

### 3. Review Recent Changes

```bash
# Check git status
git status --short

# Review recent commits
git log --oneline -10

# Run tests
pytest tests/ -v

# Type check
mypy src/plane_mcp/ tests/

# Lint
ruff check src/plane_mcp/ tests/
```

### 4. Understand Current Focus

**Current Status**: Phase 2 complete - Stickies, States, View commands, User worklist implemented

**Next Priority**:

1. Add MCP tools for stickies and states
2. GitHub Actions CI workflow
3. Label update/delete CLI commands

---

## 🎯 Key Context

### Project Details

- **Project**: `plane-mcp-redux`
- **CLI**: `plane-rex`
- **Module**: `plane_mcp`
- **SDK**: plane-python-sdk v0.2.8
- **FastMCP**: v3.x

### SDK Patterns

- Use `workspace_slug` not `workspace_id`
- Use `work_items` not `issues`
- Use `.model_dump()` not `.to_dict()`
- `CreateProject` requires `identifier` field
- Lazy SDK imports for performance

### Implemented Commands

```bash
# Projects
plane-rex project list
plane-rex project create "Name" -i IDENTIFIER
plane-rex project info <id>
plane-rex project delete <id>

# Work Items
plane-rex work list -p <project>
plane-rex work add "Title" -p <project>
plane-rex work info <id> -p <project>
plane-rex work update <id> -p <project> -n "New"
plane-rex work delete <id> -p <project>
plane-rex work my-tasks  # Assigned to you

# Labels
plane-rex label list -p <project>
plane-rex label create "Name" -p <project>
plane-rex label info <id> -p <project>

# Stickies (workspace-level)
plane-rex sticky list
plane-rex sticky create "Content"
plane-rex sticky info <id>
plane-rex sticky update <id> --content "New"
plane-rex sticky delete <id>

# States
plane-rex state list -p <project>
plane-rex state create "Name" -p <project>
plane-rex state info <id> -p <project>
plane-rex state update <id> -p <project> --name "New"
plane-rex state delete <id> -p <project>
```

---

## 🔗 Related Documentation

- [AGENTS.md](../AGENTS.md) - Project overview
- [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) - Main roadmap
- [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md) - Latest session
- [SDK_COVERAGE.md](../docs/SDK_COVERAGE.md) - Coverage tracking
- [INDEX.md](../docs/makeplane_plane-python-sdk/INDEX.md) - SDK docs

---

**Last Updated**: 2026-04-14
**Document Version**: 2.0.0
