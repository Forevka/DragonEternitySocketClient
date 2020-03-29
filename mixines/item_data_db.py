from db.items import ItemDB

class ItemDataFromDBMixine:
    item_tpl_id: int

    def item_info(self,):
        return ItemDB.get_instance().get_item(self.item_tpl_id)