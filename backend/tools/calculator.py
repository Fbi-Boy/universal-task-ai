import ast
import operator as op
from typing import Any

from backend.core.tools import Tool, ToolMetadata, ToolResult

_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
}
_ALLOWED_UNARYOPS = {ast.UAdd: op.pos, ast.USub: op.neg}
_MAX_ABS_RESULT = 1e100
_MAX_POW_EXPONENT = 1000


class CalculatorTool(Tool):
    metadata = ToolMetadata(
        name="calculator",
        description="Evaluate a bounded arithmetic expression without shell or network access.",
        risk_level="low",
        requires_network=False,
        requires_approval=False,
    )

    def run(self, arguments: dict[str, Any]) -> ToolResult:
        expression = arguments.get("expression")
        if not isinstance(expression, str) or not expression.strip():
            return ToolResult(success=False, error="expression must be a non-empty string")
        if len(expression) > 500:
            return ToolResult(success=False, error="expression is too long")
        try:
            tree = ast.parse(expression, mode="eval")
            value = self._evaluate(tree.body)
        except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError):
            return ToolResult(success=False, error="invalid or unsafe arithmetic expression")
        return ToolResult(success=True, output=value)

    def _evaluate(self, node: ast.AST) -> float | int:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)
            if isinstance(node.op, ast.Pow):
                if abs(right) > _MAX_POW_EXPONENT:
                    raise ValueError("exponent is too large")
            value = _ALLOWED_BINOPS[type(node.op)](left, right)
            if abs(value) > _MAX_ABS_RESULT:
                raise ValueError("result is too large")
            return value
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARYOPS:
            value = _ALLOWED_UNARYOPS[type(node.op)](self._evaluate(node.operand))
            if abs(value) > _MAX_ABS_RESULT:
                raise ValueError("result is too large")
            return value
        raise ValueError("unsupported expression")
