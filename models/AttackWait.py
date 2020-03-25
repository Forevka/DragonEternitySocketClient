from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    return int(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class AttackWait:
    evt: str
    hp: int
    mp: int
    opp_hp: int
    opp_mp: int
    pers_id: int
    remained: int

    @staticmethod
    def from_dict(obj: Any) -> 'AttackWait':
        assert isinstance(obj, dict)
        evt = from_str(obj.get("evt"))
        hp = from_int(obj.get("hp"))
        mp = from_int(obj.get("mp"))
        opp_hp = from_int(obj.get("oppHp"))
        opp_mp = from_int(obj.get("oppMp"))
        pers_id = from_int(obj.get("persId"))
        remained = from_int(obj.get("remained"))
        return AttackWait(evt, hp, mp, opp_hp, opp_mp, pers_id, remained)

    def to_dict(self) -> dict:
        result: dict = {}
        result["evt"] = from_str(self.evt)
        result["hp"] = from_int(self.hp)
        result["mp"] = from_int(self.mp)
        result["oppHp"] = from_int(self.opp_hp)
        result["oppMp"] = from_int(self.opp_mp)
        result["persId"] = from_int(self.pers_id)
        result["remained"] = from_int(self.remained)
        return result


def attack_wait_from_dict(s: Any) -> AttackWait:
    return AttackWait.from_dict(s)


def attack_wait_to_dict(x: AttackWait) -> Any:
    return to_class(AttackWait, x)
