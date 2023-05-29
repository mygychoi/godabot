from app.core.service import Schema


class BlockInput(Schema):
    """TODO: Implement Slack BlockKit interface"""

    pass


class MessageInput(Schema):
    channel_id: str
    text: str
    blocks: list[BlockInput] = []


class FileInput(Schema):
    channel_id: str
    file: bytes
    file_name: str
    initial_comment: str
