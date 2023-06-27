import pytest

from app.configs import settings
from app.slashcommand import SlachcommandChannelInput, SlashcommandLunchRouletteService
from tests.configs import test_settings
from tests.test_core.test_database import with_pool


@pytest.fixture
def input_variables() -> dict:
    return {
        "command": SlachcommandChannelInput.Command.LUNCH,
        "team_id": test_settings.TEST_TEAM_ID,
        "team_domain": "godabot.com",
        "user_id": "U04P352MLQM",
        "user_name": "Goda Choe",
        "channel_id": test_settings.TEST_CHANNEL_ID,
        "channel_name": test_settings.TEST_CHANNEL_NAME,
        "response_url": "https://godabot.com",
        "api_app_id": settings.SLACK_API_APP_ID,
    }


@with_pool
@pytest.mark.asyncio
async def test_roulette_open(input_variables: dict):
    servicer = SlashcommandLunchRouletteService()
    await servicer.open_roulette(input=SlachcommandChannelInput(text="--open", **input_variables))


@with_pool
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, user_name, preference",
    [
        (test_settings.TEST_USER_ID, test_settings.TEST_USER_NAME, "I'd like to eat pizza"),
        ("wanseo_id", "wanseo", "I love pizza"),
        ("matthew_id", "matthew", "Prefer american pizza"),
        ("dohyun_id", "dohyun", "I want to go italian restaurant"),
        ("stephen_id", "stephen", "Anything whatever you liket"),
    ],
)
async def test_attendance_create(
    user_id: str, user_name: str, preference: str, input_variables: dict
):
    input_variables.update(user_id=user_id, user_name=user_name, text=preference)
    servicer = SlashcommandLunchRouletteService()
    await servicer.join_roulette(input=SlachcommandChannelInput(**input_variables))


@with_pool
@pytest.mark.asyncio
async def test_roulette_spin(input_variables: dict):
    servicer = SlashcommandLunchRouletteService()
    await servicer.spin_roulette_until_success(
        input=SlachcommandChannelInput(text="--open", **input_variables)
    )


@with_pool
@pytest.mark.asyncio
async def test_roulette_cancel(input_variables):
    servicer = SlashcommandLunchRouletteService()
    await servicer.cancel_roulette(
        input=SlachcommandChannelInput(text="--cancel", **input_variables)
    )
