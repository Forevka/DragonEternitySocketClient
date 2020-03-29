# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = new_round_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
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
class NewRound:
    evt: str
    round: int
    evt_cnt: int
    agr: float
    pers_id: int
    evt_time: float
    evt_id: int

    @staticmethod
    def from_dict(obj: Any) -> 'NewRound':
        assert isinstance(obj, dict)
        evt = from_str(obj.get("evt", ""))
        round = from_int(obj.get("round", 0))
        evt_cnt = from_int(obj.get("evtCnt", 0))
        agr = from_float(obj.get("agr", 0.0))
        pers_id = from_int(obj.get("persId", 0))
        evt_time = from_float(obj.get("evtTime", 0.0))
        evt_id = from_int(obj.get("evtId", 0))
        return NewRound(evt, round, evt_cnt, agr, pers_id, evt_time, evt_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["evt"] = from_str(self.evt)
        result["round"] = from_int(self.round)
        result["evtCnt"] = from_int(self.evt_cnt)
        result["agr"] = to_float(self.agr)
        result["persId"] = from_int(self.pers_id)
        result["evtTime"] = to_float(self.evt_time)
        result["evtId"] = from_int(self.evt_id)
        return result


def new_round_from_dict(s: Any) -> NewRound:
    return NewRound.from_dict(s)


def new_round_to_dict(x: NewRound) -> Any:
    return to_class(NewRound, x)
