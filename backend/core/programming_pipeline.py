from dataclasses import dataclass
from backend.core.programming_artifacts import ProgrammingTask
from backend.core.artifact_validation import ArtifactValidator

@dataclass(frozen=True)
class ProgrammingResult:
    artifacts: dict
    checks: tuple

class ProgrammingPipeline:
    def __init__(self, planner, executor, validator=None):
        self.planner = planner
        self.executor = executor
        self.validator = validator or ArtifactValidator()

    @staticmethod
    def _invoke(component, method_name, value):
        method = getattr(component, method_name, None)
        return method(value) if callable(method) else component(value)

    def run(self, task: ProgrammingTask):
        plan = self._invoke(self.planner, "plan", task)
        outputs = self._invoke(self.executor, "execute", plan)
        checks = tuple(
            self.validator.validate(a, outputs.get(a, ""))
            for a in task.artifacts
        )
        if any(not c.passed for c in checks):
            raise ValueError("artifact validation failed")
        return ProgrammingResult(outputs, checks)
