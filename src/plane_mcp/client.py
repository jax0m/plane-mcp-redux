"""Plane API client for MCP server using the official plane-sdk."""
# type: ignore[union-attr,call-arg,invalid-argument-type,invalid-assignment]  # plane-sdk types incomplete

from typing import Any

from plane import PlaneClient


class PlaneClientWrapper:
    """
    Wrapper around the official Plane SDK client.

    Adapts the plane-sdk API to provide a consistent interface
    for tool implementations.
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the Plane client wrapper.

        Args:
            base_url: Plane API base URL
            api_key: Plane API key for authentication
        """
        self.base_url = base_url
        self.api_key = api_key
        self._client: PlaneClient | None = None

    @property
    def client(self) -> PlaneClient:
        """Get or create the underlying Plane client."""
        if self._client is None:
            self._client = PlaneClient(
                base_url=self.base_url,
                api_key=self.api_key,
            )
        return self._client

    async def close(self) -> None:
        """Clean up client resources."""
        if self._client:
            # PlaneClient may have async cleanup in future versions
            pass

    # ==================== Workspace Methods ====================

    def get_workspace(self, workspace_id: str) -> dict[str, Any] | None:
        """
        Get workspace details.

        Note: The SDK uses teamspace terminology. Workspaces are accessed
        through teamspace resource.
        """
        try:
            # Try to retrieve by ID
            result = self.client.teamspaces.retrieve(id=workspace_id)
            return result.model_dump() if result else None
        except Exception:
            return None

    def list_workspaces(self, page: int = 1, limit: int = 20) -> list[dict[str, Any]]:
        """List all workspaces (teamspaces)."""
        try:
            result = self.client.teamspaces.list()
            return [t.model_dump() for t in result] if result else []
        except Exception:
            return []

    # ==================== Project Methods ====================

    def get_project(self, workspace_id: str, project_id: str) -> dict[str, Any] | None:
        """Get project details by ID."""
        try:
            result = self.client.projects.retrieve(
                workspace_id=workspace_id,
                project_id=project_id,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    def list_projects(
        self, workspace_id: str, page: int = 1, limit: int = 20
    ) -> list[dict[str, Any]]:
        """List projects in a workspace."""
        try:
            result = self.client.projects.list(
                workspace_id=workspace_id,
                page=page,
                limit=limit,
            )
            return [p.model_dump() for p in result] if result else []
        except Exception:
            return []

    def create_project(
        self,
        workspace_id: str,
        name: str,
        description: str | None = None,
        project_type: str | None = None,
        lead: str | None = None,
    ) -> dict[str, Any] | None:
        """Create a new project."""
        try:
            data = {
                "name": name,
            }
            if description:
                data["description"] = description
            if project_type:
                data["type"] = project_type
            if lead:
                data["lead"] = lead

            result = self.client.projects.create(
                workspace_id=workspace_id,
                data=data,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    def update_project(  # type: ignore[no-untyped-def]
        self,
        workspace_id: str,
        project_id: str,
        **kwargs,
    ) -> dict[str, Any] | None:
        """Update an existing project."""
        try:
            result = self.client.projects.update(
                workspace_id=workspace_id,
                project_id=project_id,
                data=kwargs,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    # ==================== Work Item (Issue) Methods ====================

    def get_work_item(
        self, workspace_id: str, project_id: str, work_item_id: str
    ) -> dict[str, Any] | None:
        """Get work item (issue) details by ID."""
        try:
            result = self.client.work_items.retrieve(
                workspace_id=workspace_id,
                project_id=project_id,
                identifier=work_item_id,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    def list_work_items(
        self,
        workspace_id: str,
        project_id: str,
        page: int = 1,
        limit: int = 20,
        **filters,
    ) -> list[dict[str, Any]]:
        """
        List work items (issues) with optional filters.

        Args:
            workspace_id: Workspace ID
            project_id: Project ID
            page: Page number
            limit: Results per page
            **filters: Additional filters (state, assignee, labels, etc.)
        """
        try:
            # Convert filters to query params
            params = {
                "page": page,
                "limit": limit,
                **filters,
            }

            result = self.client.work_items.list(
                workspace_id=workspace_id,
                project_id=project_id,
                **params,
            )
            return [w.model_dump() for w in result] if result else []
        except Exception:
            return []

    def create_work_item(
        self,
        workspace_id: str,
        project_id: str,
        title: str,
        description: str | None = None,
        state: str | None = None,
        assignee: str | None = None,
        labels: list[str] | None = None,
        type: str | None = "issue",  # issue, task, bug, etc.
    ) -> dict[str, Any] | None:
        """Create a new work item (issue)."""
        try:
            data = {
                "name": title,  # Field name is 'name' in Plane
                "type": type or "issue",
            }

            if description:
                data["description_html"] = description  # HTML format expected

            if state:
                data["state"] = state

            if assignee:
                data["assignees"] = [assignee]  # type: ignore[assignment]  # type: ignore[assignment]

            if labels:
                data["labels"] = labels  # type: ignore[assignment]  # type: ignore[assignment]

            result = self.client.work_items.create(
                workspace_id=workspace_id,
                project_id=project_id,
                data=data,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    def update_work_item(
        self,
        workspace_id: str,
        project_id: str,
        work_item_id: str,
        **kwargs,
    ) -> dict[str, Any] | None:
        """Update an existing work item."""
        try:
            result = self.client.work_items.update(
                workspace_id=workspace_id,
                project_id=project_id,
                identifier=work_item_id,
                data=kwargs,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    def delete_work_item(
        self, workspace_id: str, project_id: str, work_item_id: str
    ) -> bool:
        """Delete a work item."""
        try:
            self.client.work_items.delete(
                workspace_id=workspace_id,
                project_id=project_id,
                identifier=work_item_id,
            )
            return True
        except Exception:
            return False

    # ==================== Cycle Methods ====================

    def get_cycle(
        self, workspace_id: str, project_id: str, cycle_id: str
    ) -> dict[str, Any] | None:
        """Get cycle details."""
        try:
            result = self.client.cycles.retrieve(
                workspace_id=workspace_id,
                project_id=project_id,
                cycle_id=cycle_id,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    def list_cycles(
        self, workspace_id: str, project_id: str, page: int = 1, limit: int = 20
    ) -> list[dict[str, Any]]:
        """List cycles in a project."""
        try:
            result = self.client.cycles.list(
                workspace_id=workspace_id,
                project_id=project_id,
                page=page,
                limit=limit,
            )
            return [c.model_dump() for c in result] if result else []
        except Exception:
            return []

    def create_cycle(  # type: ignore[no-untyped-def]
        self,
        workspace_id: str,
        project_id: str,
        name: str,
        start_date: str | None = None,
        end_date: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any] | None:
        """Create a new cycle."""
        try:
            data = {"name": name}
            if start_date:
                data["start_date"] = start_date
            if end_date:
                data["end_date"] = end_date
            if description:
                data["description_html"] = description

            result = self.client.cycles.create(
                workspace_id=workspace_id,
                project_id=project_id,
                data=data,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    def update_cycle(  # type: ignore[assignment]  # type: ignore[assignment]
        self,
        workspace_id: str,  # type: ignore[assignment]  # type: ignore[assignment]
        project_id: str,
        cycle_id: str,
        **kwargs,
    ) -> dict[str, Any] | None:
        """Update an existing cycle."""
        try:
            result = self.client.cycles.update(
                workspace_id=workspace_id,
                project_id=project_id,
                cycle_id=cycle_id,
                data=kwargs,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    # ==================== Module Methods ====================

    def get_module(
        self, workspace_id: str, project_id: str, module_id: str
    ) -> dict[str, Any] | None:
        """Get module details."""
        try:
            result = self.client.modules.retrieve(
                workspace_id=workspace_id,
                project_id=project_id,
                module_id=module_id,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    def list_modules(
        self, workspace_id: str, project_id: str, page: int = 1, limit: int = 20
    ) -> list[dict[str, Any]]:
        """List modules in a project."""
        try:
            result = self.client.modules.list(
                workspace_id=workspace_id,
                project_id=project_id,
                page=page,
                limit=limit,
            )
            return [m.model_dump() for m in result] if result else []
        except Exception:
            return []

    # ==================== Page Methods ====================

    def get_page(self, workspace_id: str, page_id: str) -> dict[str, Any] | None:
        """Get page details."""
        try:
            result = self.client.pages.retrieve(
                workspace_id=workspace_id,
                page_id=page_id,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    def list_pages(
        self, workspace_id: str, page: int = 1, limit: int = 20
    ) -> list[dict[str, Any]]:
        """List pages in a workspace."""
        try:
            result = self.client.pages.list(
                workspace_id=workspace_id,
                page=page,
                limit=limit,
            )
            return [p.model_dump() for p in result] if result else []
        except Exception:
            return []

    def create_page(
        self,
        workspace_id: str,
        title: str,
        content: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any] | None:
        """Create a new page."""
        try:
            data = {"name": title}
            if description:
                data["description_html"] = description
            if content:
                data["content_html"] = content

            result = self.client.pages.create(
                workspace_id=workspace_id,
                data=data,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    def update_page(  # type: ignore[no-untyped-def]
        self,
        workspace_id: str,
        page_id: str,
        **kwargs,
    ) -> dict[str, Any] | None:
        """Update an existing page."""
        try:
            result = self.client.pages.update(
                workspace_id=workspace_id,
                page_id=page_id,
                data=kwargs,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    # ==================== State Methods ====================

    def list_states(self, workspace_id: str, project_id: str) -> list[dict[str, Any]]:
        """List all states for a project."""
        try:
            result = self.client.states.list(
                workspace_id=workspace_id,
                project_id=project_id,
            )
            return [s.model_dump() for s in result] if result else []
        except Exception:
            return []

    # ==================== Member/User Methods ====================

    def get_member(self, workspace_id: str, member_id: str) -> dict[str, Any] | None:
        """Get member details."""
        try:
            result = self.client.users.retrieve(user_id=member_id)
            return result.model_dump() if result else None
        except Exception:
            return None

    def list_members(
        self, workspace_id: str, page: int = 1, limit: int = 20
    ) -> list[dict[str, Any]]:
        """List members in a workspace."""
        try:
            result = self.client.users.list(
                workspace_id=workspace_id,
                page=page,
                limit=limit,
            )
            return [u.model_dump() for u in result] if result else []
        except Exception:
            return []

    # ==================== Search Methods ====================

    def search_work_items(  # type: ignore[no-untyped-def]
        self,
        workspace_id: str,
        project_id: str,
        query: str,
        page: int = 1,
        limit: int = 20,
        **filters,
    ) -> list[dict[str, Any]]:
        """
        Search work items using text search.

        Note: Uses advanced_search for full-text search capabilities.
        """
        try:
            result = self.client.work_items.advanced_search(
                workspace_id=workspace_id,
                project_id=project_id,
                query=query,
                page=page,
                limit=limit,
                **filters,
            )
            return [w.model_dump() for w in result] if result else []
        except Exception:
            return []

    # ==================== Label Methods ====================

    def list_labels(self, workspace_id: str, project_id: str) -> list[dict[str, Any]]:
        """List all labels in a project."""
        try:
            result = self.client.labels.list(
                workspace_id=workspace_id,
                project_id=project_id,
            )
            return [label.model_dump() for label in result] if result else []
        except Exception:
            return []

    # ==================== Utility Methods ====================

    def get_workspace_members(self, workspace_id: str) -> list[dict[str, Any]]:
        """Get members of a workspace."""
        try:
            result = self.client.teamspaces.get_members(
                id=workspace_id,
            )
            return [m.model_dump() for m in result] if result else []
        except Exception:
            return []

    def get_project_members(
        self, workspace_id: str, project_id: str
    ) -> list[dict[str, Any]]:
        """Get members of a project."""
        try:
            result = self.client.projects.get_members(
                workspace_id=workspace_id,
                project_id=project_id,
            )
            return [m.model_dump() for m in result] if result else []
        except Exception:
            return []

    def get_project_features(
        self, workspace_id: str, project_id: str
    ) -> dict[str, Any] | None:
        """Get project features/configuration."""
        try:
            result = self.client.projects.get_features(
                workspace_id=workspace_id,
                project_id=project_id,
            )
            return result.model_dump() if result else None
        except Exception:
            return None

    def update_issue_state(
        self,
        workspace_id: str,
        project_id: str,
        work_item_id: str,
        state: str,
    ) -> dict[str, Any] | None:
        """Update the state of a work item."""
        return self.update_work_item(
            workspace_id=workspace_id,
            project_id=project_id,
            work_item_id=work_item_id,
            state=state,
        )
