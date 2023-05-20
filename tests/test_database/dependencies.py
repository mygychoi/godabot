from typing import Annotated

from fastapi import Depends

from .repositories import TempCommandRepository, TempQueryRepository
from .services import TempCommandService, TempQueryService

TempQuerier = Annotated[TempQueryService, Depends(TempQueryRepository)]
TempCommander = Annotated[TempCommandService, Depends(TempCommandRepository)]
