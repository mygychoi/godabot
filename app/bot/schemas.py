from app.core.service import Schema


class MessageInput(Schema):
    channel_id: str
    text: str
    blocks: list[dict] = []


class FileInput(Schema):
    channel_id: str
    file: bytes
    file_name: str
    initial_comment: str
