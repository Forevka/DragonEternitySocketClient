# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = cast_from_dict(json.loads(json_string))

from dataclasses import dataclass
from models.FightState import from_bool
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Damage:
    dmg_type: int
    evt: str
    hp: int
    pers_id: int
    target_id: int
    armor: int
    block: bool
    cid: int
    maxHp: int
    maxMp: int
    item_tpl_id: int
    type_: str
    crit: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Damage':
        assert isinstance(obj, dict)
        crit = from_bool(obj.get('crit', False))
        block = from_bool(obj.get('block', False))
        armor = from_int(obj.get('armor', 0))
        dmg_type = from_int(obj.get("dmgType", 0))
        evt = from_str(obj.get("evt", ''))
        hp = from_int(obj.get("hp", 0))
        pers_id = from_int(obj.get("persId", 0))
        type_ = from_str(obj.get("type", ''))
        target_id = from_int(obj.get("targetId", 0))
        cid = from_int(obj.get("id", 0))
        maxHp = from_int(obj.get("maxHp", 0))
        maxMp = from_int(obj.get("maxMp", 0))
        item_tpl_id = from_int(obj.get("itemTplId", 0))
        return Damage(dmg_type, evt, hp, pers_id, target_id, armor, block, cid, maxHp, maxMp,item_tpl_id, type_, crit)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dmgType"] = from_int(self.dmg_type)
        result["evt"] = from_str(self.evt)
        result["hp"] = from_int(self.hp)
        result["persId"] = from_int(self.pers_id)
        result["targetId"] = from_int(self.target_id)
        return result


@dataclass
class Cast:
    dmg: int
    events: List[Damage]
    evt: str
    item_tpl_id: int
    mp: int
    pers_id: int
    stand: int
    stat_killed_bots: int
    stat_killed_users: int
    target_id: int

    @staticmethod
    def from_dict(obj: Any) -> 'Cast':
        assert isinstance(obj, dict)
        dmg = from_int(obj.get("dmg"))
        events = from_list(Damage.from_dict, obj.get("events"))
        evt = from_str(obj.get("evt"))
        item_tpl_id = from_int(obj.get("itemTplId"))
        mp = from_int(obj.get("mp"))
        pers_id = from_int(obj.get("persId"))
        stand = from_int(obj.get("stand"))
        stat_killed_bots = from_int(obj.get("statKilledBots"))
        stat_killed_users = from_int(obj.get("statKilledUsers"))
        target_id = from_int(obj.get("targetId"))
        return Cast(dmg, events, evt, item_tpl_id, mp, pers_id, stand, stat_killed_bots, stat_killed_users, target_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dmg"] = from_int(self.dmg)
        result["events"] = from_list(lambda x: to_class(Damage, x), self.events)
        result["evt"] = from_str(self.evt)
        result["itemTplId"] = from_int(self.item_tpl_id)
        result["mp"] = from_int(self.mp)
        result["persId"] = from_int(self.pers_id)
        result["stand"] = from_int(self.stand)
        result["statKilledBots"] = from_int(self.stat_killed_bots)
        result["statKilledUsers"] = from_int(self.stat_killed_users)
        result["targetId"] = from_int(self.target_id)
        return result


def cast_from_dict(s: Any) -> Cast:
    return Cast.from_dict(s)


def cast_to_dict(x: Cast) -> Any:
    return to_class(Cast, x)
