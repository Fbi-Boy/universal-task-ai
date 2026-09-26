import re
from dataclasses import dataclass

@dataclass(frozen=True)
class ERDStructuralResult:
    passed: bool
    issues: tuple[str,...]

class ERDStructuralValidator:
    def validate(self,text:str)->ERDStructuralResult:
        issues=[]
        lines=[x.strip() for x in text.splitlines() if x.strip()]
        entities=re.findall(r"(?im)^\s*(?:entity|table)\s+([A-Za-z_]\w*)",text)
        if len(set(entities))!=len(entities): issues.append("duplicate entity/table names")
        if not entities: issues.append("no explicit entities/tables")
        if not re.search(r"(?i)\bPK\b",text): issues.append("missing primary key marker")
        if not re.search(r"(?i)\bFK\b",text): issues.append("missing foreign key marker")
        return ERDStructuralResult(not issues,tuple(issues))
