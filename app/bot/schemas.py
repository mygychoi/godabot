from app.core.schemas import Schema


class Block(Schema):
    """TODO: Implement Slack BlockKit interface"""

    pass


class Message(Schema):
    token: str
    channel_id: str
    text: str
    blocks: list[Block] = []
