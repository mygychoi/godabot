from typing import Awaitable, Callable, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")
CORO_FUNC = Callable[P, Awaitable[T]]
