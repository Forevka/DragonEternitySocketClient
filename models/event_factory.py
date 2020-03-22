from miniamf import ASObject
from models.BaseEvent import PingEvent, Event, EnterEvent

def event_factory(data: ASObject,):
    if (data.get('evt', None)):
        return Event(data)
    elif (data.get('status', None)):
        return PingEvent()
    else:
        return EnterEvent(data)