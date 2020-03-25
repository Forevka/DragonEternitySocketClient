# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = opponent_new_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import List, Any, Dict, TypeVar, Callable, Type, cast
from utils.parse import from_float


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class OpponentNew:
    agr: float
    bot: bool
    bot_tpl_id: int
    dead: bool
    effects: List[Any]
    evt: str
    gender: int
    hp: int
    id: int
    level: int
    max_hp: int
    max_mp: int
    mp: int
    parts: Dict[str, int]
    pers_id: int
    round: int
    spell_used_cnt: Dict[Any, Any]
    stand: int
    team: int

    @staticmethod
    def from_dict(obj: Any) -> 'OpponentNew':
        assert isinstance(obj, dict)
        agr = from_float(obj.get("agr"))
        bot = from_bool(obj.get("bot"))
        bot_tpl_id = from_int(obj.get("botTplId"))
        dead = from_bool(obj.get("dead"))
        effects = from_list(lambda x: x, obj.get("effects"))
        evt = from_str(obj.get("evt"))
        gender = from_int(obj.get("gender"))
        hp = from_int(obj.get("hp"))
        id = from_int(obj.get("id"))
        level = from_int(obj.get("level"))
        max_hp = from_int(obj.get("maxHp"))
        max_mp = from_int(obj.get("maxMp"))
        mp = from_int(obj.get("mp"))
        parts = from_dict(from_int, obj.get("parts"))
        pers_id = from_int(obj.get("persId"))
        round = from_int(obj.get("round"))
        spell_used_cnt = obj.get("spellUsedCnt", {})
        stand = from_int(obj.get("stand"))
        team = from_int(obj.get("team"))
        return OpponentNew(agr, bot, bot_tpl_id, dead, effects, evt, gender, hp, id, level, max_hp, max_mp, mp, parts, pers_id, round, spell_used_cnt, stand, team)

    def to_dict(self) -> dict:
        result: dict = {}
        result["agr"] = from_int(self.agr)
        result["bot"] = from_bool(self.bot)
        result["botTplId"] = from_int(self.bot_tpl_id)
        result["dead"] = from_bool(self.dead)
        result["effects"] = from_list(lambda x: x, self.effects)
        result["evt"] = from_str(self.evt)
        result["gender"] = from_int(self.gender)
        result["hp"] = from_int(self.hp)
        result["id"] = from_int(self.id)
        result["level"] = from_int(self.level)
        result["maxHp"] = from_int(self.max_hp)
        result["maxMp"] = from_int(self.max_mp)
        result["mp"] = from_int(self.mp)
        result["parts"] = from_dict(from_int, self.parts)
        result["persId"] = from_int(self.pers_id)
        result["round"] = from_int(self.round)
        result["spellUsedCnt"] = from_list(lambda x: x, self.spell_used_cnt)
        result["stand"] = from_int(self.stand)
        result["team"] = from_int(self.team)
        return result


def opponent_new_from_dict(s: Any) -> OpponentNew:
    return OpponentNew.from_dict(s)


def opponent_new_to_dict(x: OpponentNew) -> Any:
    return to_class(OpponentNew, x)
