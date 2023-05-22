from fastapi import APIRouter

from .models import Temp
from .services import TempCommandService, TempQueryService

router = APIRouter(prefix="/temps", tags=["Temp"])


@router.get("/{id}")
async def get_by_id(id: int) -> Temp:
    querier = TempQueryService()
    return await querier.get_by_id(id=id)


@router.get("/or-none/{id}")
async def get_or_null(id: int) -> Temp | None:
    querier = TempQueryService()
    return await querier.get_or_none(id=id)


@router.post("/")
async def create(name: str) -> Temp:
    commander = TempCommandService()
    return await commander.create(name=name)
