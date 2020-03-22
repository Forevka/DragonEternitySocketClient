import typing
import datetime
from events import EventType
from miniamf import ASObject
from loguru import logger

class BaseEvent:
    data: ASObject
    event: EventType

    def __init__(self, data: ASObject,):
        self.data = data

class Event(BaseEvent):

    def __init__(self, data: ASObject,):
        self.event = data['evt']
        self.data = data

class EnterEvent(BaseEvent):

    def __init__(self, data: ASObject,):
        self.event = EventType.Enter
        self.data = data

class PingEvent(BaseEvent):

    def __init__(self,):
        self.event = EventType.Ping

class Update:
    status: bool
    events: typing.List[BaseEvent]
    time: datetime.datetime

    def __init__(self, data: ASObject,):
        self.events = data.get('events', [])
        self.status = data.get('status', None)
        if (self.status is not None):
            self.events.append({'evt': 'ping'})
        self.time = datetime.datetime.utcfromtimestamp(data.get('time', datetime.datetime.now().timestamp()))