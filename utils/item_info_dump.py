from db.item_kinds_db import ItemKindDB
from typing import List
from models.BaseEvent import Lot
import sqlite3
 

class LotItemDB:

    instance: 'LotItemDB'

    def __init__(self,):
        self.conn = sqlite3.connect("lots_prices.sqlite") # или :memory: чтобы сохранить в RAM
        self.cursor = self.conn.cursor()
    

    def write_lot(self, lot: Lot):
        item_name = lot.item.item_info().get('title', '')
        sql_query = f"INSERT or ignore into lots VALUES ({lot.lot_id}, '{lot.item.item_unical_id}', {lot.item.item_tpl_id}, {lot.item.create_time}, {lot.item.amount}, {lot.price}, {lot.buyout}, '{item_name}', '{lot.user.nick}', {lot.time})"

        self.cursor.execute(sql_query)

    def commit(self,):
        self.conn.commit()


    @staticmethod
    def get_instance() -> 'LotItemDB':
        #if (LotItemDB.instance is None):
        #    LotItemDB.instance = LotItemDB()
        
        return LotItemDB()#LotItemDB.instance


#LotItemDB.instance = LotItemDB()