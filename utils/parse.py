from enums.attacks.other import Nephelim
from enums.attacks.attacks import Attack
from enums.items.consumable import Elixir, Orb
from enums.attacks.magic import Magic
from typing import Any, List, TypeVar, Callable, Type, cast

def load_item_type(item_id: int):
    try:
        return Magic(item_id)
    except:
        pass

    try:
        return Orb(item_id)
    except:
        pass

    try:
        return Attack(item_id)
    except:
        pass

    try:
        return Elixir(item_id)
    except:
        pass

    try:
        return Nephelim(item_id)
    except:
        pass

    raise ValueError(f"Unknow Item {item_id}")

T = TypeVar("T")

def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x

def from_none(x: Any) -> Any:
    assert x is None
    return x

def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x

def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]

def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x

def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()

def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x
