import re
from dataclasses import dataclass

@dataclass(frozen=True)
class FlowchartStructuralResult:
    passed: bool
    issues: tuple[str,...]

class FlowchartStructuralValidator:
    def validate(self,text:str)->FlowchartStructuralResult:
        issues=[]
        nodes=[x.strip() for x in re.split(r"->|→",text) if x.strip()]
        if len(nodes)<2: issues.append("fewer than two connected nodes")
        if nodes and nodes[0].lower() not in {"start","begin"}: issues.append("flow does not start with START")
        if nodes and nodes[-1].lower() not in {"end","finish","stop"}: issues.append("flow does not end with END")
        return FlowchartStructuralResult(not issues,tuple(issues))
