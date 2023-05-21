from fastapi import APIRouter

from .constants import SUCCESS
from .dependencies import SlashcommandServicer
from .schemas import SlashcommandRequest

router = APIRouter(prefix="/slashcommands", tags=["Slachcommand"])


@router.post("/echo")
async def echo(request: SlashcommandRequest, servicer: SlashcommandServicer) -> str:
    await servicer.echo(request=request)
    return SUCCESS


@router.post("/chat")
async def chat(request: SlashcommandRequest, servicer: SlashcommandServicer) -> str:
    await servicer.chat(request=request)
    return SUCCESS
