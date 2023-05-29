"""Depends on openai api specification
refer to https://platform.openai.com/docs/api-reference/chat/create
"""

from enum import Enum

from app.core.client import Form


class Model(str, Enum):
    gpt3dot5 = "gpt-3.5-turbo"


class Role(str, Enum):
    system = "system"
    assistant = "assistant"
    user = "user"


class MessageForm(Form):
    role: Role
    content: str


class ChatCompletionForm(Form):
    model: Model = Model.gpt3dot5
    messages: list[MessageForm]
    max_tokens: int = 512
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1

    @classmethod
    def from_prompt(cls, *, prompt: str) -> "ChatCompletionForm":
        return cls(
            messages=[
                MessageForm(role=Role.system, content="You are a helpful chatbot named godabot."),
                MessageForm(role=Role.user, content=prompt),
            ]
        )


class ChatCompletionFormResult(Form):
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

    class ChoiceForm(Form):
        index: int
        message: MessageForm
        finish_reason: str

    class UsageForm(Form):
        prompt_tokens: int
        completion_tokens: int
        total_tokens: int

    id: str
    object: str
    created: int
    choices: list[ChoiceForm]
    usage: UsageForm

    class Config:
        orm_mode = True

    @property
    def answer(self) -> str:
        return "".join(choice.message.content for choice in self.choices)
