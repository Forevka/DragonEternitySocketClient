from DataMixin import DataMixin
import datetime
import typing

from loguru import logger

from events import EventType
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

    def __init__(self, data: dict,):
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
        if (data.get('status', None) is not None):
            self.events.append(Event({'evt': 'ping'}))
        self.time = datetime.datetime.utcfromtimestamp(data.get('time', datetime.datetime.now().timestamp()))
        self._parse_events()

    def _parse_events(self,):
        for raw_event in self.raw_events:
            self.events.append(event_factory(raw_event))

