import abc
from enum import Enum
from itertools import chain
from typing import ClassVar

from pydantic import BaseModel


class Block(BaseModel):
    type: str


class Text(Block):
    class Type(str, Enum):
        plain_text = "plain_text"
        mark_down = "mrkdwn"

    PLAIN_TEXT: ClassVar = Type.plain_text
    MARK_DOWN: ClassVar = Type.mark_down

    type: Type = MARK_DOWN
    text: str


class Divider(Block):
    type: str = "divider"


class Header(Block):
    type: str = "header"
    text: Text


class Section(Block):
    type: str = "section"
    text: Text


class Context(Block):
    type: str = "context"
    elements: list[Text]


class CardBlockkit(abc.ABC):
    def blocks(self) -> list[dict]:
        return [block.dict() for block in chain(self.header(), self.body(), self.footer())]

    @abc.abstractmethod
    def header(self) -> list[Block]:
        """Header Component"""

    @abc.abstractmethod
    def body(self) -> list[Block]:
        """Body Component"""

    @abc.abstractmethod
    def footer(self) -> list[Block]:
        """Footer Component"""
