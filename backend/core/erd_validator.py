import re
from dataclasses import dataclass

@dataclass(frozen=True)
class ERDValidation:
    passed: bool
    issues: tuple[str,...]

class ERDValidator:
    def validate(self,text:str)->ERDValidation:
        issues=[]
        if not text.strip(): issues.append("ERD is empty")
        if not re.search(r"(?i)(entity|table|\bPK\b|\bFK\b)",text): issues.append("no entity/table/key markers found")
        return ERDValidation(not issues,tuple(issues))
