from app.core.schemas import Schema


class Block(Schema):
    """TODO: Implement Slack BlockKit interface"""

    pass


class Message(Schema):
    token: str
    channel_id: str
    text: str
    blocks: list[Block] = []


class File(Schema):
    token: str
    channel_id: str
    file_name: str
    file: bytes
    initial_comment: str
