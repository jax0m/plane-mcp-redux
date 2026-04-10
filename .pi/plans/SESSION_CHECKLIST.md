# Plane MCP Redux - Session Startup Checklist

## Before Starting Work

### 1. Read Development Context

- [ ] Review `.pi/plans/DEVELOPMENT_PLAN.md`
- [ ] Check `AGENTS.md` for project overview
- [ ] Note any tasks from previous session

### 2. Setup Environment

- [ ] Verify `.env.local` exists with credentials
- [ ] Run `plane-rex` to test server starts
- [ ] Check git status (should be clean or have intended changes)

### 3. Verify Tools

- [ ] `ty check src/plane_mcp/` - Type checking
- [ ] `mypy src/plane_mcp/` - MyPy check
- [ ] `pytest tests/ -v` - Run tests
- [ ] `ruff check src/ tests/` - Linting

### 4. Plan Your Work

- [ ] Identify the task for this session
- [ ] Check `DEVELOPMENT_PLAN.md` for related tasks
- [ ] Create feature branch: `git checkout -b feature/your-feature develop`

## During Development

### Before Committing

- [ ] Run `pre-commit run --all-files`
- [ ] Update tests if needed
- [ ] Update documentation if API changed
- [ ] Write descriptive commit message

### If Making SDK Changes

- [ ] Update `.pi/plans/SDK_NOTES.md` with any SDK discoveries
- [ ] Document any workarounds for SDK issues
- [ ] Add type ignores with explanation

## After Finishing Work

### Before Pushing

- [ ] Commit with proper message: `feat: description`
- [ ] Push: `git push origin feature/your-feature`
- [ ] Create PR on GitHub
- [ ] Add reviewers

### Documentation

- [ ] Update `DEVELOPMENT_PLAN.md` - mark tasks complete
- [ ] Update `NAMING_SUMMARY.md` if naming changed
- [ ] Add any SDK notes to `.pi/plans/SDK_NOTES.md`

## Quick Commands Reference

```bash
# Development
plane-rex                    # Run server
pytest tests/ -v            # Run tests
ty check src/plane_mcp/     # Type check
pre-commit run --all-files  # Pre-commit hooks

# Git
git checkout -b feature/name develop  # Create branch
git commit -m "feat: description"     # Commit
git push origin feature/name          # Push

# Environment
cp .env .env.local                  # Setup env
# Edit .env.local with your credentials
```

## Session Notes Template

```
## Session: [Date]
### Completed:
- [ ] Task 1
- [ ] Task 2

### Issues Encountered:
- Issue 1: Description and solution

### Next Session Tasks:
- [ ] Task 1
- [ ] Task 2

### SDK Discoveries:
- New SDK method discovered: `client.workitems.advanced_search()`
- SDK quirk: `workspace_slug` instead of `workspace_id`
```
