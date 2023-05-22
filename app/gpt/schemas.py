"""Depends on openai api specification
refer to https://platform.openai.com/docs/api-reference/chat/create
"""

from enum import Enum

from app.core.schemas import Schema


class ChatModel(str, Enum):
    gpt3dot5 = "gpt-3.5-turbo"


class Role(str, Enum):
    system = "system"
    assistant = "assistant"
    user = "user"


class Message(Schema):
    role: Role
    content: str


class ChatCompletionRequest(Schema):
    model: ChatModel
    messages: list[Message]
    max_token: int
    temperature: float
    top_p: float
    n: int


class ChatCompletionResponse(Schema):
    """{
      "id": "chatcmpl-123",
      "object": "chat.completion",
      "created": 1677652288,
      "choices": [{
        "index": 0,
        "message": {
          "role": "assistant",
          "content": "\n\nHello there, how may I assist you today?",
        },
        "finish_reason": "stop"
      }],
      "usage": {
        "prompt_tokens": 9,
        "completion_tokens": 12,
        "total_tokens": 21
      }
    }
    """

    class Choice(Schema):
        index: int
        message: Message
        finish_reason: str

    class Usage(Schema):
        prompt_tokens: int
        completion_tokens: int
        total_tokens: int

    id: str
    object: str
    created: int
    choices: list[Choice]
    usage: Usage

    class Config:
        orm_mode = True

    def answer(self):
        return "".join(choice.message.content for choice in self.choices)
