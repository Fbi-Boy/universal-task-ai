from backend.tools.calculator import CalculatorTool


def test_calculator_addition() -> None:
    result = CalculatorTool().run({"expression": "10 + 5 * 2"})
    assert result.success
    assert result.output == 20


def test_calculator_rejects_calls() -> None:
    result = CalculatorTool().run({"expression": "__import__('os').system('id')"})
    assert not result.success


def test_calculator_rejects_names() -> None:
    result = CalculatorTool().run({"expression": "secret_value + 1"})
    assert not result.success


def test_calculator_rejects_empty_expression() -> None:
    result = CalculatorTool().run({})
    assert not result.success


def test_calculator_division_by_zero() -> None:
    result = CalculatorTool().run({"expression": "1 / 0"})
    assert not result.success
