from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from backend.core.settings import SettingsStore, UserSettings

router = APIRouter(prefix="/v1/settings", tags=["settings"])
store = SettingsStore()
DEFAULT_USER = UUID("00000000-0000-0000-0000-000000000001")


class SettingsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    language: str = Field(default="id", min_length=2, max_length=2)
    theme: str = Field(default="system", min_length=1, max_length=10)
    timezone: str = Field(default="UTC", min_length=1, max_length=64)


@router.get("")
def get_settings() -> UserSettings:
    return store.get(DEFAULT_USER)


@router.put("")
def put_settings(request: SettingsUpdate) -> UserSettings:
    return store.put(UserSettings(user_id=DEFAULT_USER, language=request.language, theme=request.theme, timezone=request.timezone))
