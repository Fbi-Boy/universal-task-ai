import pytest

from backend.core.run_lifecycle import RunStatus, transition


def test_run_lifecycle() -> None:
    state = transition(RunStatus.CREATED, RunStatus.RUNNING)
    state = transition(state, RunStatus.WAITING_APPROVAL)
    state = transition(state, RunStatus.RUNNING)
    assert transition(state, RunStatus.SUCCEEDED) is RunStatus.SUCCEEDED


def test_terminal_state_cannot_resume() -> None:
    with pytest.raises(ValueError):
        transition(RunStatus.SUCCEEDED, RunStatus.RUNNING)
