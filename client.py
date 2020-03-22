import socket
import typing
import time

from loguru import logger

from AMFBuffer import AMFBuffer

from dispatcher import Dispatcher
from tasks.task import MyTask
import threading


class Client:
    onstart_handlers: typing.List[typing.Callable[['Client', Dispatcher], None]]
    tasks: typing.Dict[int, 'MyTask']

    dispatcher: Dispatcher
    receiver: threading.Thread

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        
        self.dispatcher = None

        self.receiver = None

        self.tasks = {}

        self.onstart_handlers = []

    def add_task(self, task: typing.Callable[['Client', Dispatcher], None], timeout: int):
        task_id = len(self.tasks)

        task_thread = MyTask(task, task_id, timeout, self, self.dispatcher)

        self.tasks[task_id] = task_thread
        if (self.is_connected):
            task_thread.run()

        return task_id

    def _start_tasks(self,):
        for i in self.tasks.values():
            i.run()

    def task(self, timeout: int,):

        def decorator(callback: typing.Callable[['Client', Dispatcher], None]):
            self.add_task(callback, timeout)

            return callback

        return decorator

    def onstart(self,):
        def decorator(callback: typing.Callable[['Client', Dispatcher], None]):
            self.onstart_handlers.append(callback)

            return callback

        return decorator

    def start(self,):
        logger.debug('Client connecting...')
        try:
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            logger.debug('Client connected!')

            logger.debug('Invoking on start handlers')
            for callback in self.onstart_handlers:
                logger.debug(f'Invoking {callback} handler')
                callback(self, self.dispatcher)
            
        except socket.error as err:
            logger.debug('Can`t connect ', err)
        
        self.receiver = threading.Thread(target=self.receive,)
        self.receiver.start()

        logger.debug('Starting tasks')
        self._start_tasks()
        logger.debug('Tasks started!')

    def set_dispatcher(self, disp: Dispatcher,):
        self.dispatcher = disp

    def send(self, buffer: AMFBuffer,):
        buffer.encode()
        self.socket.sendall(buffer.buffer)

    def receive(self,):
        while True:
            data = self.socket.recv(1024 * 256)
            self.dispatcher.dispatch(data, self)


