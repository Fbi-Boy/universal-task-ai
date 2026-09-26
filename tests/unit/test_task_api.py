from backend.api.main import TaskRequest, run_task

def test_run_task_endpoint_executes_safe_baseline():
    result = run_task(TaskRequest(task="Create a report"))
    assert result.status == "succeeded"
    assert result.run_id
    assert result.plan_id
    assert "safe baseline runtime" in result.output