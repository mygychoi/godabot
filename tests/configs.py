from pydantic import BaseSettings, Extra


class TestSettings(BaseSettings):
    TEST_TEAM_ID: str
    TEST_TEAM_NAME: str
    TEST_CHANNEL_ID: str
    TEST_CHANNEL_NAME: str
    TEST_USER_ID: str
    TEST_USER_NAME: str

    class Config:
        env_file = ".test.env"
        frozen = True
        extra = Extra.ignore


test_settings = TestSettings()  # type: ignore
