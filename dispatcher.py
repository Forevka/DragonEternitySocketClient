from AMFBuffer import AMFBuffer
from loguru import logger
from events import EventType
from models.event_factory import event_factory
from models.BaseEvent import Event
import typing

import json 

def upperfirst(x):
    def sliceindex(x):
        i = 0
        for c in x:
            if c.isalpha():
                i = i + 1
                return i
            i = i + 1

    i = sliceindex(x)
    return x[:i].upper() + x[i:]

class Dispatcher:
    handlers: typing.Dict[EventType, typing.List[typing.Callable[['Client', 'Dispatcher', Event], None]]]
    client: 'Client'

    def __init__(self, client: 'Client'):
        self.handlers = {}
        self.client = client
    

    def dispatch(self, data, client: 'Client'):
        #length = data[:4]
        #print(length)
        #length = int.from_bytes(bytes=length, byteorder='big')
        #print(length)
        buffer = AMFBuffer()
        updates = buffer.decode(data[4:])
        logger.debug(f'new update {updates.time}')

        for update in updates.events:
            event = event_factory(update)
            logger.debug(f'Event {event.event}')
            for handler in self.handlers.get(EventType[upperfirst(event.event)], []):
                handler(self.client, self, update)

    def add_handler(
        self, 
        event: EventType, 
        task: typing.Callable[['Client', 'Dispatcher', Event], None],
    ):
        handlers: list = self.handlers.get(event, [])
        handlers.append(task)
        self.handlers[event] = handlers


    def handler(self, event: EventType,):

        def decorator(callback: typing.Callable[['Client', 'Dispatcher', Event], None]):
            self.add_handler(event, callback)

            return callback

        return decorator