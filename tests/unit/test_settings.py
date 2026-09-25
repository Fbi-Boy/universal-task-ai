from uuid import uuid4
import pytest
from backend.core.settings import SettingsStore, UserSettings


def test_settings_round_trip() -> None:
    store = SettingsStore(); user = uuid4()
    value = UserSettings(user_id=user, language="en", theme="dark", timezone="Asia/Jakarta")
    assert store.put(value) == value
    assert store.get(user) == value


def test_settings_reject_unknown_values() -> None:
    with pytest.raises(ValueError): UserSettings(user_id=uuid4(), language="fr")
    with pytest.raises(ValueError): UserSettings(user_id=uuid4(), theme="neon")
