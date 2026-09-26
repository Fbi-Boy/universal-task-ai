from pathlib import Path

class LocalReadScope:
    def __init__(self, root: str, max_bytes=1_000_000):
        self.root = Path(root).resolve()
        self.max_bytes = max_bytes

    def _resolve(self, relative: str):
        if "\x00" in relative:
            raise ValueError("NUL byte rejected")
        target = (self.root / relative).resolve()
        if target != self.root and self.root not in target.parents:
            raise PermissionError("path escapes scope")
        if target.is_symlink():
            raise PermissionError("symlink access denied")
        return target

    def read_text(self, relative: str):
        target = self._resolve(relative)
        if not target.is_file():
            raise FileNotFoundError(relative)
        size = target.stat().st_size
        if size > self.max_bytes:
            raise ValueError("file exceeds read limit")
        return target.read_text(encoding="utf-8")

    def list_files(self, relative="."):
        target = self._resolve(relative)
        if not target.is_dir():
            raise NotADirectoryError(relative)
        return tuple(
            str(p.relative_to(self.root))
            for p in sorted(target.iterdir())
            if not p.is_symlink()
        )
