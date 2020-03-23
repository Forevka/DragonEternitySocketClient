from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)

def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()

@dataclass
class ChatMessage:
    channel: int
    evt: str
    chat_message_from: str
    key: str
    kind: int
    lang: str
    langs: int
    msg: str
    msg_time: float
    system: str

    @staticmethod
    def from_dict(obj: Any) -> 'ChatMessage':
        assert isinstance(obj, dict)
        channel = from_int(obj.get("channel"))
        evt = from_str(obj.get("evt"))
        chat_message_from = from_str(obj.get("from", ""))
        key = from_str(obj.get("key"))
        kind = from_int(obj.get("kind"))
        lang = from_str(obj.get("lang"))
        langs = from_int(obj.get("langs"))
        msg = from_str(obj.get("msg"))
        msg_time = from_float(obj.get("msgTime"))
        system = from_str(obj.get("system", ""))
        return ChatMessage(channel, evt, chat_message_from, key, kind, lang, langs, msg, msg_time, system)

    def to_dict(self) -> dict:
        return self.__dict__