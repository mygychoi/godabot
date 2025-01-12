from pydantic import Field

from app.core.client import Form

from .schemas import FileInput


class FileForm(Form):
    channel: str = Field(alias="channel_id")
    file_name: str
    file: bytes
    title: str
    initial_comment: str

    @classmethod
    def from_input(cls, *, input: FileInput) -> "FileForm":
        return cls(title=input.file_name, **input.dict())
