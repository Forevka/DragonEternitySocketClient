from uuid import UUID
from db.items import ItemDB
from models.ItemInfo import ItemInfo
import typing

class ItemInfoDB:
    instance: 'ItemInfoDB'

    db: typing.Dict[str, ItemInfo]
    itemdb: ItemDB

    def __init__(self,):
        self.db = {}
        self.itemdb = ItemDB.get_instance()
    
    def add_item(self, item: ItemInfo):
        self.db[str(item.id)] = item
    
    def get_item_description(self, id_: UUID):
        item = self.db[str(id_)]

        return self.itemdb.get_item(item.item_tpl_id)

    @staticmethod
    def get_instance() -> 'ItemInfoDB':
        if (ItemInfoDB.instance is None):
            ItemInfoDB.instance = ItemInfoDB()
        
        return ItemInfoDB.instance


ItemInfoDB.instance = ItemInfoDB()