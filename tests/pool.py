from functools import wraps

from app.core.constants import CORO_FUNC, P, T
from app.core.database import PoolManager


def with_pool(coro_func: CORO_FUNC) -> CORO_FUNC:
    @wraps(coro_func)
    async def decorate(*args: P.args, **kwargs: P.kwargs) -> T:
        async with PoolManager.initiate(None):
            return await coro_func(*args, **kwargs)

    return decorate
