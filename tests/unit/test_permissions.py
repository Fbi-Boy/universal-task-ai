import pytest

from backend.core.permissions import PermissionDenied, ToolPermission, authorize_tool

def test_tool_must_be_explicitly_allowed():
    with pytest.raises(PermissionDenied):
        authorize_tool(ToolPermission(frozenset()), "shell")

def test_network_is_denied_by_default():
    permissions = ToolPermission(frozenset({"web"}))
    with pytest.raises(PermissionDenied):
        authorize_tool(permissions, "web", needs_network=True)

def test_explicit_capabilities_are_allowed():
    permissions = ToolPermission(
        frozenset({"web"}),
        allow_network=True,
    )
    authorize_tool(permissions, "web", needs_network=True)
