"""Deterministic, narrow intent routing for low-risk arithmetic only."""

from __future__ import annotations

import re

from backend.core.tool_invocation import ToolInvocation

_MAX_TASK_LENGTH = 600
_MAX_EXPRESSION_LENGTH = 500
_PREFIX = re.compile(
    r"^\s*(?:hitung(?:kan)?|calculate|calc|berapa\s+hasil(?:\s+dari)?|what\s+is)"
    r"\s*[:,-]?\s*(.+?)\s*$",
    re.IGNORECASE,
)
_ALLOWED_EXPRESSION = re.compile(r"[0-9\s()+\-*/.]+\Z")


class SafeCalculatorIntentRouter:
    """Route only explicit, simple arithmetic requests to the calculator tool.

    This router does not infer browser, filesystem, network, or process actions.
    Any task outside the narrow expression grammar remains on the safe baseline
    unless the user explicitly chooses a registered tool in the UI/API.
    """

    def route(self, task_text: str) -> ToolInvocation | None:
        if not isinstance(task_text, str) or not task_text or len(task_text) > _MAX_TASK_LENGTH:
            return None

        match = _PREFIX.fullmatch(task_text)
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
