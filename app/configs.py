import tomllib
from enum import Enum
from typing import Any

import openai
import sentry_sdk
from pydantic import BaseSettings, Extra, PostgresDsn
from pydantic.env_settings import SettingsSourceCallable
from sentry_sdk.integrations.fastapi import FastApiIntegration


def pyproject_settings(setting: BaseSettings) -> dict[str, Any]:  # noqa
    with open("pyproject.toml", mode="rb") as pyproject:
        project_table: dict[str, Any] = tomllib.load(pyproject)["project"]
        return {key.upper(): value for key, value in project_table.items()}


class Settings(BaseSettings):
    class Environment(str, Enum):
        DEV = "development"
        STAGING = "staging"
        PROD = "production"

    DEV = Environment.DEV
    STAGING = Environment.STAGING
    PROD = Environment.PROD
    ENV: Environment = DEV

    # Database
    DATABASE_URL: PostgresDsn

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_ORGANIZATION: str

    # Stability
    STABILITY_API_KEY: str

    # Slack
    SLACK_CLIENT_ID: str
    SLACK_CLIENT_SECRET: str
    SLACK_SIGNING_SECRET: str
    SLACK_API_APP_ID: str

    # Sentry
    SENTRY_DSN: str

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
        return self.ENV == self.DEV


settings = Settings()  # type: ignore

# OpenAI setups
openai.api_key = settings.OPENAI_API_KEY
openai.organization = settings.OPENAI_ORGANIZATION

# Sentry setups
sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=0.2,
    integrations=[FastApiIntegration(transaction_style="url")],
    environment=settings.ENV.value,
)
