from dataclasses import dataclass
from pathlib import Path
from backend.core.workspace_policy import WorkspaceDenied, WorkspacePolicy

@dataclass(frozen=True)
class ProjectFile:
    path: str
    content: str
    bytes: int

@dataclass(frozen=True)
class ProjectContext:
    root: str
    files: tuple[ProjectFile, ...]

class ProjectContextReader:
    def __init__(self, policy: WorkspacePolicy) -> None:
        self._policy = policy

    def collect(self, relative_paths: tuple[str, ...] = ()) -> ProjectContext:
        if len(relative_paths) > self._policy.max_files:
            raise ValueError("too many requested project files")
        files: list[ProjectFile] = []
        candidates = [self._policy.resolve_relative(path) for path in relative_paths] if relative_paths else self._discover()
        for path in candidates[: self._policy.max_files]:
            if not self._policy.is_allowed_file(path):
                continue
            try:
                size = path.stat().st_size
                if size > self._policy.max_file_bytes:
                    continue
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                raise WorkspaceDenied("project file could not be read safely") from exc
            files.append(ProjectFile(self._display_path(path), content, size))
        return ProjectContext(str(self._policy.roots[0]), tuple(files))

    def _discover(self) -> list[Path]:
        root = self._policy.roots[0]
        found: list[Path] = []
        for path in sorted(root.rglob("*")):
            if any(part in self._policy.ignored_dirs for part in path.parts):
                continue
            if path.is_symlink():
                continue
            if self._policy.is_allowed_file(path):
                found.append(path)
            if len(found) >= self._policy.max_files:
                break
        return found

    def _display_path(self, path: Path) -> str:
        for root in self._policy.roots:
            try:
                return path.relative_to(root).as_posix()
            except ValueError:
                continue
        raise WorkspaceDenied("project file is outside configured workspace roots")
