# .pi/plans/ - Development Plans & Context

This directory contains documentation for the plane-mcp-redux project that will be loaded by the pi coding agent.

## Files

| File                   | Purpose                   | When to Use                       |
| ---------------------- | ------------------------- | --------------------------------- |
| `DEVELOPMENT_PLAN.md`  | **Main development plan** | Every session - always read first |
| `SDK_NOTES.md`         | SDK-specific details      | Initial development phase         |
| `SESSION_CHECKLIST.md` | Session startup checklist | When starting new session         |

## Quick Reference

**Current Session Context:**

- Project: `plane-mcp-redux`
- CLI: `plane-rex`
- Module: `plane_mcp`
- Status: Initial setup complete, ready for live testing
- Next: Test with real Plane API

**Key SDK Notes:**

- Use `workspace_slug` not `workspace_id`
- Use `work_items` not `issues`
- Use `.model_dump()` not `.to_dict()`
- SDK has incomplete type stubs (use type ignores)

**See `DEVELOPMENT_PLAN.md` for complete details.**
