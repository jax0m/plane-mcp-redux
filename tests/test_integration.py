"""
Integration tests for Plane MCP server and CLI.

These tests use real API credentials from environment variables.
Run with: pytest tests/test_integration.py -v

Required environment variables:
    - PLANE_BASE_URL
    - PLANE_API_KEY
    - PLANE_WORKSPACE_SLUG
"""

import os
import uuid
from collections.abc import Generator
from typing import Any

import pytest
from plane.errors.errors import HttpError
from pydantic_settings import BaseSettings, SettingsConfigDict

from plane_mcp.server import (
    get_plane_client,
    label_exists,
    project_exists,
    work_item_exists,
)

# =============================================================================
# CONFIGURATION
# =============================================================================


class Settings(BaseSettings):
    """Test configuration from environment."""

    PLANE_BASE_URL: str = os.getenv("PLANE_BASE_URL", "https://api.plane.so")
    PLANE_API_KEY: str = os.getenv("PLANE_API_KEY", "")
    PLANE_WORKSPACE_SLUG: str = os.getenv("PLANE_WORKSPACE_SLUG", "workspace")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

# Skip all tests if credentials are not configured
pytestmark = pytest.mark.skipif(
    not settings.PLANE_API_KEY,
    reason="PLANE_API_KEY not configured - set in .env or environment",
)


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture(scope="session")
def client():
    """Get the Plane client for testing."""
    return get_plane_client()


@pytest.fixture(scope="function")
def test_project(client) -> Generator[dict[str, Any], None, None]:
    """Create a test project and clean up after the test."""
    from plane.models.projects import CreateProject

    # Use short uppercase identifier (matches Plane's expected format)
    unique_id = uuid.uuid4().hex[:4].upper()
    identifier = f"T{unique_id}"

    data = CreateProject(name=f"Test Project {identifier}", identifier=identifier)
    project = client.projects.create(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG, data=data
    )

    yield {"id": project.id, "identifier": project.identifier}

    # Cleanup
    try:
        client.projects.delete(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG, project_id=project.id
        )
    except HttpError:
        pass  # Project may already be deleted


@pytest.fixture(scope="function")
def test_work_item(client, test_project) -> Generator[dict[str, Any], None, None]:
    """Create a test work item and clean up after the test."""
    from plane.models.work_items import CreateWorkItem

    data = CreateWorkItem(
        name="Test Work Item",
        description="This is a test work item",
        priority="medium",
    )
    work_item = client.work_items.create(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG,
        project_id=test_project["id"],
        data=data,
    )

    yield {"id": work_item.id, "name": work_item.name}

    # Cleanup
    try:
        client.work_items.delete(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=test_project["id"],
            work_item_id=work_item.id,
        )
    except HttpError:
        pass  # Work item may already be deleted


@pytest.fixture(scope="function")
def test_label(client, test_project) -> Generator[dict[str, Any], None, None]:
    """Create a test label and clean up after the test."""
    from plane.models.labels import CreateLabel

    data = CreateLabel(name="Test Label", color="#FF0000")
    label = client.labels.create(
        workspace_slug=settings.PLANE_WORKSPACE_SLUG,
        project_id=test_project["id"],
        data=data,
    )

    yield {"id": label.id, "name": label.name}

    # Cleanup - labels may not have delete endpoint
    pass


# =============================================================================
# PROJECT TESTS
# =============================================================================


class TestProjectPreChecks:
    """Test project existence pre-checks."""

    def test_project_exists_returns_true(self, client, test_project):
        """Verify project_exists returns True for existing project."""
        assert project_exists(test_project["id"], client) is True

    def test_project_exists_returns_false(self, client):
        """Verify project_exists returns False for non-existent project."""
        fake_id = str(uuid.uuid4())
        assert project_exists(fake_id, client) is False


class TestProjectList:
    """Test project listing."""

    def test_list_projects_returns_list(self, client):
        """Verify list returns at least some projects."""
        from plane.models.query_params import PaginatedQueryParams

        projects = client.projects.list(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            params=PaginatedQueryParams(per_page=20),
        )
        assert hasattr(projects, "results")
        assert isinstance(projects.results, list)

    def test_list_projects_has_required_fields(self, client):
        """Verify projects have required fields."""
        from plane.models.query_params import PaginatedQueryParams

        projects = client.projects.list(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            params=PaginatedQueryParams(per_page=1),
        )
        if projects.results:
            p = projects.results[0]
            assert hasattr(p, "id")
            assert hasattr(p, "name")
            assert hasattr(p, "identifier")


class TestProjectCreate:
    """Test project creation."""

    def test_create_project_minimal(self, client):
        """Verify project can be created with minimal fields."""
        from plane.models.projects import CreateProject

        # Use short uppercase identifier
        unique_id = uuid.uuid4().hex[:4].upper()
        identifier = f"M{unique_id}"

        data = CreateProject(name="Minimal Test", identifier=identifier)
        project = client.projects.create(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG, data=data
        )

        assert project.id is not None
        assert project.name == "Minimal Test"
        assert project.identifier == identifier

        # Cleanup
        try:
            client.projects.delete(
                workspace_slug=settings.PLANE_WORKSPACE_SLUG, project_id=project.id
            )
        except HttpError:
            pass


class TestProjectRetrieve:
    """Test project retrieval."""

    def test_retrieve_project(self, client, test_project):
        """Verify project can be retrieved by ID."""
        project = client.projects.retrieve(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=test_project["id"],
        )
        assert project.id == test_project["id"]
        assert project.identifier == test_project["identifier"]

    def test_retrieve_nonexistent_project_raises(self, client):
        """Verify retrieving non-existent project raises HttpError."""
        fake_id = str(uuid.uuid4())
        with pytest.raises(HttpError):
            client.projects.retrieve(
                workspace_slug=settings.PLANE_WORKSPACE_SLUG, project_id=fake_id
            )


# =============================================================================
# WORK ITEM TESTS
# =============================================================================


class TestWorkItemPreChecks:
    """Test work item existence pre-checks."""

    def test_work_item_exists_returns_true(self, client, test_project, test_work_item):
        """Verify work_item_exists returns True for existing work item."""
        assert (
            work_item_exists(test_project["id"], test_work_item["id"], client) is True
        )

    def test_work_item_exists_returns_false_project(self, client):
        """Verify work_item_exists returns False for non-existent project."""
        fake_project = str(uuid.uuid4())
        fake_work_item = str(uuid.uuid4())
        assert work_item_exists(fake_project, fake_work_item, client) is False

    def test_work_item_exists_returns_false_item(self, client, test_project):
        """Verify work_item_exists returns False for non-existent work item."""
        fake_work_item = str(uuid.uuid4())
        assert work_item_exists(test_project["id"], fake_work_item, client) is False


class TestWorkItemCreate:
    """Test work item creation."""

    def test_create_work_item_minimal(self, client, test_project):
        """Verify work item can be created with just name."""
        from plane.models.work_items import CreateWorkItem

        data = CreateWorkItem(name="Minimal Work Item")
        work_item = client.work_items.create(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=test_project["id"],
            data=data,
        )

        assert work_item.id is not None
        assert work_item.name == "Minimal Work Item"

        # Cleanup
        try:
            client.work_items.delete(
                workspace_slug=settings.PLANE_WORKSPACE_SLUG,
                project_id=test_project["id"],
                work_item_id=work_item.id,
            )
        except HttpError:
            pass

    def test_create_work_item_with_all_fields(self, client, test_project, test_label):
        """Verify work item can be created with all optional fields."""
        from plane.models.work_items import CreateWorkItem

        data = CreateWorkItem(
            name="Full Work Item",
            description="Test description",
            priority="high",
            labels=[test_label["id"]],
        )
        work_item = client.work_items.create(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=test_project["id"],
            data=data,
        )

        assert work_item.name == "Full Work Item"
        assert work_item.priority == "high"

        # Cleanup
        try:
            client.work_items.delete(
                workspace_slug=settings.PLANE_WORKSPACE_SLUG,
                project_id=test_project["id"],
                work_item_id=work_item.id,
            )
        except HttpError:
            pass


class TestWorkItemUpdate:
    """Test work item updates."""

    def test_update_work_item_name(self, client, test_project, test_work_item):
        """Verify work item name can be updated."""
        from plane.models.work_items import UpdateWorkItem

        data = UpdateWorkItem(name="Updated Name")
        work_item = client.work_items.update(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=test_project["id"],
            work_item_id=test_work_item["id"],
            data=data,
        )

        assert work_item.name == "Updated Name"

    def test_update_work_item_priority(self, client, test_project, test_work_item):
        """Verify work item priority can be updated."""
        from plane.models.work_items import UpdateWorkItem

        data = UpdateWorkItem(priority="high")
        work_item = client.work_items.update(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=test_project["id"],
            work_item_id=test_work_item["id"],
            data=data,
        )

        assert work_item.priority == "high"


class TestWorkItemDelete:
    """Test work item deletion."""

    def test_delete_work_item(self, client, test_project):
        """Verify work item can be deleted."""
        from plane.models.work_items import CreateWorkItem

        # Create a work item
        data = CreateWorkItem(name="To Be Deleted")
        work_item = client.work_items.create(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=test_project["id"],
            data=data,
        )

        # Delete it
        client.work_items.delete(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=test_project["id"],
            work_item_id=work_item.id,
        )

        # Verify it's gone
        assert work_item_exists(test_project["id"], work_item.id, client) is False


# =============================================================================
# LABEL TESTS
# =============================================================================


class TestLabelPreChecks:
    """Test label existence pre-checks."""

    def test_label_exists_returns_true(self, client, test_project, test_label):
        """Verify label_exists returns True for existing label."""
        assert label_exists(test_project["id"], test_label["id"], client) is True

    def test_label_exists_returns_false(self, client, test_project):
        """Verify label_exists returns False for non-existent label."""
        fake_label = str(uuid.uuid4())
        assert label_exists(test_project["id"], fake_label, client) is False


class TestLabelCreate:
    """Test label creation."""

    def test_create_label_minimal(self, client, test_project):
        """Verify label can be created with just name."""
        from plane.models.labels import CreateLabel

        data = CreateLabel(name="Minimal Label")
        label = client.labels.create(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=test_project["id"],
            data=data,
        )

        assert label.id is not None
        assert label.name == "Minimal Label"


class TestLabelList:
    """Test label listing."""

    def test_list_labels_returns_list(self, client, test_project):
        """Verify list returns labels."""
        labels = client.labels.list(
            workspace_slug=settings.PLANE_WORKSPACE_SLUG,
            project_id=test_project["id"],
        )
        assert hasattr(labels, "results")
        assert isinstance(labels.results, list)


# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================


class TestErrorHandling:
    """Test error handling with invalid inputs."""

    def test_invalid_project_id_returns_false(self, client):
        """Verify invalid project ID is handled gracefully."""
        # Invalid UUID format
        assert project_exists("not-a-uuid", client) is False

    def test_invalid_work_item_id_returns_false(self, client, test_project):
        """Verify invalid work item ID is handled gracefully."""
        # Invalid UUID format
        assert work_item_exists(test_project["id"], "not-a-uuid", client) is False

    def test_invalid_label_id_returns_false(self, client, test_project):
        """Verify invalid label ID is handled gracefully."""
        # Invalid UUID format
        assert label_exists(test_project["id"], "not-a-uuid", client) is False
