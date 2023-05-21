from typing import Annotated

from fastapi import Depends

from .clients import AccessClient
from .repositories import AccessCommandRepository
from .services import AccessCommandService, AccessQueryRepository, AccessQueryService

AccessQuerier = Annotated[AccessQueryService, Depends(AccessQueryRepository)]


def access_commander(querier: AccessQuerier) -> AccessCommandService:
    return AccessCommandService(
        repository=AccessCommandRepository(), querier=querier, client=AccessClient()
    )


AccessCommander = Annotated[AccessCommandService, Depends(access_commander)]
