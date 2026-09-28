from backend.core.analyzer import TaskAnalysis
from backend.core.intent_router import SafeCalculatorIntentRouter
from backend.core.planner import ExecutionPlan
from backend.core.run_lifecycle import RunStatus
from backend.core.schemas import TaskContract
from backend.core.task_executor import ExecutionResult
from backend.core.task_intake import TaskIntakeService
from backend.core.task_planner import TaskPlanner
from backend.core.task_service import TaskService
from backend.core.tool_invocation import ToolInvocation
from backend.tools.calculator import CalculatorTool


def test_routes_explicit_indonesian_and_english_arithmetic():
    router = SafeCalculatorIntentRouter()
    cases = [
        ("Hitung: 12 * (3 + 1)", "12 * (3 + 1)"),
        ("Calculate 2 ** 3", "2 ** 3"),
        ("Berapa hasil dari 14 / 2?", "14 / 2"),
        ("What is 9 - 4?", "9 - 4"),
    ]
    for text, expected in cases:
        invocation = router.route(text)
        assert invocation is not None
        assert invocation.tool_name == "calculator"
        assert invocation.arguments == {"expression": expected}


def test_router_rejects_general_or_non_arithmetic_requests():
    router = SafeCalculatorIntentRouter()
    cases = [
        "What is your name?",
        "Calculate __import__('os').system('id')",
        "Hitung 10 + open('/etc/passwd')",
        "Calculate 1000,000 + 1",
        "Please calculate this for me: 1 + 1",
        "Browse example.com",
        "Read a local file: notes.txt",
    ]
    for text in cases:
        assert router.route(text) is None


def test_router_bounds_task_and_expression_length():
    router = SafeCalculatorIntentRouter()
    assert router.route("Calculate " + "1" * 700) is None
    assert router.route("Calculate " + "1" * 501) is None


def test_routed_expression_uses_the_existing_safe_calculator():
    invocation = SafeCalculatorIntentRouter().route("Hitung: 12 * (3 + 1)")
    assert invocation is not None
    result = CalculatorTool().run(invocation.arguments)
    assert result.success is True
    assert result.output == 48


class CapturingExecutor:
    def __init__(self):
        self.invocations = ()
        self.contract = None

    @property
    def tool_catalog(self):
        return ()

    @property
    def approval_store(self):
        return None

    def execute(self, contract, plan, *, tool_invocations=()):
        self.contract = contract
        self.invocations = tool_invocations
        return ExecutionResult("test-run", RunStatus.SUCCEEDED, "ok", plan)


def test_task_service_auto_routes_only_when_enabled():
    executor = CapturingExecutor()
    service = TaskService(TaskIntakeService(), TaskPlanner(), executor)

    service.run("Calculate: 8 * 7")

    assert len(executor.invocations) == 1
    assert executor.invocations[0].tool_name == "calculator"
    assert executor.invocations[0].arguments == {"expression": "8 * 7"}
    assert executor.contract.tools_required == ["calculator"]


def test_task_service_can_disable_auto_routing_and_respects_explicit_tools():
    executor = CapturingExecutor()
    service = TaskService(TaskIntakeService(), TaskPlanner(), executor)

    service.run("Calculate: 8 * 7", auto_route_tools=False)
    assert executor.invocations == ()

    explicit = ToolInvocation(tool_name="calculator", arguments={"expression": "3 + 4"})
    service.run("Calculate: 8 * 7", tool_invocations=(explicit,))
    assert executor.invocations == (explicit,)
