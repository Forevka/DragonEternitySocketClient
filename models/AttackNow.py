from dataclasses import dataclass
from typing import Dict, Any
from utils.parse import from_int, from_str, from_float

@dataclass
class AttackNow:
    evt: str
    evt_cnt: int
    opp_hp: int
    remained: int
    hp: int
    mp: int
    pers_id: int
    next_stands: Dict[str, int]
    evt_time: float
    evt_id: int
    opp_mp: int

    @staticmethod
    def from_dict(obj: Any) -> 'AttackNow':
        evt = from_str(obj.get("evt"))
        evt_cnt = from_float(obj.get("evtCnt", 0))
        opp_hp = from_float(obj.get("oppHp", 0))
        remained = from_float(obj.get("remained", 0))
        hp = from_float(obj.get("hp", 0))
        mp = from_float(obj.get("mp", 0))
        pers_id = from_float(obj.get("persId", 0))
        next_stands = obj.get("nextStands")
        evt_time = obj.get("evtTime", 0.0)
        evt_id = from_float(obj.get("evtId", 0))
        opp_mp = from_float(obj.get("oppMp", 0))
        return AttackNow(evt, evt_cnt, opp_hp, remained, hp, mp, pers_id, next_stands, evt_time, evt_id, opp_mp)

    def to_dict(self) -> dict:
        result: dict = {}
        result["evt"] = from_str(self.evt)
        result["evtCnt"] = from_int(self.evt_cnt)
        result["oppHp"] = from_int(self.opp_hp)
        result["remained"] = from_int(self.remained)
        result["hp"] = from_int(self.hp)
        result["mp"] = from_int(self.mp)
        result["persId"] = from_int(self.pers_id)
        result["nextStands"] = self.next_stands
        result["evtTime"] = self.evt_time
        result["evtId"] = from_int(self.evt_id)
        result["oppMp"] = from_int(self.opp_mp)
        return result