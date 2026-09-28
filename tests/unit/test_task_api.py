from backend.api.main import TaskRequest, run_task

def test_run_task_endpoint_reports_unsupported_task_honestly():
    result = run_task(TaskRequest(task="Create a report"))
    assert result.status == "needs_tool"
    assert result.run_id
    assert result.plan_id
    assert "was not executed" in result.output