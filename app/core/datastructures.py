from typing import Generic

from pydantic import Extra
from pydantic.generics import GenericModel

from .constants import T


class Empty(Exception):
    pass


class Stack(GenericModel, Generic[T]):
    data: list[T] = []

    class Config:
        frozen = True
        extra = Extra.forbid
        arbitrary_types_allowed = True

    def __len__(self) -> int:
        return len(self.data)

    def __bool__(self) -> bool:
        return bool(self.data)

    def push(self, item: T):
        self.data.append(item)

    def pop(self) -> T:
        if self.is_empty():
            raise Empty("Slack is empty.")
        return self.data.pop()

    def top(self) -> T:
        if self.is_empty():
            raise Empty("Slack is empty")
        return self.data[-1]

    def is_empty(self) -> bool:
        return len(self) == 0
