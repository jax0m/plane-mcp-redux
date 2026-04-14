"""Core Plane MCP Server using modern FastMCP 3.x patterns."""

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.server.context import Context
from pydantic_settings import BaseSettings

from .client import PlaneClientWrapper

# Load environment variables
load_dotenv()


class PlaneConfig(BaseSettings):
    """Configuration settings for Plane MCP server."""

    PLANE_BASE_URL: str = "https://api.plane.so"
    PLANE_API_KEY: str = ""
    PLANE_WORKSPACE_SLUG: str = "workspace"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",  # Ignore extra env vars
    }


def get_plane_client() -> PlaneClientWrapper:
    """
    Dependency injection for Plane client.

    This provides lazy loading - the client is only created when a tool needs it.
    """
    config = PlaneConfig()
    return PlaneClientWrapper(
        base_url=config.PLANE_BASE_URL,
        api_key=config.PLANE_API_KEY,
    )


# Create the FastMCP server instance
mcp = FastMCP(
    name="plane-mcp-redux",
    instructions="Plane project management MCP server. Use workspace tools to discover workspaces, then project tools to explore projects, and issue tools to manage work items. Most commonly used: list_issues, get_issue, create_issue, update_issue_state.",
)


# ============================================================================
# Workspace Tools
# ============================================================================


@mcp.tool(
    description="List all workspaces (teamspaces) accessible with the current API key. Returns workspace metadata including name, slug, and identifiers. Use this to discover available workspaces.",
)
async def list_workspaces(
    page: int = 1,
    limit: int = 20,
    client: PlaneClientWrapper = Depends(get_plane_client),
    ctx: Context | None = None,
) -> dict:
    """List all accessible workspaces."""
    workspaces = client.list_workspaces(page=page, limit=limit)
    return {
        "workspaces": workspaces,
        "page": page,
        "limit": limit,
    }


@mcp.tool(
    description="Get detailed information about a specific workspace by ID or slug. Returns workspace configuration, settings, and metadata.",
)
async def get_workspace(
    workspace_slug: str,
    workspace_id: str,
    include_projects: bool = False,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Get workspace details."""
    workspace = client.get_workspace(workspace_slug)

    if workspace:
        result = workspace.copy() if isinstance(workspace, dict) else dict(workspace)
        if include_projects:
            result["projects"] = []  # Projects would be fetched separately
        return result
    return {"error": "Workspace not found"}


# ============================================================================
# Project Tools
# ============================================================================


@mcp.tool(
    description="List all projects within a workspace. Returns project metadata including name, description, and project type.",
)
async def list_projects(
    workspace_id: str,
    page: int = 1,
    limit: int = 20,
    client: PlaneClientWrapper = Depends(get_plane_client),
    ctx: Context | None = None,
) -> dict:
    """List projects in a workspace."""
    projects = client.list_projects(workspace_slug=workspace_id, page=page, limit=limit)
    return {
        "projects": projects,
        "page": page,
        "limit": limit,
    }


@mcp.tool(
    description="Get detailed information about a specific project including settings, members, and associated components.",
)
async def get_project(
    workspace_id: str,
    project_id: str,
    include_members: bool = False,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Get project details."""
    project = client.get_project(workspace_slug=workspace_id, project_id=project_id)

    if project:
        result = project.copy() if isinstance(project, dict) else dict(project)
        if include_members:
            result["members"] = client.get_project_members(
                workspace_slug=workspace_id, project_id=project_id
            )
        return result
    return {"error": "Project not found"}


@mcp.tool(
    description="Create a new project within a workspace. Specify project name, description, type, and other settings.",
)
async def create_project(
    workspace_id: str,
    name: str,
    description: str | None = None,
    project_type: str | None = None,
    lead: str | None = None,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Create a new project."""
    project = client.create_project(
        workspace_slug=workspace_id,
        name=name,
        description=description,
        project_type=project_type,
        lead=lead,
    )

    if project:
        return project
    return {"error": "Failed to create project"}


@mcp.tool(
    description="Update details of an existing project including name, description, and other settings.",
)
async def update_project(
    workspace_id: str,
    project_id: str,
    name: str | None = None,
    description: str | None = None,
    project_type: str | None = None,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Update project details."""
    kwargs = {}
    if name:
        kwargs["name"] = name
    if description:
        kwargs["description_html"] = description
    if project_type:
        kwargs["type"] = project_type

    project = client.update_project(
        workspace_slug=workspace_id,
        project_id=project_id,
        **kwargs,
    )

    if project:
        return project
    return {"error": "Failed to update project"}


# ============================================================================
# Issue (Work Item) Tools
# ============================================================================


@mcp.tool(
    description="List all work items (issues) within a project. Supports filtering by state, assignee, labels, and other criteria. Returns paginated results.",
)
async def list_issues(
    workspace_id: str,
    project_id: str,
    page: int = 1,
    limit: int = 20,
    state: str | None = None,
    assignee: str | None = None,
    labels: list[str] | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
    ctx: Context | None = None,
) -> dict:
    """List issues with optional filters."""
    filters = {}
    if state:
        filters["state"] = state
    if assignee:
        filters["assignees"] = assignee
    if labels:
        filters["labels"] = labels  # type: ignore[assignment]  # type: ignore[assignment]

    work_items = client.list_work_items(
        workspace_slug=workspace_id,
        project_id=project_id,
        page=page,
        limit=limit,
        **filters,
    )
    return {
        "issues": work_items,
        "page": page,
        "limit": limit,
        "total": len(work_items),
    }


@mcp.tool(
    description="Get detailed information about a specific work item including description, state, assignee, labels, and comments.",
)
async def get_issue(
    workspace_id: str,
    project_id: str,
    issue_id: str,
    include_comments: bool = False,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Get work item details."""
    work_item = client.get_work_item(
        workspace_slug=workspace_id,
        project_id=project_id,
        work_item_id=issue_id,
    )

    if work_item:
        result = work_item.copy() if isinstance(work_item, dict) else dict(work_item)
        if include_comments:
            result["comments"] = []
        return result
    return {"error": "Work item not found"}


@mcp.tool(
    description="Create a new work item in a project. Specify title, description, state, assignee, labels, and other properties.",
)
async def create_issue(
    workspace_id: str,
    project_id: str,
    title: str,
    description: str | None = None,
    state: str | None = None,
    assignee: str | None = None,
    labels: list[str] | None = None,
    type: str = "issue",
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Create a new work item."""
    work_item = client.create_work_item(
        workspace_slug=workspace_id,
        project_id=project_id,
        title=title,
        description=description,
        state=state,
        assignee=assignee,
        labels=labels,
        type=type,
    )

    if work_item:
        return work_item
    return {"error": "Failed to create work item"}


@mcp.tool(
    description="Update details of an existing work item including title, description, state, assignee, and labels.",
)
async def update_issue(
    workspace_id: str,
    project_id: str,
    issue_id: str,
    title: str | None = None,
    description: str | None = None,
    state: str | None = None,
    assignee: str | None = None,
    labels: list[str] | None = None,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Update work item details."""
    kwargs = {}
    if title:
        kwargs["name"] = title
    if description:
        kwargs["description_html"] = description
    if state:
        kwargs["state"] = state
    if assignee:
        kwargs["assignees"] = [assignee]  # type: ignore[assignment]  # type: ignore[assignment]
    if labels:
        kwargs["labels"] = labels  # type: ignore[assignment]  # type: ignore[assignment]

    work_item = client.update_work_item(
        workspace_slug=workspace_id,
        project_id=project_id,
        work_item_id=issue_id,
        **kwargs,
    )

    if work_item:
        return work_item
    return {"error": "Failed to update work item"}


@mcp.tool(
    description="Permanently delete a work item from a project.",
    annotations={"destructiveHint": True},
)
async def delete_issue(
    workspace_id: str,
    project_id: str,
    issue_id: str,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Delete a work item."""
    success = client.delete_work_item(
        workspace_slug=workspace_id,
        project_id=project_id,
        work_item_id=issue_id,
    )

    if success:
        return {
            "message": "Work item deleted successfully",
            "workspace_id": workspace_id,
            "project_id": project_id,
            "issue_id": issue_id,
        }
    return {"error": "Failed to delete work item"}


@mcp.tool(
    description="Assign a work item to a specific user or team member.",
)
async def assign_issue(
    workspace_id: str,
    project_id: str,
    issue_id: str,
    assignee: str,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Assign work item to a user."""
    work_item = client.update_work_item(
        workspace_slug=workspace_id,
        project_id=project_id,
        work_item_id=issue_id,
        assignees=[assignee],
    )

    if work_item:
        return {
            "message": "Work item assigned successfully",
            "issue_id": issue_id,
            "assignee": assignee,
            "work_item": work_item,
        }
    return {"error": "Failed to assign work item"}


@mcp.tool(
    description="Search for work items using text search across title and description. Supports fuzzy matching and filters.",
)
async def search_issues(
    workspace_id: str,
    project_id: str,
    query: str,
    page: int = 1,
    limit: int = 20,
    state: str | None = None,
    assignee: str | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
    ctx: Context | None = None,
) -> dict:
    """Search for work items."""
    filters = {}
    if state:
        filters["state"] = state
    if assignee:
        filters["assignees"] = assignee

    work_items = client.search_work_items(
        workspace_slug=workspace_id,
        project_id=project_id,
        query=query,
        page=page,
        limit=limit,
        **filters,
    )
    return {
        "results": work_items,
        "query": query,
        "page": page,
        "limit": limit,
    }


@mcp.tool(
    description="Change the state/status of a work item (e.g., to-do, in-progress, done).",
)
async def update_issue_state(
    workspace_id: str,
    project_id: str,
    issue_id: str,
    state: str,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Update work item state."""
    work_item = client.update_issue_state(
        workspace_slug=workspace_id,
        project_id=project_id,
        work_item_id=issue_id,
        state=state,
    )

    if work_item:
        return {
            "message": "State updated successfully",
            "issue_id": issue_id,
            "state": state,
            "work_item": work_item,
        }
    return {"error": "Failed to update state"}


# ============================================================================
# Cycle Tools
# ============================================================================


@mcp.tool(
    description="List all cycles (sprints) in a project. Cycles are time-boxed periods for completing work items.",
)
async def list_cycles(
    workspace_id: str,
    project_id: str,
    page: int = 1,
    limit: int = 20,
    client: PlaneClientWrapper = Depends(get_plane_client),
    ctx: Context | None = None,
) -> dict:
    """List cycles in a project."""
    cycles = client.list_cycles(
        workspace_slug=workspace_id,
        project_id=project_id,
        page=page,
        limit=limit,
    )
    return {"cycles": cycles, "page": page, "limit": limit}


@mcp.tool(
    description="Get detailed information about a specific cycle including issues, start date, end date, and progress.",
)
async def get_cycle(
    workspace_id: str,
    project_id: str,
    cycle_id: str,
    include_issues: bool = False,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Get cycle details."""
    cycle = client.get_cycle(
        workspace_slug=workspace_id,
        project_id=project_id,
        cycle_id=cycle_id,
    )

    if cycle:
        result = cycle.copy() if isinstance(cycle, dict) else dict(cycle)
        if include_issues:
            result["issues"] = []
        return result
    return {"error": "Cycle not found"}


@mcp.tool(
    description="Create a new cycle (sprint) in a project.",
)
async def create_cycle(
    workspace_id: str,
    project_id: str,
    name: str,
    start_date: str | None = None,
    end_date: str | None = None,
    description: str | None = None,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Create a new cycle."""
    cycle = client.create_cycle(
        workspace_slug=workspace_id,
        project_id=project_id,
        name=name,
        start_date=start_date,
        end_date=end_date,
        description=description,
    )

    if cycle:
        return cycle
    return {"error": "Failed to create cycle"}


@mcp.tool(
    description="Update details of an existing cycle.",
)
async def update_cycle(
    workspace_id: str,
    project_id: str,
    cycle_id: str,
    name: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    description: str | None = None,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Update cycle details."""
    kwargs = {}
    if name:
        kwargs["name"] = name
    if start_date:
        kwargs["start_date"] = start_date
    if end_date:
        kwargs["end_date"] = end_date
    if description:
        kwargs["description_html"] = description

    cycle = client.update_cycle(
        workspace_slug=workspace_id,
        project_id=project_id,
        cycle_id=cycle_id,
        **kwargs,
    )

    if cycle:
        return cycle
    return {"error": "Failed to update cycle"}


# ============================================================================
# Module Tools
# ============================================================================


@mcp.tool(
    description="List all modules (feature sets) in a project.",
)
async def list_modules(
    workspace_id: str,
    project_id: str,
    page: int = 1,
    limit: int = 20,
    client: PlaneClientWrapper = Depends(get_plane_client),
    ctx: Context | None = None,
) -> dict:
    """List modules in a project."""
    modules = client.list_modules(
        workspace_slug=workspace_id,
        project_id=project_id,
        page=page,
        limit=limit,
    )
    return {"modules": modules, "page": page, "limit": limit}


@mcp.tool(
    description="Get detailed information about a specific module.",
)
async def get_module(
    workspace_id: str,
    project_id: str,
    module_id: str,
    include_issues: bool = False,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Get module details."""
    module = client.get_module(
        workspace_slug=workspace_id,
        project_id=project_id,
        module_id=module_id,
    )

    if module:
        result = module.copy() if isinstance(module, dict) else dict(module)
        if include_issues:
            result["issues"] = []
        return result
    return {"error": "Module not found"}


# ============================================================================
# Page Tools
# ============================================================================


@mcp.tool(
    description="List all pages (documentation) in a workspace.",
)
async def list_pages(
    workspace_id: str,
    page: int = 1,
    limit: int = 20,
    client: PlaneClientWrapper = Depends(get_plane_client),
    ctx: Context | None = None,
) -> dict:
    """List pages in a workspace."""
    pages = client.list_pages(
        workspace_slug=workspace_id,
        page=page,
        limit=limit,
    )
    return {"pages": pages, "page": page, "limit": limit}


@mcp.tool(
    description="Get detailed information about a specific page.",
)
async def get_page(
    workspace_id: str,
    page_id: str,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Get page details."""
    page = client.get_page(workspace_slug=workspace_id, page_id=page_id)

    if page:
        return page.copy() if isinstance(page, dict) else dict(page)
    return {"error": "Page not found"}


@mcp.tool(
    description="Create a new page (documentation) in a workspace.",
)
async def create_page(
    workspace_id: str,
    title: str,
    content: str | None = None,
    description: str | None = None,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Create a new page."""
    page = client.create_page(
        workspace_slug=workspace_id,
        title=title,
        content=content,
        description=description,
    )

    if page:
        return page
    return {"error": "Failed to create page"}


@mcp.tool(
    description="Update details of an existing page.",
)
async def update_page(
    workspace_id: str,
    page_id: str,
    title: str | None = None,
    content: str | None = None,
    description: str | None = None,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Update page details."""
    kwargs = {}
    if title:
        kwargs["name"] = title
    if content:
        kwargs["content_html"] = content
    if description:
        kwargs["description_html"] = description

    page = client.update_page(
        workspace_slug=workspace_id,
        page_id=page_id,
        **kwargs,
    )

    if page:
        return page
    return {"error": "Failed to update page"}


# ============================================================================
# State Tools
# ============================================================================


@mcp.tool(
    description="List all available states (e.g., backlog, todo, in_progress, done) for issues in a project. States define the workflow of issues.",
)
async def list_states(
    workspace_id: str,
    project_id: str,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """List available states for a project."""
    states = client.list_states(workspace_slug=workspace_id, project_id=project_id)
    return {
        "states": states,
        "workspace_id": workspace_id,
        "project_id": project_id,
    }


# ============================================================================
# Member Tools
# ============================================================================


@mcp.tool(
    description="List all members (users) in a workspace. Returns user information including name, email, and roles.",
)
async def list_members(
    workspace_id: str,
    page: int = 1,
    limit: int = 20,
    client: PlaneClientWrapper = Depends(get_plane_client),
    ctx: Context | None = None,
) -> dict:
    """List members in a workspace."""
    members = client.list_members(
        workspace_slug=workspace_id,
        page=page,
        limit=limit,
    )
    return {"members": members, "page": page, "limit": limit}


@mcp.tool(
    description="Get detailed information about a specific workspace member.",
)
async def get_member(
    workspace_id: str,
    member_id: str,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """Get member details."""
    member = client.get_member(workspace_slug=workspace_id, member_id=member_id)

    if member:
        return member.copy() if isinstance(member, dict) else dict(member)
    return {"error": "Member not found"}


# ============================================================================
# Label Tools
# ============================================================================


@mcp.tool(
    description="List all labels/tags in a project. Labels are used to categorize and filter work items.",
)
async def list_labels(
    workspace_id: str,
    project_id: str,
    ctx: Context | None = None,
    client: PlaneClientWrapper = Depends(get_plane_client),
) -> dict:
    """List labels in a project."""
    labels = client.list_labels(workspace_slug=workspace_id, project_id=project_id)
    return {
        "labels": labels,
        "workspace_id": workspace_id,
        "project_id": project_id,
    }


# ============================================================================
# Main Entry Point
# ============================================================================


def main() -> None:
    """Main entry point for the Plane MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
