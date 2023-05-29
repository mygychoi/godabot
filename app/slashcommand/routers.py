import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, Response

from .schemas import SlashcommandInput
from .services import SlashcommandQueryService, SlashcommandService

SlashcommandInputDep = Annotated[SlashcommandInput, Depends(SlashcommandInput)]

router = APIRouter(prefix="/slashcommands", tags=["Slachcommand"])


@router.post("/echo")
async def echo(input: SlashcommandInputDep) -> Response:
    querier = SlashcommandQueryService()
    await querier.echo(input=input)
    return Response(status_code=204)


@router.post("/chat")
async def chat(input: SlashcommandInputDep) -> Response:
    commander = SlashcommandService()
    asyncio.create_task(commander.chat(input=input))
    return Response(status_code=200, content="Thanks! Please wait for a second...")


@router.post("/draw")
async def draw(input: SlashcommandInputDep) -> Response:
    commander = SlashcommandService()
    asyncio.create_task(commander.draw(input=input))
    return Response(
        status_code=200,
        content="Thanks! I am drawing now, Please wait for a second...",
    )
