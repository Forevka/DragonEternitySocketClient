from dataclasses import dataclass
from db.bot_info_db import BotInfoDB
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Bot:
    area_bot_id: int
    id: int

    def get_name(self,):
        me = BotInfoDB.get_instance().get_by_area_id(self.area_bot_id)
        return me.get('title', '')

    @staticmethod
    def from_dict(obj: Any) -> 'Bot':
        assert isinstance(obj, dict)
        area_bot_id = from_int(obj.get("areaBotId", 0))
        id = from_int(obj.get("id", 0))
        return Bot(area_bot_id, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["areaBotId"] = from_int(self.area_bot_id)
        result["id"] = from_int(self.id)
        return result


@dataclass
class AreaBots:
    bots: List[Bot]
    evt: str

    def find_by_name(self, name: str):
        for i in self.bots:
            if name.lower() in i.get_name().lower():
                return i
        
        return None

    @staticmethod
    def from_dict(obj: Any) -> 'AreaBots':
        assert isinstance(obj, dict)
        bots = from_list(Bot.from_dict, obj.get("bots"))
        evt = from_str(obj.get("evt"))
        return AreaBots(bots, evt)

    def to_dict(self) -> dict:
        result: dict = {}
        result["bots"] = from_list(lambda x: to_class(Bot, x), self.bots)
        result["evt"] = from_str(self.evt)
        return result


def area_bots_from_dict(s: Any) -> AreaBots:
    return AreaBots.from_dict(s)


def area_bots_to_dict(x: AreaBots) -> Any:
    return to_class(AreaBots, x)
