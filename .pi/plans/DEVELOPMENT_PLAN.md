# Plane MCP Redux - Development Plan

## Current Status (Session: Initial Setup)

### ✅ Completed

- [x] Project structure and Python packaging (`pyproject.toml`)
- [x] FastMCP 3.x server implementation with lazy loading
- [x] Plane SDK v0.2.8 client wrapper
- [x] 30 focused tools (72% reduction from original 109)
- [x] Full type safety (mypy, ty checking - all passing)
- [x] Pre-commit hooks configured and tested
- [x] Pi coding agent context setup (AGENTS.md, .pi/settings.json, prompts)
- [x] AI-DECLARATION.md for transparency
- [x] All tests passing (7/7)

### 🔴 Pending

- [ ] Live testing with actual Plane API credentials
- [ ] Testing all 30 tools in real-world scenarios
- [ ] Error handling verification
- [ ] Performance testing (lazy loading verification)
- [ ] MCP client integration testing

---

## Next Steps (Immediate - This Session)

### 1. Live API Testing

**Goal**: Verify all tools work with real Plane instance

```bash
# Setup
cp .env .env.local
# Edit .env.local with your actual credentials:
# PLANE_BASE_URL=https://your-plane-instance.com
# PLANE_API_KEY=your_actual_api_key
# PLANE_WORKSPACE_SLUG=your_workspace

# Run server
plane-rex
```

**Test Plan**:

1. Start MCP server: `plane-rex`
2. Test workspace tools first (discoverable)
3. Test project tools
4. Test issue tools (most commonly used)
5. Verify lazy loading works (client created on first call)
6. Check error handling for invalid inputs

### 2. Basic Iteration

**Focus**: Fix any issues discovered during live testing

Common issues to watch for:

- SDK API mismatches (workspace_slug vs workspace_id)
- Pagination handling
- Field name differences (name vs title, etc.)
- Authentication errors
- Rate limiting

---

## Testing Strategy (Future - CI/CD Ready)

### Unit Tests

- Location: `tests/`
- Coverage: All client methods, tool handlers
- Tools: `pytest`, `pytest-asyncio`, `pytest-cov`
- Target: 80%+ coverage

### Integration Tests

- Location: `tests/integration/`
- Requires: `.env.test.local` with test Plane instance
- Scope: End-to-end tool execution
- Note: Run only on PR/merge to avoid test instance spam

### E2E Tests

- Location: `tests/e2e/`
- Scope: Full MCP workflow
- Tools: `httpx` for MCP protocol testing

### CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
on: [push, pull_request]
jobs:
    test:
        - Run unit tests
        - Run type checking (ty, mypy)
        - Run linting (ruff, flake8)
    integration:
        - Only on main branch
        - Run integration tests
```

---

## GitFlow Strategy for GitHub

### Branch Naming Convention

```
main               # Production-ready code
develop            # Integration branch for features
feature/name       # New features
bugfix/name        # Bug fixes
release/1.0.0      # Release preparation
hotfix/name        # Critical production fixes
```

### Recommended Workflow

1. **Start Feature**:

    ```bash
    git checkout develop
    git checkout -b feature/issue-search-improvement
    ```

2. **Develop & Test**:

    ```bash
    # Make changes
    # Commit frequently with descriptive messages
    git add .
    git commit -m "feat: implement advanced issue search"
    ```

3. **Test Before PR**:

    ```bash
    git push origin feature/issue-search-improvement
    # Create PR from GitHub UI
    ```

4. **Merge Strategy**:
    - **Feature branches**: Squash merge to main
    - **Bugfixes**: Merge commit to preserve history
    - **Releases**: Tag release commits

### Commit Message Convention

```bash
feat: new feature (e.g., "feat: add issue search tool")
fix: bug fix (e.g., "fix: handle null workspace response")
docs: documentation (e.g., "docs: update README with usage")
test: add/modify tests (e.g., "test: add integration tests for cycles")
refactor: code refactoring (e.g., "refactor: simplify client wrapper")
chore: maintenance (e.g., "chore: update dependencies")
```

### When to Use Which Branch

| Branch Type | When to Use           | Example             |
| ----------- | --------------------- | ------------------- |
| `main`      | Production-ready code | Stable releases     |
| `develop`   | Active development    | All feature work    |
| `feature/*` | New features          | Feature development |
| `bugfix/*`  | Production bugs       | Hotfixes            |
| `release/*` | Release prep          | Version tagging     |
| `hotfix/*`  | Critical fixes        | Emergency patches   |

---

## SDK-Specific Development Notes

### Current State: Development Phase (SDK Details CRITICAL)

**These notes are essential for initial development:**

1. **SDK API Mappings** (v0.2.8)

    ```python
    # SDK uses these names - be careful!
    workspace_slug  # NOT workspace_id
    work_items      # NOT issues
    teamspace       # NOT workspace
    identifier      # NOT id (for work items)
    ```

2. **Common SDK Patterns**

    ```python
    # Get work item by identifier
    work_item = client.work_items.retrieve(
        workspace_slug=workspace_id,
        project_id=project_id,
        work_item_id="PROJ-123"  # Identifier format
    )

    # Search work items
    results = client.work_items.advanced_search(
        workspace_slug=workspace_id,
        data=AdvancedSearchWorkItem(query="search term")
    )

    # Create work item
    result = client.work_items.create(
        workspace_slug=workspace_id,
        project_id=project_id,
        data={"name": "Task title", "type": "task"}
    )
    ```

3. **SDK Type Stub Issues**
    - Many SDK methods return `Unknown` type
    - Use `# type: ignore` for SDK calls
    - `.model_dump()` not `.to_dict()` (Pydantic v2)
    - Add `ty.toml` to ignore SDK-related errors

4. **Workspace vs Teamspace**
    ```python
    # Plane uses "teamspace" internally but "workspace" in docs
    # Our wrapper uses workspace_slug for clarity
    client.teamspaces.retrieve(workspace_slug=..., teamspace_id=...)
    ```

### Future State: Production Phase (SDK Details Less Critical)

**Once stable, these notes can be simplified:**

- SDK usage becomes standardized
- Fewer edge cases to document
- More examples in README
- Can remove detailed type ignore notes
- Focus shifts to feature development

---

## Session Continuity Guide

### For Pi Client (When Session Restarts)

**Key files to reference:**

1. `AGENTS.md` - Project overview and patterns
2. `.pi/plans/DEVELOPMENT_PLAN.md` - This file
3. `NAMING_SUMMARY.md` - Naming conventions
4. `PRE_COMMIT.md` - Git workflow

**Critical context for new session:**

1. Current status: Initial setup complete, need live testing
2. SDK uses `workspace_slug`, not `workspace_id`
3. Work items (not issues) in SDK
4. Use `.model_dump()` not `.to_dict()`
5. CLI command is `plane-rex`
6. Package name is `plane-mcp-redux`
7. Python module is `plane_mcp`

**Immediate tasks for next session:**

1. Test with real Plane API
2. Fix any issues discovered
3. Iterate on tool implementations
4. Start writing integration tests

---

## Quick Reference Commands

### Development

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

# Pre-commit (all files)
pre-commit run --all-files
```

### Git

```bash
# Setup
git checkout -b feature/new-feature develop

# Commit
git add .
git commit -m "feat: implement new feature"

# Push & PR
git push origin feature/new-feature
# Create PR on GitHub
```

---

## Notes to Self (Current Session)

- [x] SDK has incomplete type stubs - use type ignores
- [x] Pre-commit hooks need staged files to work properly
- [x] Server name should be "plane-mcp-redux" for consistency
- [x] CLI command is "plane-rex" - short and professional
- [x] All tests passing with new naming
- [ ] Need real Plane credentials for live testing
- [ ] Test lazy loading behavior
- [ ] Verify all 30 tools work correctly
- [ ] Consider adding more error handling
- [ ] Update README with more detailed usage examples

---

## Tags for Session Retrieval

```
#plane-mcp #mcp-server #fastmcp #plane-sdk #python #mcp #mcp-server #ai
#lazy-loading #type-safety #testing #ci-cd #gitflow
```

---

## API Test Results (Session 1)

**Test Date**: Initial setup completed  
**Workspace**: `testing-workspace` at `https://isengard.doorsofdurin.run`

### ✅ Working Operations
1. **List Projects** - Returns paginated list with count
2. **Create Project** - Successfully creates with required fields
3. **Retrieve Project** - Gets project details by ID
4. **Delete Project** - Removes projects without error

### ❌ Non-Working Operations
1. **Retrieve Workspace** - Returns HTTP 404 (endpoint may not exist)
2. **List Teamspaces** - Returns HTTP 404 (no teamspaces or different endpoint)
3. **List Work Items** - Returns HTTP 404 (need to test with valid project)

### Full Test Results
See `.pi/plans/API_TEST_RESULTS.md` for detailed findings.

### Recommendations
- Focus MCP tools on Projects API (fully functional)
- Skip workspace retrieval tools for now
- Test Work Items API with different project
- Document SDK quirks and workarounds

---

## Session Notes (Session 1 - Initial Setup)

### Completed
- [x] Project structure and packaging
- [x] FastMCP server with lazy loading
- [x] Plane SDK client wrapper
- [x] 30 tools implemented
- [x] Full type safety (mypy, ty checking)
- [x] Pre-commit hooks configured
- [x] Pi context setup
- [x] All tests passing (7/7)
- [x] Live API connection test

### SDK Discoveries
- **Import**: `import plane` (not `plane_sdk`)
- **Required field**: `CreateProject.identifier` must be provided
- **Pagination**: Use `.count` and `.results` (not `.data`)
- **Workspace**: Retrieval returns 404, skip for now
- **Teamspaces**: Listing returns 404, may not exist
- **Work Items**: Need to test with valid project ID

### Issues Encountered
1. **SDK is synchronous** (not async) - All calls return immediately
2. **Pydantic models required** for create operations (not dicts)
3. **Identifier field required** for CreateProject (auto-generated in SDK)
4. **Workspace retrieval fails** - 404 error, skip this functionality
5. **Teamspaces API fails** - 404 error, no teamspaces or different endpoint

### Next Session Tasks
- [ ] Update MCP tools based on API test results
- [ ] Remove workspace retrieval tools (returns 404)
- [ ] Add error handling for non-existent workspaces
- [ ] Test Work Items API with known valid project
- [ ] Add more comprehensive error handling
- [ ] Write integration tests for working endpoints
- [ ] Update documentation with API quirks

### Files Created
- `.pi/plans/DEVELOPMENT_PLAN.md` - This file
- `.pi/plans/SESSION_CHECKLIST.md` - Session startup guide
- `.pi/plans/API_TEST_RESULTS.md` - API test findings
- `NAMING.md` - Naming conventions
- `NAMING_SUMMARY.md` - Naming documentation
- `SESSION_GUIDE.md` - Session continuity guide

---

## Quick Reference (Session 1)

### Commands
```bash
# Test connection
export $(grep -v "^#" .env | xargs)
python /tmp/test_plane_connection.py

# Run server
plane-rex

# Run tests
pytest tests/ -v

# Type check
ty check src/plane_mcp/
```

### Key SDK Patterns
```python
import plane
from plane.models.projects import CreateProject

client = plane.PlaneClient(base_url, api_key)

# List (paginated)
projects = client.projects.list(workspace_slug="slug")
print(projects.count)        # Total count
print(projects.results)      # List of Project

# Create (requires model)
data = CreateProject(
    name="Project",
    identifier="PROJ-123"  # Required!
)
project = client.projects.create(workspace_slug="slug", data=data)

# Retrieve
project = client.projects.retrieve(
    workspace_slug="slug",
    project_id="PROJ-123"
)

# Delete
client.projects.delete(
    workspace_slug="slug",
    project_id="PROJ-123"
)
```
