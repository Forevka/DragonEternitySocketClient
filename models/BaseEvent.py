from dataclasses import dataclass
from mixines.item_data_db import ItemDataFromDBMixine
from enums.events.events import EventType
from DataMixin import DataMixin
import datetime
import typing

from loguru import logger
from miniamf import ASObject

def event_factory(data: dict,):
    if (data.get('evt', None)):
        return Event(data)
    elif (data.get('status', None)):
        return Event({'evt': 'Ping'})
    else:
        return Event({'evt': 'Enter'})

class BaseEvent(DataMixin):
    event: EventType
    seq: int

    def __init__(self, data: dict,):
        self.seq = data.get('seq', -1)
        self.data.update(data)

class Event(BaseEvent):

    def __init__(self, data: dict,):
        super().__init__(data)
        self.event = data['evt']

@dataclass
class UserLot:
    rank2: int
    nick: str
    level: int
    kind: int
    normNick: str
    rank: int
    registerLang: str

@dataclass
class ItemLot(ItemDataFromDBMixine):
    create_time: float
    durability: int
    item_tpl_id: int
    item_unical_id: str
    amount: int

@dataclass
class Lot:
    user: UserLot
    item: ItemLot

    time: int
    lot_id: int
    buyout: int
    price: int

    def __init__(self, data: dict,):
        self.buyout = data.get('buyout', 0)
        self.lot_id = data.get('id', 0)
        self.price = data.get('price', 0)
        self.time = data.get('time', 0)

        user = data.get('user', {})
        item = data.get('item', {})

        self.user = UserLot(user.get('rank2', 0), user.get('nick', ''), user.get('level', 0), user.get('kind', 0), user.get('normNick', ''), user.get('rank', 0), user.get('registerLang', 'ru'))
        amount = item.get('place')
        if (isinstance(amount, str)):
            amount = 1
        elif (isinstance(amount, dict)):
            amount = amount.get('auction', 1)
        else:
            amount = 1
            
        self.item = ItemLot(item.get('createTime', 0.0), item.get('durability', 0), item.get('itemTplId', 0), item.get('id', ''), amount)
        

class Update:
    seq: int

    events: typing.List[Event]
    lots: typing.List[Lot]

    raw_events: typing.List[ASObject]
    raw_lots: typing.List[ASObject]
    time: datetime.datetime

    def __init__(self, data: ASObject,):
        self.seq = data.get('seq', -1)
        self.raw_events = data.get('events', [])
        self.raw_lots = data.get('lots', [])

        self.events = []
        self.lots = []

        self.time = datetime.datetime.utcfromtimestamp(data.get('time', datetime.datetime.now().timestamp()))
        self._parse_events()
        self._parse_lots()

    def _parse_lots(self,):
        if (self.raw_lots):
            for raw_lot in self.raw_lots:
                self.lots.append(Lot(raw_lot))
            
            self.events.append(Event({'evt': 'lots', 'lots': self.lots}))
        
        

    def _parse_events(self,):
        for raw_event in self.raw_events:
            self.events.append(Event(raw_event))

