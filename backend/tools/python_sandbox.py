from typing import Any, Mapping

from backend.core.sandbox import DockerSandbox, SandboxError
from backend.core.tools import Tool, ToolMetadata, ToolResult


class PythonSandboxTool(Tool):
    metadata = ToolMetadata(
        name="python_sandbox",
        description="Execute a bounded Python snippet inside the Docker sandbox",
        risk_level="high",
        requires_approval=True,
        requires_network=False,
    )

    def __init__(self, sandbox: DockerSandbox, *, max_code_bytes: int = 20_000, max_output_bytes: int = 100_000) -> None:
        if max_code_bytes < 1 or max_code_bytes > 100_000:
            raise ValueError("max_code_bytes must be between 1 and 100000")
        if max_output_bytes < 1 or max_output_bytes > 1_000_000:
            raise ValueError("max_output_bytes must be between 1 and 1000000")
        self._sandbox = sandbox
        self._max_code_bytes = max_code_bytes
        self._max_output_bytes = max_output_bytes

    def run(self, arguments: Mapping[str, Any]) -> ToolResult:
        code = arguments.get("code")
        if not isinstance(code, str) or not code.strip():
            return ToolResult(success=False, error="code must be a non-empty string")
        if len(code.encode("utf-8")) > self._max_code_bytes:
            return ToolResult(success=False, error="code exceeds configured size limit")
        try:
            result = self._sandbox.run(["python", "-I", "-B", "-c", code])
        except SandboxError as exc:
            return ToolResult(success=False, error=str(exc))
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        if len(stdout.encode("utf-8")) > self._max_output_bytes or len(stderr.encode("utf-8")) > self._max_output_bytes:
            return ToolResult(success=False, error="sandbox output exceeds configured size limit")
        if result.returncode != 0:
            return ToolResult(success=False, error=stderr[-self._max_output_bytes:] or f"python exited with code {result.returncode}")
        return ToolResult(success=True, output=stdout)
