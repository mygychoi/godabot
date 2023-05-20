from __future__ import annotations

from typing import Self

from asyncpg import Record
from pydantic import BaseModel

from .registry import Registry


class Schema(Registry, BaseModel):
    @classmethod
    def construct_from(cls, *, obj: Record | dict, _fields_set: set | None = None) -> Self:
        return cls.construct(**obj, _fields_set=_fields_set)

    @classmethod
    def construct_from_or_none(
        cls, *, obj: Record | dict, _fields_set: set | None = None
    ) -> Self | None:
        if obj is None:
            return None
        else:
            return cls.construct(**obj, _fields_set=_fields_set)

    @classmethod
    def parse_obj_or_none(cls, *, obj: dict | Record | None) -> Self | None:
        if obj is None:
            return None
        else:
            return cls.parse_obj(obj)
