from utils.parse import from_int
from dataclasses import dataclass
import typing

class FightItem:
    item_tpl_id: int
    cnt: int
    src_type: int
    src_id: str
    data: dict

    item_type: typing.Any

    def get_type_str(self,):
        return str(self.item_type)