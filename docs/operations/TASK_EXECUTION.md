# Task Execution

The runtime path is intentionally staged:
1. Task text enters `TaskIntakeService`.
2. `TaskPlanner` produces a bounded `ExecutionPlan`.
3. `TaskExecutor` persists lifecycle state before and after execution.
4. The baseline executor performs only side-effect-free stages.

Tasks that require tools or agents are not executed implicitly. Without an approval requirement they fail closed until a registered execution boundary is supplied. With approval required, the run enters `waiting_approval`.

This prevents the first runtime path from becoming an unrestricted shell, browser, filesystem, or network execution surface.
