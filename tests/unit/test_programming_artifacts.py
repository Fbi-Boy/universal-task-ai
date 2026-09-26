import pytest
from backend.core.channel import Channel, InboundMessage
from backend.core.programming_artifacts import ProgrammingArtifact, ProgrammingTask, ReferenceRequest

def test_programming_task_supports_erd_flowchart_research_and_browser():
    task=ProgrammingTask('Design university assignment system',(ProgrammingArtifact.ERD,ProgrammingArtifact.FLOWCHART),(ReferenceRequest('ERD design patterns'),),'https://example.edu')
    assert task.needs_browser and task.needs_research

def test_programming_task_requires_artifact():
    with pytest.raises(ValueError): ProgrammingTask('do programming work')

def test_channel_message_has_identity():
    m=InboundMessage(Channel.WHATSAPP,'wa-user-1','Kerjakan ERD',True)
    assert m.channel is Channel.WHATSAPP
