from unittest.mock import Mock

from backend.core.tools import ToolResult
from backend.tools.python_sandbox import PythonSandboxTool


def test_python_tool_uses_isolated_python_flags() -> None:
    sandbox = Mock()
    sandbox.run.return_value = type("Result", (), {"returncode": 0, "stdout": "2\\n", "stderr": ""})()
    tool = PythonSandboxTool(sandbox)
    result = tool.run({"code": "print(1 + 1)"})
    assert result == ToolResult(success=True, output="2\\n")
    sandbox.run.assert_called_once_with(["python", "-I", "-B", "-c", "print(1 + 1)"])


def test_python_tool_rejects_oversized_code() -> None:
    sandbox = Mock()
    tool = PythonSandboxTool(sandbox, max_code_bytes=4)
    result = tool.run({"code": "12345"})
    assert not result.success
    sandbox.run.assert_not_called()


def test_python_tool_fails_on_nonzero_exit() -> None:
    sandbox = Mock()
    sandbox.run.return_value = type("Result", (), {"returncode": 1, "stdout": "", "stderr": "bad"})()
    result = PythonSandboxTool(sandbox).run({"code": "raise Exception()"})
    assert not result.success
    assert result.error == "bad"
