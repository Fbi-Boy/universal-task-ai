import re

from backend.core.requirements import Requirement, RequirementSet

_BULLET_RE = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+(.+?)\s*$")

def extract_requirements(task_text: str) -> RequirementSet:
    """Extract explicit list-like requirements without asking an LLM to invent facts.

    This is intentionally conservative: free-form prose remains a single explicit
    requirement instead of being silently split into assumptions.
    """
    text = task_text.strip()
    if not text:
        raise ValueError("task_text must not be empty")

    matches = [match.group(1) for line in text.splitlines() if (match := _BULLET_RE.match(line))]
    if not matches:
        matches = [text]

    requirements = [
        Requirement(
            key=f"req_{index}",
            description=value,
            source="explicit",
            priority="must",
        )
        for index, value in enumerate(matches, start=1)
    ]
    return RequirementSet(items=requirements)
