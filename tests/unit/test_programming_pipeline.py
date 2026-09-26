from backend.core.programming_artifacts import ProgrammingArtifact,ProgrammingTask
from backend.core.programming_pipeline import ProgrammingPipeline

def test_pipeline_validates_outputs():
    t=ProgrammingTask("make code",(ProgrammingArtifact.CODE,))
    p=ProgrammingPipeline(lambda x:x,lambda x:{ProgrammingArtifact.CODE:"print(1)"})
    assert p.run(t).checks[0].passed
