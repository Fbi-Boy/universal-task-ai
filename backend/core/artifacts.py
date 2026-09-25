from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path


@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    path: Path
    sha256: str
    size: int


class ArtifactStore:
    """Store artifacts beneath one trusted root with content-addressed IDs."""

    def __init__(self, root: Path, *, max_size_bytes: int = 50 * 1024 * 1024) -> None:
        if max_size_bytes < 1:
            raise ValueError("max_size_bytes must be positive")
        self._root = root.resolve()
        self._root.mkdir(parents=True, exist_ok=True)
        self._max_size = max_size_bytes

    def put(self, name: str, content: bytes) -> Artifact:
        if not name or Path(name).name != name:
            raise ValueError("artifact name must be a single filename")
        if len(content) > self._max_size:
            raise ValueError("artifact exceeds configured size limit")
        digest = sha256(content).hexdigest()
        target = (self._root / f"{digest}-{name}").resolve()
        target.relative_to(self._root)
        target.write_bytes(content)
        return Artifact(digest, target, digest, len(content))

    def get(self, artifact: Artifact) -> bytes:
        candidate = artifact.path.resolve()
        candidate.relative_to(self._root)
        if not candidate.is_file() or candidate.is_symlink():
            raise FileNotFoundError("artifact is not an allowed regular file")
        content = candidate.read_bytes()
        if len(content) > self._max_size or sha256(content).hexdigest() != artifact.sha256:
            raise ValueError("artifact integrity check failed")
        return content
