from typing import Annotated, Any

from fastapi import Depends

from .clients import AccessClient
from .repositories import AccessCommandRepository
from .services import AccessCommandService, AccessQueryRepository, AccessQueryService

AccessQuerier = Annotated[AccessQueryService, Depends(AccessQueryRepository)]


def access_commander(querier: AccessQuerier) -> dict[str, Any]:
    return {"querier": querier, "repository": AccessCommandRepository(), "client": AccessClient()}


AccessCommander = Annotated[AccessCommandService, Depends(access_commander)]
