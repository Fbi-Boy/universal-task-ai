"""Deterministic routing for explicitly requested, bounded low-risk tasks."""

from __future__ import annotations

import re
from collections.abc import Collection

from backend.core.tool_invocation import ToolInvocation


class SafeCalculatorIntentRouter:
    """Route only explicit, simple arithmetic requests to the calculator tool."""

    def route(self, task_text: str) -> ToolInvocation | None:
        if not isinstance(task_text, str) or not task_text or len(task_text) > _MAX_TASK_LENGTH:
            return None

        match = _CALCULATOR_PREFIX.fullmatch(task_text)
        if match is None:
            return None

        expression = match.group(1).strip()
        if expression.endswith("?"):
            expression = expression[:-1].strip()
        if (
            not expression
            or len(expression) > _MAX_EXPRESSION_LENGTH
            or not _ALLOWED_EXPRESSION.fullmatch(expression)
            or not any(character.isdigit() for character in expression)
            or not any(operator in expression for operator in "+-*/")
        ):
            return None

        return ToolInvocation(
            tool_name="calculator",
            arguments={"expression": expression},
        )


class SafeTaskIntentRouter:
    """Route only narrow explicit intents; never infer authority from vague tasks.

    Local file reads are routed only when the user explicitly names a relative
    path and the filesystem read tool is already enabled by runtime configuration.
    The local capability broker remains responsible for root containment and reads.
    """

    def __init__(self, calculator_router: SafeCalculatorIntentRouter | None = None) -> None:
        self._calculator = calculator_router or SafeCalculatorIntentRouter()

    def route(
        self,
        task_text: str,
        *,
        available_tools: Collection[str] = (),
    ) -> ToolInvocation | None:
        calculator = self._calculator.route(task_text)
        if calculator is not None:
            return calculator

        if (
            not isinstance(task_text, str)
            or not task_text
            or len(task_text) > _MAX_TASK_LENGTH
            or "filesystem.read_text" not in available_tools
        ):
            return None

        match = _LOCAL_READ_PREFIX.fullmatch(task_text)
        if match is None:
            return None

        path = match.group(1).strip()
        if not _is_safe_relative_path(path):
            return None

        return ToolInvocation(
            tool_name="filesystem.read_text",
            arguments={"path": path},
        )


def _is_safe_relative_path(path: str) -> bool:
    if not path or len(path) > _MAX_LOCAL_PATH_LENGTH or "\x00" in path:
        return False
    if path.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", path):
        return False
    if any(ord(character) < 32 for character in path):
        return False
    if re.search(r"[/\\]{2,}", path):
        return False
    segments = re.split(r"[/\\]+", path)
    return all(segment not in {"", ".", ".."} for segment in segments)


_MAX_TASK_LENGTH = 600
_MAX_EXPRESSION_LENGTH = 500
_MAX_LOCAL_PATH_LENGTH = 1024
_CALCULATOR_PREFIX = re.compile(
    r"^\s*(?:hitung(?:kan)?|calculate|calc|berapa\s+hasil(?:\s+dari)?|what\s+is)"
    r"\s*[:,]?\s*(.+?)\s*$",
    re.IGNORECASE,
)
_ALLOWED_EXPRESSION = re.compile(r"[0-9\s()+\-*/.]+\Z")
_LOCAL_READ_PREFIX = re.compile(
    r"^\s*(?:read\s+(?:a\s+)?local\s+file|read\s+file|baca\s+file(?:\s+lokal)?)"
    r"\s*[:,]\s*(.+?)\s*$",
    re.IGNORECASE,
)
