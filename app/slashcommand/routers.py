from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Response

from .schemas import SlashcommandForm
from .services import SlashcommandQueryService, SlashcommandService

SlashcommandFormDep = Annotated[SlashcommandForm, Depends(SlashcommandForm)]

router = APIRouter(prefix="/slashcommands", tags=["Slachcommand"])


@router.post("/echo")
async def echo(form: SlashcommandFormDep) -> Response:
    querier = SlashcommandQueryService()
    await querier.echo(form=form)
    return Response(status_code=204)


@router.post("/chat")
async def chat(form: SlashcommandFormDep, background_tasks: BackgroundTasks) -> Response:
    commander = SlashcommandService()
    background_tasks.add_task(commander.chat, form=form)
    return Response(status_code=200, content="Thanks! Please wait for a second...")


@router.post("/draw")
async def draw(form: SlashcommandFormDep, background_tasks: BackgroundTasks) -> Response:
    commander = SlashcommandService()
    background_tasks.add_task(commander.draw, form=form)
    return Response(
        status_code=200,
        content="Thanks! I am drawing now, Please wait for a second...",
    )
