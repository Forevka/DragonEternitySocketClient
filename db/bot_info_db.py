#from models.game_state.FightItem import FightItem
from enums.sub_item_kind import SubItemKind
import typing
import json

class BotInfoDB:
    db: dict

    instance: 'BotInfoDB'

    def __init__(self):
        self.db = json.loads(open('db\\botTpls.json', 'r', encoding='utf-8').read())

    def get_by_id(self, bot_id: int):
        return self.db[str(bot_id)]

    @staticmethod
    def get_instance() -> 'BotInfoDB':
        if (BotInfoDB.instance is None):
            BotInfoDB.instance = BotInfoDB()
        
        return BotInfoDB.instance

BotInfoDB.instance = BotInfoDB()