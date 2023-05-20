from collections import OrderedDict
from functools import wraps
from typing import Any, Generic

from .constants import CORO_FUNC, T


class RLUCache(Generic[T]):
    def __init__(self, *, size: int):
        self._size = size
        self._cache: OrderedDict[str, T] = OrderedDict()

    def __contains__(self, key: str) -> bool:
        return key in self._cache

    def __getitem__(self, key: str) -> T:
        return self._cache[key]

    def __len__(self) -> int:
        return len(self._cache)

    def __repr__(self) -> str:
        return repr(self._cache)

    def push(self, key: str, value: T):
        self._cache[key] = value
        self._cache.move_to_end(key, last=True)
        if len(self._cache) > self._size:
            self._cache.popitem(last=False)


class RLUManager(Generic[T]):
    def __init__(self, key: str, size: int = 10):
        self._key = key
        self._size = size
        self._rlu: RLUCache[T] = RLUCache(size=size)

    def __call__(self, coro_func: CORO_FUNC) -> CORO_FUNC:
        @wraps(coro_func)
        async def decorate(*args: Any, **kwargs: Any) -> T:
            key = kwargs[self._key]
            if key in self._rlu:
                return self._rlu[key]
            else:
                res = await coro_func(*args, **kwargs)
                self._rlu.push(key, res)
                return res

        return decorate


rlu = RLUManager
