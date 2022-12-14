from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ChatRequest(_message.Message):
    __slots__ = ["text"]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class ChatResponse(_message.Message):
    __slots__ = ["error", "text"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    error: str
    text: str
    def __init__(self, text: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class ChatStreamResponse(_message.Message):
    __slots__ = ["end_of_stream", "error", "text"]
    END_OF_STREAM_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    end_of_stream: bool
    error: str
    text: str
    def __init__(self, text: _Optional[str] = ..., error: _Optional[str] = ..., end_of_stream: bool = ...) -> None: ...
