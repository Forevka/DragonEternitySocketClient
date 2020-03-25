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

class Update:
    events: typing.List[Event]
    raw_events: typing.List[ASObject]
    time: datetime.datetime

    def __init__(self, data: ASObject,):
        self.raw_events = data.get('events', [])
        self.events = []
        self.time = datetime.datetime.utcfromtimestamp(data.get('time', datetime.datetime.now().timestamp()))
        self._parse_events()

    def _parse_events(self,):
        for raw_event in self.raw_events:
            self.events.append(Event(raw_event))

