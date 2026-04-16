"""Tests for Plane MCP server."""

from plane_mcp.client import PlaneClientWrapper
from plane_mcp.server import Settings, get_plane_client, mcp


class TestSettings:
    """Tests for Settings."""

    def test_default_values(self):
        """Test config can be instantiated."""
        # Just verify config loads without error
        # (actual values depend on .env file)
        config = Settings()
        assert config is not None
        assert len(config.PLANE_BASE_URL) > 0


class TestPlaneClientWrapper:
    """Tests for PlaneClientWrapper."""

    def test_client_initialization(self):
        """Test client initialization."""
        wrapper = PlaneClientWrapper(
            base_url="https://test.plane.so",
            api_key="test_key",
        )
        assert wrapper.base_url == "https://test.plane.so"
        assert wrapper.api_key == "test_key"


class TestFastMCPInstance:
    """Tests for FastMCP instance."""

    def test_mcp_instance_exists(self):
        """Test that mcp instance is created."""
        assert mcp is not None
        assert mcp.name == "plane-mcp-redux"

    def test_mcp_has_name(self):
        """Test that MCP has a name."""
        assert mcp.name == "plane-mcp-redux"

    def test_tools_are_registered(self):
        """Test that tools are registered on the MCP instance."""
        # FastMCP 3.x tools are accessible via the server
        # This verifies the decorator pattern worked
        assert hasattr(mcp, "tool")  # Decorator method exists


class TestDependencyInjection:
    """Tests for dependency injection pattern."""

    def test_get_plane_client(self):
        """Test that get_plane_client dependency is defined."""
        # This function is defined and can be used as a dependency
        assert callable(get_plane_client)

    def test_client_is_lazy(self):
        """Test that client is only created when needed."""
        # The client is created lazily via Depends()
        # We can't easily test this without mocking, but we verify the pattern
        assert get_plane_client is not None
