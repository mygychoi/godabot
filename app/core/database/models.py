from __future__ import annotations

from datetime import datetime
from typing import Self, TypeVar

from asyncpg import Record
from pydantic import BaseModel, Field

from app.core.registry import Registry
from app.core.timezone import utcnow


class Model(BaseModel, Registry):
    @classmethod
    def construct_from(cls, *, record: Record | dict, _fields_set: set | None = None) -> Self:
        return cls.construct(**record, _fields_set=_fields_set)

    @classmethod
    def construct_from_or_none(
        cls, *, record: Record | dict, _fields_set: set | None = None
    ) -> Self | None:
        if record is None:
            return None
        else:
            return cls.construct(**record, _fields_set=_fields_set)

    @classmethod
    def parse_obj_or_none(cls, *, obj: dict | Record) -> Self | None:
        if obj is None:
            return None
        else:
            return cls.parse_obj(obj)

    @classmethod
    def update_many_from(cls, *, models: list[ModelType], records: list[Record]):
        for i in range(len(records)):
            models[i].update_from(record=records[i])

    def update_from(self, *, record: Record):
        for field, value in record.items():
            setattr(self, field, value)


ModelType = TypeVar("ModelType", bound=Model)


class TimestampModel(Model):
    created_at: datetime = Field(
        description="timestamp with time zone, not null",
        default_factory=utcnow,
    )
    updated_at: datetime | None = Field(
        description="timestamp with time zone",
        default=None,
    )
