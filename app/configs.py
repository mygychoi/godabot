import tomllib
from enum import Enum
from typing import Any

from pydantic import BaseSettings, Extra, PostgresDsn
from pydantic.env_settings import SettingsSourceCallable


class Environment(str, Enum):
    DEV = "development"
    STAGING = "staging"
    PROD = "production"


def pyproject_settings(setting: BaseSettings) -> dict[str, Any]:  # noqa
    with open("pyproject.toml", mode="rb") as pyproject:
        project_table: dict[str, Any] = tomllib.load(pyproject)["project"]
        return {key.upper(): value for key, value in project_table.items()}


class Settings(BaseSettings):
    ENVIRONMENT: Environment = Environment.DEV

    # Database
    DATABASE_URL: PostgresDsn

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_ORGANIZATION: str

    # Slack
    SLACK_CLIENT_ID: str
    SLACK_CLIENT_SECRET: str
    SLACK_SIGNING_SECRET: str
    SLACK_API_APP_ID: str

    # Project
    NAME: str
    VERSION: str
    DESCRIPTION: str
    AUTHORS: list[dict[str, str | Any]]
    LICENSE: str

    class Config:
        env_file = ".env"
        frozen = True
        extra = Extra.ignore

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings, file_secret_settings, pyproject_settings

    @property
    def DEBUG(self) -> bool:  # noqa
        return self.ENVIRONMENT == Environment.DEV


settings = Settings()  # pyright: ignore
