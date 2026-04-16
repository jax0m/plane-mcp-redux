"""
Plane MCP Server - FastMCP 3.x with Error Handling

This is a Proof of Concept demonstrating the workflow-oriented CLI design
with proper error handling for production use.
"""

import os
from typing import NoReturn

# Load environment variables
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from plane.errors.errors import ConfigurationError, HttpError, PlaneError
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

# Initialize FastMCP
mcp = FastMCP("plane-mcp-redux")

# =============================================================================
# ERROR HANDLING UTILITIES
# =============================================================================


def format_http_error(error: HttpError) -> str:
    """Format HTTP error with context-specific messages."""
    messages: dict[int, str] = {
        400: "Bad Request - Missing required fields or invalid parameters",
        401: "Unauthorized - Invalid or missing API key",
        403: "Forbidden - Insufficient permissions",
        404: "Not Found - Resource does not exist",
        409: "Conflict - Resource already exists (try different identifier)",
        422: "Validation Error - Invalid data format",
        429: "Rate Limited - Too many requests, please wait",
        500: "Internal Server Error - Plane API issue",
        502: "Bad Gateway - Plane API unavailable",
        503: "Service Unavailable - Plane API temporarily down",
    }
    base_msg = messages.get(error.status_code, f"HTTP {error.status_code}")
    return (
        f"❌ {base_msg}\n   Details: {error.message}"
        if hasattr(error, "message")
        else f"❌ {base_msg}"
    )


def handle_api_error(error: Exception) -> NoReturn:
    """
    Handle API-specific errors with user-friendly messages.

    Args:
        error: The exception that occurred

    Raises:
        ToolError: Formatted error message
    """
    if isinstance(error, ConfigurationError):
        raise ToolError(
            "❌ Configuration Error\n"
            "   - Check your .env file\n"
            "   - Ensure PLANE_API_KEY is set\n"
            "   - Ensure PLANE_BASE_URL is correct"
        )
    if isinstance(error, HttpError):
        raise ToolError(format_http_error(error))
    if isinstance(error, PlaneError):
        raise ToolError(f"❌ Plane API Error: {error}")
    raise ToolError(f"❌ Unexpected error ({type(error).__name__}): {str(error)[:200]}")


# =============================================================================
# PRE-CHECK UTILITIES
# =============================================================================


def project_exists(project_id: str, client) -> bool:
    """Check if a project exists by ID."""
    try:
        client.projects.retrieve(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG, project_id=project_id
        )
        return True
    except HttpError:
        return False
    except Exception:
        return False


def work_item_exists(project_id: str, work_item_id: str, client) -> bool:
    """Check if a work item exists."""
    try:
        client.work_items.retrieve(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=project_id,
            work_item_id=work_item_id,
        )
        return True
    except HttpError:
        return False
    except Exception:
        return False


def label_exists(project_id: str, label_id: str, client) -> bool:
    """Check if a label exists."""
    try:
        client.labels.retrieve(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=project_id,
            label_id=label_id,
        )
        return True
    except HttpError:
        return False
    except Exception:
        return False


# =============================================================================
# GLOBAL CONFIGURATION
# =============================================================================


class Settings(BaseSettings):
    """Global Plane MCP configuration."""

    PLANE_BASE_URL: str = os.getenv("PLANE_BASE_URL", "https://api.plane.so")
    PLANE_API_KEY: str = os.getenv("PLANE_API_KEY", "")
    PLANE_WORKSPACE_SLUG: str = os.getenv("PLANE_WORKSPACE_SLUG", "workspace")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()


# =============================================================================
# LAZY LOADING CLIENT
# =============================================================================

_plane_client = None


def get_plane_client():
    """Lazy client initialization."""
    global _plane_client
    if _plane_client is None:
        from plane.client.plane_client import PlaneClient

        _plane_client = PlaneClient(
            base_url=settings.PLANE_BASE_URL,
            api_key=settings.PLANE_API_KEY,
        )
    return _plane_client


# =============================================================================
# PROJECT COMMANDS
# =============================================================================


@mcp.tool(description="List all projects in workspace")
async def project_list() -> list[dict]:
    """List all projects in the configured workspace."""
    try:
        client = get_plane_client()
        from plane.models.query_params import PaginatedQueryParams

        projects = client.projects.list(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            params=PaginatedQueryParams(per_page=20),
        )

        result = []
        for p in projects.results:
            result.append(
                {
                    "id": p.id,
                    "identifier": p.identifier,
                    "name": p.name,
                    "description": p.description,
                    "total_members": p.total_members,
                    "total_modules": p.total_modules,
                }
            )

        return result

    except Exception as e:
        handle_api_error(e)


@mcp.tool(description="Create a new project")
async def project_create(name: str, identifier: str | None = None) -> dict:
    """Create a new project in the configured workspace."""
    try:
        from plane.models.projects import CreateProject

        client = get_plane_client()

        if identifier is None:
            import uuid

            identifier = f"PROJ-{uuid.uuid4().hex[:8]}"

        data = CreateProject(name=name, identifier=identifier)
        project = client.projects.create(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG, data=data
        )

        return {
            "id": project.id,
            "identifier": project.identifier,
            "name": project.name,
            "description": project.description,
        }

    except Exception as e:
        handle_api_error(e)


@mcp.tool(description="Get project details by UUID")
async def project_info(project_id: str) -> dict:
    """Get detailed information about a project by UUID."""
    try:
        client = get_plane_client()
        project = client.projects.retrieve(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG, project_id=project_id
        )

        return {
            "id": project.id,
            "identifier": project.identifier,
            "name": project.name,
            "description": project.description,
            "total_members": project.total_members,
            "total_modules": project.total_modules,
            "total_cycles": project.total_cycles,
        }

    except Exception as e:
        handle_api_error(e)


@mcp.tool(description="Delete a project by UUID")
async def project_delete(project_id: str) -> dict:
    """Delete a project by UUID. Verifies existence before deletion."""
    try:
        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project_id, client):
            raise ToolError(
                f"❌ Project not found: {project_id}\n"
                "   - Verify the project ID is correct\n"
                "   - Use project_list to see available projects"
            )

        client.projects.delete(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG, project_id=project_id
        )
        return {"status": "deleted", "project_id": project_id}

    except ToolError:
        raise
    except Exception as e:
        handle_api_error(e)


# =============================================================================
# WORK ITEM COMMANDS
# =============================================================================


@mcp.tool(description="List work items in a project")
async def work_list(
    project_id: str,
    state: str | None = None,
    label: str | None = None,
) -> list[dict]:
    """List work items in a project with optional filters. Verifies project exists."""
    try:
        client = get_plane_client()
        from plane.models.query_params import WorkItemQueryParams

        # Pre-check: verify project exists
        if not project_exists(project_id, client):
            raise ToolError(
                f"❌ Project not found: {project_id}\n"
                "   - Verify the project ID is correct\n"
                "   - Use project_list to see available projects"
            )

        params = WorkItemQueryParams()
        if state:
            params.state = state
        if label:
            params.labels = [label]

        work_items = client.work_items.list(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=project_id,
            params=params,
        )

        result = []
        for w in work_items.results:
            result.append(
                {
                    "id": w.id,
                    "name": w.name,
                    "description_html": w.description_html,
                    "priority": w.priority,
                    "state": w.state,
                    "labels": w.labels,
                    "assignees": w.assignees,
                }
            )

        return result

    except ToolError:
        raise
    except Exception as e:
        handle_api_error(e)


@mcp.tool(description="Create a new work item (task/issue)")
async def work_add(
    project_id: str,
    title: str,
    description: str | None = None,
    priority: str = "medium",
    labels: list[str] | None = None,
) -> dict:
    """Create a new work item. Verifies project exists before creation."""
    try:
        from plane.models.work_items import CreateWorkItem

        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project_id, client):
            raise ToolError(
                f"❌ Project not found: {project_id}\n"
                "   - Verify the project ID is correct\n"
                "   - Use project_list to see available projects"
            )

        data = CreateWorkItem(
            project_id=project_id,
            name=title,
            description=description,
            priority=priority,
            labels=labels or [],
        )

        work_item = client.work_items.create(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=project_id,
            data=data,
        )

        return {
            "id": work_item.id,
            "name": work_item.name,
            "description_html": work_item.description_html,
            "priority": work_item.priority,
            "labels": work_item.labels,
        }

    except ToolError:
        raise
    except Exception as e:
        handle_api_error(e)


@mcp.tool(description="Update a work item")
async def work_update(
    project_id: str,
    work_item_id: str,
    name: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    labels: list[str] | None = None,
) -> dict:
    """Update a work item with partial fields. Verifies existence before update."""
    try:
        from plane.models.work_items import UpdateWorkItem

        client = get_plane_client()

        # Pre-check: verify work item exists
        if not work_item_exists(project_id, work_item_id, client):
            raise ToolError(
                f"❌ Work item not found: {work_item_id} in project {project_id}\n"
                "   - Verify the IDs are correct\n"
                "   - Use work_list to see available work items"
            )

        # Validate at least one field is provided
        if all(v is None for v in [name, description, priority, labels]):
            raise ToolError(
                "❌ No update fields provided\n"
                "   - Provide at least one of: name, description, priority, labels"
            )

        data = UpdateWorkItem()
        if name is not None:
            data.name = name
        if description is not None:
            data.description = description
        if priority is not None:
            data.priority = priority
        if labels is not None:
            data.labels = labels

        work_item = client.work_items.update(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=project_id,
            work_item_id=work_item_id,
            data=data,
        )

        return {
            "id": work_item.id,
            "name": work_item.name,
            "priority": work_item.priority,
        }

    except ToolError:
        raise
    except Exception as e:
        handle_api_error(e)


@mcp.tool(description="Delete a work item")
async def work_delete(project_id: str, work_item_id: str) -> dict:
    """Delete a work item. Verifies existence before deletion."""
    try:
        client = get_plane_client()

        # Pre-check: verify work item exists
        if not work_item_exists(project_id, work_item_id, client):
            raise ToolError(
                f"❌ Work item not found: {work_item_id} in project {project_id}\n"
                "   - Verify the IDs are correct\n"
                "   - Use work_list to see available work items"
            )

        client.work_items.delete(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=project_id,
            work_item_id=work_item_id,
        )
        return {"status": "deleted", "work_item_id": work_item_id}

    except ToolError:
        raise
    except Exception as e:
        handle_api_error(e)


# =============================================================================
# LABEL COMMANDS
# =============================================================================


@mcp.tool(description="List labels in a project")
async def label_list(project_id: str) -> list[dict]:
    """List all labels in a project. Verifies project exists."""
    try:
        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project_id, client):
            raise ToolError(
                f"❌ Project not found: {project_id}\n"
                "   - Verify the project ID is correct\n"
                "   - Use project_list to see available projects"
            )

        labels = client.labels.list(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG, project_id=project_id
        )

        return [label.model_dump() for label in labels.results]

    except ToolError:
        raise
    except Exception as e:
        handle_api_error(e)


@mcp.tool(description="Create a new label")
async def label_create(project_id: str, name: str, color: str = "#0088FE") -> dict:
    """Create a new label in a project. Verifies project exists before creation."""
    try:
        from plane.models.labels import CreateLabel

        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project_id, client):
            raise ToolError(
                f"❌ Project not found: {project_id}\n"
                "   - Verify the project ID is correct\n"
                "   - Use project_list to see available projects"
            )

        label = client.labels.create(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=project_id,
            data=CreateLabel(name=name, color=color),
        )

        return label.model_dump()  # type: ignore[no-any-return]

    except ToolError:
        raise
    except Exception as e:
        handle_api_error(e)


@mcp.tool(description="Assign a label to a work item")
async def label_assign(
    project_id: str,
    work_item_id: str,
    label_id: str,
) -> dict:
    """Assign a label to a work item. Verifies both exist before assignment."""
    try:
        from plane.models.work_items import UpdateWorkItem

        client = get_plane_client()

        # Pre-check: verify work item exists
        if not work_item_exists(project_id, work_item_id, client):
            raise ToolError(
                f"❌ Work item not found: {work_item_id} in project {project_id}\n"
                "   - Verify the IDs are correct\n"
                "   - Use work_list to see available work items"
            )

        # Pre-check: verify label exists
        if not label_exists(project_id, label_id, client):
            raise ToolError(
                f"❌ Label not found: {label_id} in project {project_id}\n"
                "   - Verify the label ID is correct\n"
                "   - Use label_list to see available labels"
            )

        work_item = client.work_items.update(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=project_id,
            work_item_id=work_item_id,
            data=UpdateWorkItem(labels=[label_id]),
        )

        return {
            "status": "assigned",
            "work_item_id": work_item_id,
            "labels": work_item.labels,
        }

    except ToolError:
        raise
    except Exception as e:
        handle_api_error(e)


# =============================================================================
# PROMPTS
# =============================================================================


@mcp.prompt("create-work-item")
def create_work_item_prompt(
    project_name: str = "Select project...",
    task_name: str = "Enter task name...",
    description: str = "Brief description...",
    priority: str = "medium",
    labels: list[str] | None = None,
) -> str:
    """
    Interactive prompt to create a new work item.

    Args:
        project_name: Name of the project
        task_name: Title of the work item
        description: Detailed description
        priority: Priority level (low, medium, high)
        labels: List of labels to assign

    Returns:
        Formatted prompt for CLI or chat
    """
    if labels is None:
        labels_str = "(none)"
    else:
        labels_str = ", ".join(labels) if labels else "(none)"
    return f"""
# Create Work Item

**Project**: {project_name}
**Task**: {task_name}
**Description**: {description}
**Priority**: {priority}
**Labels**: {labels_str}

---

Ready to create? Type 'confirm' to create this work item.
"""


@mcp.prompt("list-work-items")
def list_work_items_prompt(
    project_name: str = "Select project...",
    state_filter: str = "All states",
    label_filter: str = "All labels",
) -> str:
    """
    Interactive prompt to list work items with filters.

    Args:
        project_name: Name of the project
        state_filter: Filter by state (todo, in progress, done)
        label_filter: Filter by label name

    Returns:
        Formatted prompt for CLI or chat
    """
    return f"""
# List Work Items

**Project**: {project_name}
**State Filter**: {state_filter}
**Label Filter**: {label_filter}

---

Ready to list? Type 'confirm' to fetch work items.
"""


# =============================================================================
# HELPER: Print available tools
# =============================================================================


@mcp.tool(description="Print available tools")
async def print_tools() -> str:
    """Print available MCP tools for debugging."""
    tools = [
        "project_list - List all projects",
        "project_create - Create new project",
        "project_info - Get project details",
        "project_delete - Delete project",
        "work_list - List work items",
        "work_add - Create new work item",
        "work_update - Update work item",
        "work_delete - Delete work item",
        "label_list - List labels",
        "label_create - Create new label",
        "label_assign - Assign label to work item",
    ]
    return "\n".join(tools)


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 Plane MCP Server Starting...")
    print("=" * 80)
    print()
    print(f"Base URL: {settings.PLANE_BASE_URL}")
    print(f"Workspace: {settings.PLANE_WORKSPACE_SLUG}")
    print()
    print("Available tools:")
    print("  - project_list")
    print("  - project_create")
    print("  - project_info")
    print("  - project_delete")
    print("  - work_list")
    print("  - work_add")
    print("  - work_update")
    print("  - work_delete")
    print("  - label_list")
    print("  - label_create")
    print("  - label_assign")
    print()
    print("Run with: fastmcp dev inspector src/plane_mcp/server.py")
    print("=" * 80)
