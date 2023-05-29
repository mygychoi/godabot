from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .services import AccessCommandService

router = APIRouter(prefix="/accesses", tags=["Access"])


@router.get("/activate")
async def activate(code: str) -> RedirectResponse:
    commander = AccessCommandService()
    access = await commander.activate(code=code)
    return RedirectResponse(f"https://app.slack.com/client/{access.team_id}")


@router.get("/deactivate", deprecated=True)  # TODO: Research webhook request spec
async def deactivate_access(team_id: str) -> RedirectResponse:
    commander = AccessCommandService()
    access = await commander.deactivate(team_id=team_id)
    return RedirectResponse(f"https://app.slack.com/client/{access.team_id}")
