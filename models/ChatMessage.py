from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast
from utils.parse import from_int, from_str, from_float

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
        channel = from_int(obj.get("channel"))
        evt = from_str(obj.get("evt"))
        chat_message_from = from_str(obj.get("from", ""))
        key = from_str(obj.get("key", ''))
        kind = from_int(obj.get("kind", -1))
        lang = from_str(obj.get("lang", ''))
        langs = from_int(obj.get("langs", -1))
        msg = from_str(obj.get("msg"))
        msg_time = from_float(obj.get("msgTime"))
        system = from_str(obj.get("system", ""))
        return ChatMessage(channel, evt, chat_message_from, key, kind, lang, langs, msg, msg_time, system)

    def to_dict(self) -> dict:
        return self.__dict__