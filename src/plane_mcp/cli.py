"""
Plane MCP CLI - Complete Command Line Interface

Usage:
    plane-rex <command> [options]

Examples:
    plane-rex project list
    plane-rex work add "Fix bug" --project my-project --label bug --priority high
    plane-rex --autoconfirm project delete <id>
"""

import os
from typing import Any

import click
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    PLANE_BASE_URL: str = os.getenv("PLANE_BASE_URL", "https://api.plane.so")
    PLANE_API_KEY: str = os.getenv("PLANE_API_KEY", "")
    PLANE_WORKSPACE_SLUG: str = os.getenv("PLANE_WORKSPACE_SLUG", "workspace")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

# Global context for autoconfirm
ctx_autoconfirm = False


def handle_error(error: Exception) -> None:
    """Handle API errors with user-friendly messages."""
    # Import error classes lazily to avoid SDK import overhead
    from plane.errors.errors import ConfigurationError, HttpError, PlaneError

    if isinstance(error, ConfigurationError):
        message = f"❌ Configuration error: {error}"
    elif isinstance(error, HttpError):
        if error.status_code == 404:
            message = "❌ Not Found (HTTP 404): Resource does not exist"
        elif error.status_code == 400:
            message = f"❌ Bad Request (HTTP 400): {error.message if hasattr(error, 'message') else error}"
        elif error.status_code == 409:
            message = "❌ Conflict (HTTP 409): Resource already exists"
        else:
            message = f"❌ API error (HTTP {error.status_code}): {error.message if hasattr(error, 'message') else error}"
    elif isinstance(error, PlaneError):
        message = f"❌ Plane API error: {error}"
    else:
        message = f"❌ Unexpected error ({type(error).__name__}): {str(error)[:200]}"
    click.echo(message, err=True)
    raise click.exceptions.ClickException(message)


_plane_client: Any = None


def get_plane_client():
    """Get or create the Plane client."""
    global _plane_client
    if _plane_client is None:
        from plane.client.plane_client import PlaneClient

        _plane_client = PlaneClient(
            base_url=settings.PLANE_BASE_URL,
            api_key=settings.PLANE_API_KEY,
        )
    return _plane_client


def project_exists(project_id: str, client) -> bool:
    """Check if a project exists by ID."""
    from plane.errors.errors import HttpError

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
    from plane.errors.errors import HttpError

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


def confirm_action(message: str, autoconfirm: bool = False) -> bool:
    """Ask for user confirmation."""
    if autoconfirm:
        return True
    return click.confirm(message)


def _get_projects():
    """Get list of projects."""
    client = get_plane_client()
    from plane.models.query_params import PaginatedQueryParams

    projects = client.projects.list(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG,
        params=PaginatedQueryParams(per_page=20),
    )
    return projects.results


@click.group()
@click.option(
    "--autoconfirm",
    "-y",
    is_flag=True,
    default=False,
    help="Automatically confirm all actions without prompting",
)
@click.pass_context
def cli(ctx, autoconfirm):
    """Plane MCP CLI - Manage your Plane workspaces"""
    ctx.ensure_object(dict)
    ctx.obj["autoconfirm"] = autoconfirm


@cli.group()
def project():
    """Project management commands"""
    pass


@project.command(name="list")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def project_list(workspace):
    """List all projects in workspace"""
    try:
        projects = _get_projects()
        if projects:
            click.echo(f"Found {len(projects)} project(s):")
            for p in projects[:10]:
                click.echo(f"  [{p.id}] {p.name} ({p.identifier})")
        else:
            click.echo("No projects found")
    except Exception as e:
        handle_error(e)


@project.command(name="create")
@click.argument("name")
@click.option("--identifier", "-i", required=True, help="Unique identifier")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def project_create(name, identifier, workspace):
    """Create a new project"""
    try:
        from plane.models.projects import CreateProject

        client = get_plane_client()
        data = CreateProject(name=name, identifier=identifier)
        project = client.projects.create(workspace_slug=workspace, data=data)
        click.echo("✅ Created:")
        click.echo(f"   ID: {project.id}")
        click.echo(f"   Identifier: {project.identifier}")
    except Exception as e:
        handle_error(e)


@project.command(name="info")
@click.argument("project_id")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def project_info(project_id, workspace):
    """Get project details"""
    try:
        client = get_plane_client()
        project = client.projects.retrieve(
            workspace_slug=workspace, project_id=project_id
        )
        click.echo(f"Project: {project.name} ({project.identifier})")
        click.echo(f"ID: {project.id}")
        click.echo(f"Members: {project.total_members}")
    except Exception as e:
        handle_error(e)


@project.command(name="delete")
@click.argument("project_id")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Skip confirmation prompt"
)
@click.pass_context
def project_delete(ctx, project_id, workspace, yes):
    """Delete a project"""
    try:
        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project_id, client):
            raise click.ClickException(
                f"❌ Project not found: {project_id}\n"
                "   - Verify the project ID is correct\n"
                "   - Use 'project list' to see available projects"
            )

        # Confirmation
        autoconfirm = ctx.obj.get("autoconfirm", False) or yes
        if not confirm_action(
            f"Delete project '{project_id}'? This cannot be undone.", autoconfirm
        ):
            click.echo("Cancelled.")
            return

        client.projects.delete(workspace_slug=workspace, project_id=project_id)
        click.echo(f"✅ Deleted project: {project_id}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@cli.group()
def work():
    """Work item management commands"""
    pass


@work.command(name="add")
@click.argument("title")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option("--description", "-d", default=None, help="Description")
@click.option("--priority", "-P", default="medium", help="Priority: low, medium, high")
@click.option("--label", "-L", multiple=True, default=[], help="Labels")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def work_add(title, project, description, priority, label, workspace):
    """Create a new work item"""
    try:
        from plane.models.work_items import CreateWorkItem

        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project, client):
            raise click.ClickException(
                f"❌ Project not found: {project}\n"
                "   - Verify the project ID is correct\n"
                "   - Use 'project list' to see available projects"
            )

        labels = list(label) if label else []
        data = CreateWorkItem(
            project_id=project,
            name=title,
            description=description,
            priority=priority,
            labels=labels,
        )
        work_item = client.work_items.create(
            workspace_slug=workspace, project_id=project, data=data
        )
        click.echo("✅ Created:")
        click.echo(f"   ID: {work_item.id}")
        click.echo(f"   Name: {work_item.name}")
        click.echo(f"   Priority: {work_item.priority}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@work.command(name="list")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def work_list(project, workspace):
    """List work items in project"""
    try:
        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project, client):
            raise click.ClickException(
                f"❌ Project not found: {project}\n"
                "   - Verify the project ID is correct\n"
                "   - Use 'project list' to see available projects"
            )

        from plane.models.query_params import WorkItemQueryParams

        params = WorkItemQueryParams()
        work_items = client.work_items.list(
            workspace_slug=workspace, project_id=project, params=params
        )
        if work_items.results:
            click.echo(f"Found {len(work_items.results)} work item(s):")
            for w in work_items.results[:20]:
                click.echo(f"  [{w.id}] {w.name} [{w.priority}]")
        else:
            click.echo("No work items found")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@work.command(name="update")
@click.argument("work_item_id")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option("--name", "-n", default=None, help="New title")
@click.option("--description", "-D", default=None, help="New description")
@click.option("--priority", "-P", default=None, help="New priority")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def work_update(work_item_id, project, name, description, priority, workspace):
    """Update a work item"""
    try:
        from plane.models.work_items import UpdateWorkItem

        client = get_plane_client()

        # Pre-check: verify work item exists
        if not work_item_exists(project, work_item_id, client):
            raise click.ClickException(
                f"❌ Work item not found: {work_item_id} in project {project}\n"
                "   - Verify the IDs are correct\n"
                "   - Use 'work list -p {project}' to see available work items"
            )

        # Validate at least one field is provided
        if all(v is None for v in [name, description, priority]):
            raise click.ClickException(
                "❌ No update fields provided\n"
                "   - Provide at least one of: --name, --description, --priority"
            )

        data = UpdateWorkItem()
        if name is not None:
            data.name = name
        if description is not None:
            data.description = description
        if priority is not None:
            data.priority = priority

        work_item = client.work_items.update(
            workspace_slug=workspace,
            project_id=project,
            work_item_id=work_item_id,
            data=data,
        )
        click.echo("✅ Updated:")
        click.echo(f"   ID: {work_item.id}")
        click.echo(f"   Name: {work_item.name}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@work.command(name="delete")
@click.argument("work_item_id")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Skip confirmation prompt"
)
@click.pass_context
def work_delete(ctx, work_item_id, project, workspace, yes):
    """Delete a work item"""
    try:
        client = get_plane_client()

        # Pre-check: verify work item exists
        if not work_item_exists(project, work_item_id, client):
            raise click.ClickException(
                f"❌ Work item not found: {work_item_id} in project {project}\n"
                "   - Verify the IDs are correct\n"
                "   - Use 'work list -p {project}' to see available work items"
            )

        # Confirmation
        autoconfirm = ctx.obj.get("autoconfirm", False) or yes
        if not confirm_action(
            f"Delete work item '{work_item_id}'? This cannot be undone.", autoconfirm
        ):
            click.echo("Cancelled.")
            return

        client.work_items.delete(
            workspace_slug=workspace, project_id=project, work_item_id=work_item_id
        )
        click.echo(f"✅ Deleted work item: {work_item_id}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@cli.group()
def label():
    """Label management commands"""
    pass


@label.command(name="create")
@click.argument("name")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option("--color", "-c", default="#0088FE", help="Color")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def label_create(name, project, color, workspace):
    """Create a new label"""
    try:
        from plane.models.labels import CreateLabel

        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project, client):
            raise click.ClickException(
                f"❌ Project not found: {project}\n"
                "   - Verify the project ID is correct\n"
                "   - Use 'project list' to see available projects"
            )

        label = client.labels.create(
            workspace_slug=workspace,
            project_id=project,
            data=CreateLabel(name=name, color=color),
        )
        click.echo("✅ Created:")
        click.echo(f"   ID: {label.id}")
        click.echo(f"   Name: {label.name}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@label.command(name="list")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def label_list(project, workspace):
    """List labels in project"""
    try:
        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project, client):
            raise click.ClickException(
                f"❌ Project not found: {project}\n"
                "   - Verify the project ID is correct\n"
                "   - Use 'project list' to see available projects"
            )

        labels = client.labels.list(workspace_slug=workspace, project_id=project)
        if labels.results:
            click.echo(f"Found {len(labels.results)} label(s):")
            for label in labels.results[:20]:
                click.echo(f"  [{label.id}] {label.name} ({label.color})")
        else:
            click.echo("No labels found")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@label.command(name="info")
@click.argument("label_id")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def label_info(label_id, project, workspace):
    """Get label details"""
    try:
        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project, client):
            raise click.ClickException(
                f"❌ Project not found: {project}\n"
                "   - Verify the project ID is correct\n"
                "   - Use 'project list' to see available projects"
            )

        label = client.labels.retrieve(
            workspace_slug=workspace, project_id=project, label_id=label_id
        )
        click.echo(f"Label: {label.name}")
        click.echo(f"ID: {label.id}")
        click.echo(f"Color: {label.color}")
        if hasattr(label, "description") and label.description:
            click.echo(f"Description: {label.description}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


# =============================================================================
# STICKY COMMANDS (Workspace-level)
# =============================================================================


@cli.group()
def sticky():
    """Sticky note management commands (workspace-level)"""
    pass


@sticky.command(name="list")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def sticky_list(workspace):
    """List all sticky notes in workspace"""
    try:
        click.echo("Fetching stickies...")
        client = get_plane_client()

        stickies = client.stickies.list(workspace_slug=workspace)
        if stickies.results:
            click.echo(f"Found {len(stickies.results)} sticky note(s):")
            for s in stickies.results[:20]:
                desc = (
                    s.description_stripped[:50]
                    if s.description_stripped
                    else "(no content)"
                )
                click.echo(f"  [{s.id}] {desc}... [{s.background_color}]")
        else:
            click.echo("No sticky notes found")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@sticky.command(name="create")
@click.argument("content")
@click.option("--name", "-n", default=None, help="Optional title")
@click.option(
    "--color", "-c", default=None, help="Background color (peach, dark-blue, orange)"
)
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def sticky_create(content, name, color, workspace):
    """Create a new sticky note"""
    try:
        click.echo("Creating sticky...")
        from plane.models.stickies import CreateSticky

        client = get_plane_client()

        data = CreateSticky(
            name=name,
            description=content,
            description_html=f"<p>{content}</p>",
            background_color=color,
        )
        sticky = client.stickies.create(workspace_slug=workspace, data=data)
        click.echo("✅ Created:")
        click.echo(f"   ID: {sticky.id}")
        click.echo(f"   Content: {sticky.description_stripped[:50]}...")
        click.echo(f"   Background: {sticky.background_color}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@sticky.command(name="info")
@click.argument("sticky_id")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def sticky_info(sticky_id, workspace):
    """Get sticky note details"""
    try:
        click.echo("Fetching sticky...")
        client = get_plane_client()

        sticky = client.stickies.retrieve(workspace_slug=workspace, sticky_id=sticky_id)
        click.echo("Sticky Note")
        click.echo(f"ID: {sticky.id}")
        if sticky.name:
            click.echo(f"Title: {sticky.name}")
        click.echo(f"Content: {sticky.description_stripped}")
        click.echo(f"Background: {sticky.background_color}")
        if sticky.color:
            click.echo(f"Text Color: {sticky.color}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@sticky.command(name="update")
@click.argument("sticky_id")
@click.option("--content", "-c", default=None, help="New content")
@click.option("--name", "-n", default=None, help="New title")
@click.option("--color", "-C", default=None, help="New background color")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def sticky_update(sticky_id, content, name, color, workspace):
    """Update a sticky note"""
    try:
        click.echo("Updating sticky...")
        from plane.models.stickies import UpdateSticky

        client = get_plane_client()

        # Validate at least one field is provided
        if all(v is None for v in [content, name, color]):
            raise click.ClickException(
                "❌ No update fields provided\n"
                "   - Provide at least one of: --content, --name, --color"
            )

        data = UpdateSticky()
        if name is not None:
            data.name = name
        if content is not None:
            data.description = content
            data.description_html = f"<p>{content}</p>"
        if color is not None:
            data.background_color = color

        sticky = client.stickies.update(
            workspace_slug=workspace, sticky_id=sticky_id, data=data
        )
        click.echo("✅ Updated:")
        click.echo(f"   ID: {sticky.id}")
        click.echo(f"   Content: {sticky.description_stripped[:50]}...")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@sticky.command(name="delete")
@click.argument("sticky_id")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Skip confirmation prompt"
)
@click.pass_context
def sticky_delete(ctx, sticky_id, workspace, yes):
    """Delete a sticky note"""
    try:
        click.echo("Verifying sticky...")
        client = get_plane_client()

        # Confirmation
        autoconfirm = ctx.obj.get("autoconfirm", False) or yes
        if not confirm_action(
            f"Delete sticky '{sticky_id}'? This cannot be undone.", autoconfirm
        ):
            click.echo("Cancelled.")
            return

        click.echo("Deleting...")
        client.stickies.delete(workspace_slug=workspace, sticky_id=sticky_id)
        click.echo(f"✅ Deleted sticky: {sticky_id}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


# =============================================================================
# STATE COMMANDS
# =============================================================================


@cli.group()
def state():
    """State/workflow management commands"""
    pass


@state.command(name="list")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def state_list(project, workspace):
    """List all states in project"""
    try:
        click.echo("Fetching states...")
        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project, client):
            raise click.ClickException(
                f"❌ Project not found: {project}\n"
                "   - Verify the project ID is correct\n"
                "   - Use 'project list' to see available projects"
            )

        states = client.states.list(workspace_slug=workspace, project_id=project)
        if states.results:
            click.echo(f"Found {len(states.results)} state(s):")
            for s in states.results:
                click.echo(f"  [{s.id}] {s.name} [{s.group}] {s.color}")
        else:
            click.echo("No states found")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@state.command(name="create")
@click.argument("name")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option(
    "--group", "-g", default="new", help="State group (new, started, completed)"
)
@click.option("--color", "-c", default="#0088FE", help="State color")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def state_create(name, project, group, color, workspace):
    """Create a new state"""
    try:
        click.echo("Creating state...")
        from plane.models.states import CreateState

        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project, client):
            raise click.ClickException(
                f"❌ Project not found: {project}\n"
                "   - Verify the project ID is correct\n"
                "   - Use 'project list' to see available projects"
            )

        data = CreateState(name=name, group=group, color=color)
        state = client.states.create(
            workspace_slug=workspace, project_id=project, data=data
        )
        click.echo("✅ Created:")
        click.echo(f"   ID: {state.id}")
        click.echo(f"   Name: {state.name}")
        click.echo(f"   Group: {state.group}")
        click.echo(f"   Color: {state.color}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@state.command(name="info")
@click.argument("state_id")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def state_info(state_id, project, workspace):
    """Get state details"""
    try:
        click.echo("Fetching state...")
        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project, client):
            raise click.ClickException(
                f"❌ Project not found: {project}\n"
                "   - Verify the project ID is correct\n"
                "   - Use 'project list' to see available projects"
            )

        state = client.states.retrieve(
            workspace_slug=workspace, project_id=project, state_id=state_id
        )
        click.echo(f"State: {state.name}")
        click.echo(f"ID: {state.id}")
        click.echo(f"Group: {state.group}")
        click.echo(f"Color: {state.color}")
        if hasattr(state, "sort_order"):
            click.echo(f"Sort Order: {state.sort_order}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@state.command(name="update")
@click.argument("state_id")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option("--name", "-n", default=None, help="New name")
@click.option("--group", "-g", default=None, help="New group (new, started, completed)")
@click.option("--color", "-c", default=None, help="New color")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def state_update(state_id, project, name, group, color, workspace):
    """Update a state"""
    try:
        click.echo("Updating state...")
        from plane.models.states import UpdateState

        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project, client):
            raise click.ClickException(
                f"❌ Project not found: {project}\n"
                "   - Verify the project ID is correct\n"
                "   - Use 'project list' to see available projects"
            )

        # Validate at least one field is provided
        if all(v is None for v in [name, group, color]):
            raise click.ClickException(
                "❌ No update fields provided\n"
                "   - Provide at least one of: --name, --group, --color"
            )

        data = UpdateState()
        if name is not None:
            data.name = name
        if group is not None:
            data.group = group
        if color is not None:
            data.color = color

        state = client.states.update(
            workspace_slug=workspace, project_id=project, state_id=state_id, data=data
        )
        click.echo("✅ Updated:")
        click.echo(f"   ID: {state.id}")
        click.echo(f"   Name: {state.name}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@state.command(name="delete")
@click.argument("state_id")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Skip confirmation prompt"
)
@click.pass_context
def state_delete(ctx, state_id, project, workspace, yes):
    """Delete a state"""
    try:
        click.echo("Verifying state...")
        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project, client):
            raise click.ClickException(
                f"❌ Project not found: {project}\n"
                "   - Verify the project ID is correct\n"
                "   - Use 'project list' to see available projects"
            )

        # Confirmation
        autoconfirm = ctx.obj.get("autoconfirm", False) or yes
        if not confirm_action(
            f"Delete state '{state_id}'? This cannot be undone.", autoconfirm
        ):
            click.echo("Cancelled.")
            return

        click.echo("Deleting...")
        client.states.delete(
            workspace_slug=workspace, project_id=project, state_id=state_id
        )
        click.echo(f"✅ Deleted state: {state_id}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


# =============================================================================
# WORK ITEM VIEW COMMAND
# =============================================================================


@work.command(name="info")
@click.argument("work_item_id")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def work_info(work_item_id, project, workspace):
    """Get work item details"""
    try:
        click.echo("Fetching work item...")
        from plane.models.query_params import RetrieveQueryParams

        client = get_plane_client()

        # Pre-check: verify project exists
        if not project_exists(project, client):
            raise click.ClickException(
                f"❌ Project not found: {project}\n"
                "   - Verify the project ID is correct\n"
                "   - Use 'project list' to see available projects"
            )

        work_item = client.work_items.retrieve(
            workspace_slug=workspace,
            project_id=project,
            work_item_id=work_item_id,
            params=RetrieveQueryParams(expand="labels,assignees,state"),
        )
        click.echo(f"Work Item: {work_item.name}")
        click.echo(f"ID: {work_item.id}")
        click.echo(f"Priority: {work_item.priority}")
        if hasattr(work_item, "state") and work_item.state:
            click.echo(
                f"State: {work_item.state.name if hasattr(work_item.state, 'name') else work_item.state}"
            )
        if hasattr(work_item, "description_html") and work_item.description_html:
            # Strip HTML for display
            import re

            desc = re.sub(r"<[^>]+>", "", work_item.description_html)
            click.echo(f"Description: {desc[:200]}...")
        if hasattr(work_item, "labels") and work_item.labels:
            label_names = [
                label.name if hasattr(label, "name") else label
                for label in work_item.labels
            ]
            click.echo(f"Labels: {', '.join(label_names)}")
        if hasattr(work_item, "assignees") and work_item.assignees:
            assignee_names = [
                assignee.name if hasattr(assignee, "name") else assignee
                for assignee in work_item.assignees
            ]
            click.echo(f"Assignees: {', '.join(assignee_names)}")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


@work.command(name="my-tasks")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
@click.option("--limit", "-l", default=20, help="Maximum items to show")
def my_tasks(workspace, limit):
    """List work items assigned to you across all projects"""
    try:
        click.echo("Fetching your assigned tasks...")
        from plane.models.query_params import PaginatedQueryParams, WorkItemQueryParams

        client = get_plane_client()

        # Get current user
        me = client.users.get_me()
        user_id = me.id

        # Get all projects
        projects = client.projects.list(
            workspace_slug=workspace,
            params=PaginatedQueryParams(per_page=50),
        )

        assigned_items = []
        for project in projects.results:
            try:
                work_items = client.work_items.list(
                    workspace_slug=workspace,
                    project_id=project.id,
                    params=WorkItemQueryParams(assignees=[user_id], per_page=limit),
                )
                for wi in work_items.results:
                    assigned_items.append((project.name, wi))
            except Exception:
                pass  # Skip projects we can't access

        if assigned_items:
            click.echo(f"\nFound {len(assigned_items)} assigned work item(s):")
            for project_name, wi in assigned_items[:limit]:
                click.echo(f"  [{wi.id}] {wi.name} - {project_name} [{wi.priority}]")
        else:
            click.echo("No assigned work items found")
    except click.ClickException:
        raise
    except Exception as e:
        handle_error(e)


if __name__ == "__main__":
    cli()
