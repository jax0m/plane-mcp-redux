"""
Plane MCP CLI - Complete Command Line Interface

Usage:
    plane-rex <command> [options]

Examples:
    plane-rex project list
    plane-rex work add "Fix bug" --project my-project --label bug --priority high
"""

import os

import click
from dotenv import load_dotenv
from plane.errors.errors import ConfigurationError, HttpError, PlaneError
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    PLANE_BASE_URL: str = os.getenv("PLANE_BASE_URL", "https://api.plane.so")
    PLANE_API_KEY: str = os.getenv("PLANE_API_KEY", "")
    PLANE_WORKSPACE_SLUG: str = os.getenv("PLANE_WORKSPACE_SLUG", "workspace")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()


def handle_error(func, error):
    error_type = type(error).__name__
    if isinstance(error, ConfigurationError):
        message = f"❌ Configuration error: {error}"
    elif isinstance(error, HttpError):
        message = f"❌ API error ({error.status_code}): {str(error)}"
    elif isinstance(error, PlaneError):
        message = f"❌ Plane API error: {error}"
    else:
        message = f"❌ Unexpected error ({error_type})"
    click.echo(message, err=True)
    raise click.exceptions.ClickException(message)


_plane_client = None


def get_plane_client():
    global _plane_client
    if _plane_client is None:
        from plane.client.plane_client import PlaneClient

        _plane_client = PlaneClient(
            base_url=settings.PLANE_BASE_URL,
            api_key=settings.PLANE_API_KEY,
        )
    return _plane_client


def _get_projects():
    client = get_plane_client()
    from plane.models.query_params import PaginatedQueryParams

    projects = client.projects.list(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG,
        params=PaginatedQueryParams(per_page=20),
    )
    return projects.results


@click.group()
def cli():
    """Plane MCP CLI - Manage your Plane workspaces"""
    pass


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
        handle_error(project_list, e)


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
        handle_error(project_create, e)


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
        handle_error(project_info, e)


@project.command(name="delete")
@click.argument("project_id")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def project_delete(project_id, workspace):
    """Delete a project"""
    try:
        client = get_plane_client()
        client.projects.delete(workspace_slug=workspace, project_id=project_id)
        click.echo(f"✅ Deleted project: {project_id}")
    except Exception as e:
        handle_error(project_delete, e)


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
    except Exception as e:
        handle_error(work_add, e)


@work.command(name="list")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def work_list(project, workspace):
    """List work items in project"""
    try:
        client = get_plane_client()
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
    except Exception as e:
        handle_error(work_list, e)


@work.command(name="update")
@click.argument("work_item_id")
@click.option("--name", "-n", default=None, help="New title")
@click.option("--description", "-D", default=None, help="New description")
@click.option("--priority", "-P", default=None, help="New priority")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def work_update(work_item_id, name, description, priority, workspace):
    """Update a work item"""
    try:
        from plane.models.work_items import UpdateWorkItem

        client = get_plane_client()
        data = UpdateWorkItem()
        if name is not None:
            data.name = name
        if description is not None:
            data.description = description
        if priority is not None:
            data.priority = priority
        work_item = client.work_items.update(
            workspace_slug=workspace,
            project_id=work_item_id,
            work_item_id=work_item_id,
            data=data,
        )
        click.echo("✅ Updated:")
        click.echo(f"   ID: {work_item.id}")
        click.echo(f"   Name: {work_item.name}")
    except Exception as e:
        handle_error(work_update, e)


@work.command(name="delete")
@click.argument("work_item_id")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def work_delete(work_item_id, workspace):
    """Delete a work item"""
    try:
        client = get_plane_client()
        client.work_items.delete(
            workspace_slug=workspace, project_id=work_item_id, work_item_id=work_item_id
        )
        click.echo(f"✅ Deleted work item: {work_item_id}")
    except Exception as e:
        handle_error(work_delete, e)


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
        label = client.labels.create(
            workspace_slug=workspace,
            project_id=project,
            data=CreateLabel(name=name, color=color),
        )
        click.echo("✅ Created:")
        click.echo(f"   ID: {label.id}")
        click.echo(f"   Name: {label.name}")
    except Exception as e:
        handle_error(label_create, e)


@label.command(name="list")
@click.option("--project", "-p", required=True, help="Project identifier")
@click.option(
    "--workspace", "-w", default=settings.PLANE_WORKSPACE_SLUG, help="Workspace slug"
)
def label_list(project, workspace):
    """List labels in project"""
    try:
        client = get_plane_client()
        labels = client.labels.list(workspace_slug=workspace, project_id=project)
        if labels.results:
            click.echo(f"Found {len(labels.results)} label(s):")
            for label in labels.results[:20]:
                click.echo(f"  [{label.id}] {label.name} ({label.color})")
        else:
            click.echo("No labels found")
    except Exception as e:
        handle_error(label_list, e)


if __name__ == "__main__":
    cli()
