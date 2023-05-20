from typing import Awaitable, Callable, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")
CORO_FUNC = Callable[P, Awaitable[R]]

T = TypeVar("T")
