import typing
import json

class ItemKindDB:
    instance: 'ItemKindDB'

    db: typing.Dict[str, dict]

    def __init__(self,):
        self.db = json.loads(open('db\\itemKinds.json', 'r', encoding='utf-8').read())

    def get_all_kinds(self,) -> typing.List[int]:
        return [int(i) for i in self.db.keys()]

    @staticmethod
    def get_instance() -> 'ItemKindDB':
        if (ItemKindDB.instance is None):
            ItemKindDB.instance = ItemKindDB()
        
        return ItemKindDB.instance


ItemKindDB.instance = ItemKindDB()