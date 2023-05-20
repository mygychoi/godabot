from fastapi import APIRouter

from .dependencies import TempCommander, TempQuerier
from .models import Temp

router = APIRouter(prefix="/temps", tags=["Temp"])


@router.get("/{id}", response_model=Temp)
async def get_by_id(id: int, querier: TempQuerier) -> Temp:
    return await querier.get_by_id(id=id)


@router.get("/or-none/{id}")
async def get_or_null(id: int, querier: TempQuerier) -> Temp | None:
    return await querier.get_or_none(id=id)


@router.post("/", response_model=Temp)
async def create(name: str, commander: TempCommander) -> Temp:
    return await commander.create(name=name)
