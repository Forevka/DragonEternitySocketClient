# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = item_info_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast
from uuid import UUID


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Place:
    bag: int

    @staticmethod
    def from_dict(obj: Any) -> 'Place':
        bag = from_int(obj.get("bag"))
        return Place(bag)

    def to_dict(self) -> dict:
        result: dict = {}
        result["bag"] = from_int(self.bag)
        return result


@dataclass
class ItemInfo:
    create_time: float
    evt: str
    id: UUID
    item_tpl_id: int
    place: Place

    @staticmethod
    def from_dict(obj: Any) -> 'ItemInfo':
        create_time = from_float(obj.get("createTime"))
        evt = from_str(obj.get("evt"))
        id = UUID(obj.get("id"))
        item_tpl_id = from_int(obj.get("itemTplId"))
        place = Place.from_dict(obj.get("place"))
        return ItemInfo(create_time, evt, id, item_tpl_id, place)

    def to_dict(self) -> dict:
        result: dict = {}
        result["createTime"] = to_float(self.create_time)
        result["evt"] = from_str(self.evt)
        result["id"] = str(self.id)
        result["itemTplId"] = from_int(self.item_tpl_id)
        result["place"] = to_class(Place, self.place)
        return result


def item_info_from_dict(s: Any) -> ItemInfo:
    return ItemInfo.from_dict(s)


def item_info_to_dict(x: ItemInfo) -> Any:
    return to_class(ItemInfo, x)
