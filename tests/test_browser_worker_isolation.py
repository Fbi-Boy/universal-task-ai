import pytest

from backend.core.browser_policy import BrowserAction, BrowserPolicy
from backend.tools.browser_worker import BrowserCommand, BrowserWorkerTool


class FakeWorker:
    def __init__(self):
        self.commands = []

    def execute(self, command):
        self.commands.append(command)
        return command.action.value

    def execute_batch(self, commands):
        self.commands.extend(commands)
        return [command.action.value for command in commands]


def policy():
    return BrowserPolicy(frozenset({"example.com"}))


def test_browser_tool_accepts_bounded_batch():
    worker = FakeWorker()
    tool = BrowserWorkerTool(policy(), worker)
    result = tool.run({
        "commands": [
            {"action": "navigate", "url": "https://example.com"},
            {"action": "read"},
        ]
    })
    assert result.success is True
    assert result.output == ["navigate", "read"]
    assert len(worker.commands) == 2


def test_browser_tool_rejects_oversized_batch():
    worker = FakeWorker()
    tool = BrowserWorkerTool(policy(), worker)
    result = tool.run({"commands": [{"action": "read"}] * 9})
    assert result.success is False
    assert "8" in (result.error or "")
    assert worker.commands == []


def test_browser_tool_rejects_unknown_command_fields():
    worker = FakeWorker()
    tool = BrowserWorkerTool(policy(), worker)
    result = tool.run({"commands": [{"action": "read", "unexpected": True}]})
    assert result.success is False
    assert "unknown" in (result.error or "")
    assert worker.commands == []


def test_browser_tool_preserves_single_command_compatibility():
    worker = FakeWorker()
    tool = BrowserWorkerTool(policy(), worker)
    result = tool.run({"action": "read"})
    assert result.success is True
    assert result.output == "read"


def test_browser_command_bounds_value():
    with pytest.raises(ValueError):
        BrowserCommand(
            BrowserAction.TYPE,
            selector="#x",
            value="x" * (64 * 1024 + 1),
        )
