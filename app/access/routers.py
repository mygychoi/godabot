from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .dependencies import AccessCommander
from .schemas import AccessRequest

router = APIRouter(prefix="/accesses", tags=["Access"])


@router.get("/activate")
async def activate(request: AccessRequest, commander: AccessCommander) -> RedirectResponse:
    access = await commander.activate(request=request)
    return RedirectResponse(f"https://app.slack.com/client/{access.team_id}")


@router.get("/deactivate", deprecated=True)  # TODO: Research webhook request spec
async def deactivate_access(team_id: str, commander: AccessCommander) -> RedirectResponse:
    access = await commander.deactivate(team_id=team_id)
    return RedirectResponse(f"https://app.slack.com/client/{access.team_id}")
