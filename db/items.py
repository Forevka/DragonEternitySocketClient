#from models.game_state.FightItem import FightItem
from enums.sub_item_kind import SubItemKind
#from enums.attacks.magic import Magic
#from enums.item_kinds import ItemKind
import typing
import json

class ItemDB:
    db: dict

    magic: typing.Dict[int, dict]
    elixir: typing.Dict[int, dict]

    instance: 'ItemDB'

    def __init__(self):
        self.db = json.loads(open('db\\itemTpls.json', 'r', encoding='utf-8').read())

        self.magic = {}
        self.elixir = {}

        self._load_items()

    def get_item(self, id: int):
        return self.db.get(str(id), {})

    def _load_items(self,):
        for i in self.db.values():
            kind = i.get('kindId', 0)
            itemId = i.get('id', 0)
            if kind in SubItemKind.Magic:
                self.magic[int(itemId)] = i
            elif kind in SubItemKind.Elixir:
                self.elixir[int(itemId)] = i

    @staticmethod
    def get_instance() -> 'ItemDB':
        if (ItemDB.instance is None):
            ItemDB.instance = ItemDB()
        
        return ItemDB.instance

    def get_magic(self, id_: int):
        return self.magic.get(id_, None)
    
    def get_possible_magic(self, list_id: typing.List[int]):
        return [self.magic[i] for i in self.magic.keys() if i in list_id]

ItemDB.instance = ItemDB()