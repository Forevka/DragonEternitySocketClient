from __future__ import annotations
from enums.events.events import EventType
from fsm.finite_state_machine import UserState
import typing

from loguru import logger

from models.BaseEvent import Event, Update
from tasks.task import MyTask

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
    tasks: typing.Dict[int, MyTask]

    user_state: UserState

    def __init__(self, client: 'Client'):
        self.client = client
        
        self.handlers = {}
        self.tasks = {}
    
    def add_task(self, task: typing.Callable[['Client', 'Dispatcher'], None], timeout: int):
        task_id = len(self.tasks)

        task_thread = MyTask(task, task_id, timeout, self.client, self)

        self.tasks[task_id] = task_thread
        if (self.client.is_connected):
            task_thread.start()

        return task_id

    def _start_tasks(self,):
        for i in self.tasks.values():
            i.start()

    def _stop_tasks(self,):
        for i in self.tasks.values():
            i.cancel()

    def task(self, timeout: int,):

        def decorator(callback: typing.Callable[['Client', Dispatcher], None]):
            self.add_task(callback, timeout)

            return callback

        return decorator

    def dispatch(self, updates: Update):
        for event in updates.events:
            logger.debug(f'Event {event.event} seq {event.seq}')
            print(event.data) #TradeOppConfirm
            for handler in self.handlers.get(EventType[upperfirst(event.event)], []):
                handler(self.client, self, event)

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
