# Plane MCP Redux - Development Plan

## Current Status

### ✅ Completed

- [x] Project structure and Python packaging
- [x] FastMCP 3.x server with lazy loading
- [x] Plane SDK v0.2.8 client wrapper
- [x] 30 focused tools (72% reduction from original 109)
- [x] Full type safety (mypy, ty checking - all passing)
- [x] Pre-commit hooks configured
- [x] Pi context setup
- [x] All tests passing (7/7)

### 🔴 Pending

- [ ] Live testing with real Plane API credentials
- [ ] Test all 30 tools in real-world scenarios
- [ ] Error handling verification
- [ ] Performance testing

---

## Next Steps

### 1. Live API Testing

```bash
# Setup
cp .env .env.local
# Edit .env.local with your actual credentials
PLANE_BASE_URL=https://your-plane-instance.com
PLANE_API_KEY=your_api_key
PLANE_WORKSPACE_SLUG=your_workspace

# Run server
plane-rex
```

### 2. Basic Iteration

**Focus Areas**:

- SDK API mismatches (workspace_slug vs workspace_id)
- Pagination handling
- Field name differences
- Error handling
- Rate limiting

---

## Testing Strategy

### Unit Tests

- Location: `tests/`
- Coverage: All client methods, tool handlers
- Target: 80%+ coverage

### Integration Tests

- Location: `tests/integration/`
- Requires: `.env.test.local`
- Scope: End-to-end tool execution

---

## GitFlow Strategy

### Branch Naming

```
main               # Production-ready code
develop            # Integration branch
feature/name       # New features
bugfix/name        # Bug fixes
release/1.0.0      # Release prep
hotfix/name        # Critical fixes
```

### Commit Convention

```bash
feat: new feature
fix: bug fix
docs: documentation
test: add/modify tests
refactor: code refactoring
chore: maintenance
```

---

## SDK-Specific Notes

### Key Patterns

```python
import plane
from plane.models.projects import CreateProject

client = plane.PlaneClient(base_url, api_key)

# List (paginated)
projects = client.projects.list(workspace_slug="slug")
print(projects.count)
print(projects.results)

# Create (requires model)
data = CreateProject(
    name="Project",
    identifier="PROJ-123"  # Required!
)
project = client.projects.create(workspace_slug="slug", data=data)
```

### Common Issues

- SDK uses `workspace_slug`, not `workspace_id`
- `project_id` is UUID, not identifier
- Use `.model_dump()` not `.to_dict()` (Pydantic v2)
- SDK has incomplete type stubs (use type ignores)

---

## Session Continuity

**Key files to reference:**

1. `AGENTS.md` - Project overview
2. `.pi/plans/DEVELOPMENT_PLAN.md` - This file
3. `docs/makeplane_plane-python-sdk/INDEX.md` - SDK documentation

---

## Quick Reference

```bash
# Run server
plane-rex

# Test
pytest tests/ -v

# Type check
ty check src/plane_mcp/
mypy src/plane_mcp/

# Lint/format
ruff check --fix src/ tests/
ruff format src/ tests/
```

---

**Last Updated**: 2026-04-13T20:20:00Z
**Document Version**: 1.0.0
