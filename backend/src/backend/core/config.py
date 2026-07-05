from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from typing import ClassVar


class Settings(BaseSettings):
    BASE_DIR: ClassVar[Path] = Path(__file__).resolve().parents[4]
    model_config = SettingsConfigDict(
        env_nested_delimiter=".",
        env_nested_max_split=3,
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        frozen=True,
    )

    app_name: str
    app_env: str

    api_host: str
    api_port: int

    database_url: str
    redis_url: str

    llm_api_key: str

    amd_credit_status: str
    amd_runtime_mode: str
