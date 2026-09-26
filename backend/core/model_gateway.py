from abc import ABC, abstractmethod
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

ModelRole = Literal["system", "user", "assistant", "tool"]

class ModelMessage(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    role: ModelRole
    content: str = Field(min_length=1, max_length=16_000)

class ModelRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    messages: list[ModelMessage] = Field(min_length=1, max_length=64)
    max_output_tokens: int = Field(default=2_000, ge=1, le=8_000)
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)

    def validate_bounds(self) -> None:
        total = sum(len(message.content) for message in self.messages)
        if total > 100_000:
            raise ValueError("model request content exceeds 100000 characters")

class ModelResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    provider: str = Field(min_length=1, max_length=64)
    model: str = Field(min_length=1, max_length=128)
    content: str = Field(min_length=1, max_length=20_000)
    finish_reason: str | None = Field(default=None, max_length=64)

class ModelGateway(ABC):
    @abstractmethod
    def generate(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError

class StaticModelGateway(ModelGateway):
    def __init__(self, content: str, *, model: str = "static-test") -> None:
        if not content.strip():
            raise ValueError("content must not be blank")
        self._content = content
        self._model = model

    def generate(self, request: ModelRequest) -> ModelResponse:
        request.validate_bounds()
        return ModelResponse(
            provider="static",
            model=self._model,
            content=self._content,
            finish_reason="stop",
        )
