from fastapi.exceptions import HTTPException

from app.core.database import CommandService, QueryService

from .clients import AccessClient
from .models import Access
from .repositories import AccessCommandRepository, AccessQueryRepository
from .schemas import AccessRequest


class AccessQueryService(QueryService):
    repository: AccessQueryRepository = AccessQueryRepository()

    async def get_by_team_id(self, *, team_id: str) -> Access:
        return await self.repository.get_by_team_id(team_id=team_id)


class AccessCommandService(CommandService):
    querier: AccessQueryService = AccessQueryService()
    repository: AccessCommandRepository = AccessCommandRepository()
    client: AccessClient = AccessClient()

    async def activate(self, *, request: AccessRequest) -> Access:
        access_resp = await self.client.request(request=request)
        if not access_resp.ok:
            raise HTTPException(status_code=403, detail="Failed")
        access = Access.parse_response(response=access_resp)
        async with self.transaction():
            return await self.repository.save(access=access)

    async def deactivate(self, *, team_id: str) -> Access:
        access = await self.querier.get_by_team_id(team_id=team_id)
        if not access.is_active:
            return access
        else:
            access.is_active = False
            async with self.transaction():
                return await self.repository.save(access=access)

    async def delete(self, *, team_id: str):
        async with self.transaction():
            await self.repository.delete(team_id=team_id)
