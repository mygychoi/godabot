import time
from functools import wraps

from .constants import CORO_FUNC, P, T


def atimer(coro_func: CORO_FUNC) -> CORO_FUNC:
    @wraps(coro_func)
    async def decorate(*args: P.args, **kwargs: P.kwargs) -> tuple[float, T]:
        start = time.perf_counter()
        res = await coro_func(*args, **kwargs)
        return time.perf_counter() - start, res

    return decorate
