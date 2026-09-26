from dataclasses import dataclass
import re

@dataclass(frozen=True)
class FlowchartValidation:
    passed: bool
    issues: tuple[str,...]

class FlowchartValidator:
    def validate(self,text:str)->FlowchartValidation:
        issues=[]
        if not text.strip(): issues.append("flowchart is empty")
        if not re.search(r"(?i)(start|begin)",text): issues.append("missing start marker")
        if not re.search(r"(?i)(end|finish|stop)",text): issues.append("missing end marker")
        if "->" not in text and "→" not in text: issues.append("missing flow transitions")
        return FlowchartValidation(not issues,tuple(issues))
