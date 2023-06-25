import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, Response

from .schemas import SlachcommandChannelInput, SlashcommandInput
from .services import (
    SlashcommandEchoService,
    SlashcommandLunchRouletteService,
    SlashcommandService,
)

SlashcommandInputDep = Annotated[SlashcommandInput, Depends(SlashcommandInput)]
SlashcommandChannelInputDep = Annotated[SlachcommandChannelInput, Depends(SlachcommandChannelInput)]

router = APIRouter(prefix="/slashcommands", tags=["Slachcommand"])


@router.post("/echo")
async def echo(input: SlashcommandInputDep) -> Response:
    querier = SlashcommandEchoService()
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


@router.post("/lunch")
async def lunch(input: SlashcommandChannelInputDep):
    servicer = SlashcommandLunchRouletteService()
    match input.text:
        case "--open":
            await servicer.open_roulette(input=input)
            return Response(status_code=204)
        case "--cancel":
            await servicer.cancel_roulette(input=input)
            return Response(status_code=200, content="Roulette is canceled.")
        case "--spin":
            asyncio.create_task(servicer.spin_roulette_until_success(input=input))
            return Response(
                status_code=200,
                content="Thanks! I am spinning the roulette, Please wait for a second...",
            )
        case _:
            await servicer.join_roulette(input=input)
            return Response(status_code=204)
