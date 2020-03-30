# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = fight_results_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast
from uuid import UUID


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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class DropItem:
    item_id: UUID
    count: int

    @staticmethod
    def from_dict(data: dict):
        r = []
        for i in data.items():
            r.append(DropItem(i[0], i[1]))
        return r

@dataclass
class FightResults:
    area_id: int
    dec_money: bool
    dmg: int
    drop_items: List[DropItem]
    eliminated_bots: List[Any]
    evt: str
    exp: int
    fight_id: UUID
    fight_title: str
    finish: bool
    honor: int
    honor2: int
    kill_cnt: int
    money: int
    pvp: bool
    team: int
    winner_team: int

    @staticmethod
    def from_dict(obj: Any) -> 'FightResults':
        area_id = from_int(obj.get("areaId", 0))
        dec_money = from_bool(obj.get("decMoney", False))
        dmg = from_int(obj.get("dmg", 0))
        drop_items = DropItem.from_dict(obj.get("dropItems", {}))#DropItems.from_dict(obj.get("dropItems"))
        eliminated_bots = []#from_list(lambda x: x, obj.get("eliminatedBots"))
        evt = from_str(obj.get("evt", ''))
        exp = from_int(obj.get("exp", 0))
        fight_id = UUID(obj.get("fightId", ''))
        fight_title = from_str(obj.get("fightTitle", ''))
        finish = from_bool(obj.get("finish", True))
        honor = from_int(obj.get("honor", 0))
        honor2 = from_int(obj.get("honor2", 0))
        kill_cnt = from_int(obj.get("killCnt", 0))
        money = from_int(obj.get("money", 0))
        pvp = from_bool(obj.get("pvp", False))
        team = from_int(obj.get("team", 1))
        winner_team = from_int(obj.get("winnerTeam", 1))
        return FightResults(area_id, dec_money, dmg, drop_items, eliminated_bots, evt, exp, fight_id, fight_title, finish, honor, honor2, kill_cnt, money, pvp, team, winner_team)

    def to_dict(self) -> dict:
        result: dict = {}
        result["areaId"] = from_int(self.area_id)
        result["decMoney"] = from_bool(self.dec_money)
        result["dmg"] = from_int(self.dmg)
        result["dropItems"] = dict(self.drop_items)#to_class(DropItems, self.drop_items)
        result["eliminatedBots"] = from_list(lambda x: x, self.eliminated_bots)
        result["evt"] = from_str(self.evt)
        result["exp"] = from_int(self.exp)
        result["fightId"] = str(self.fight_id)
        result["fightTitle"] = from_str(self.fight_title)
        result["finish"] = from_bool(self.finish)
        result["honor"] = from_int(self.honor)
        result["honor2"] = from_int(self.honor2)
        result["killCnt"] = from_int(self.kill_cnt)
        result["money"] = from_int(self.money)
        result["pvp"] = from_bool(self.pvp)
        result["team"] = from_int(self.team)
        result["winnerTeam"] = from_int(self.winner_team)
        return result


def fight_results_from_dict(s: Any) -> FightResults:
    return FightResults.from_dict(s)


def fight_results_to_dict(x: FightResults) -> Any:
    return to_class(FightResults, x)
