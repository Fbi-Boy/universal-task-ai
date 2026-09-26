from dataclasses import dataclass
from pathlib import PurePosixPath

@dataclass(frozen=True)
class DownloadPolicy:
    max_bytes: int = 20_000_000
    allowed_extensions: frozenset[str] = frozenset({".pdf",".csv",".xlsx",".txt",".png",".jpg",".zip"})
    def validate(self,filename:str,size:int):
        if size<0 or size>self.max_bytes: raise PermissionError("download exceeds size limit")
        p=PurePosixPath(filename)
        if p.name!=filename or p.suffix.lower() not in self.allowed_extensions: raise PermissionError("download type/path rejected")
        return True
