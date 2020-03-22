import socket
import threading
import typing
import time

from loguru import logger

from AMFBuffer import AMFBuffer

from dispatcher import Dispatcher

class CancellationToken:
    cancel_requested: bool = False

    def cancel(self,):
        self.cancel_requested = True

class Client:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        
        self.dispatcher: Dispatcher = None

        self.receiver: threading.Thread = None

        self.tasks: typing.Dict[int, MyTask] = {}

        self.onstart_handlers: typing.List[typing.Callable[[Client, Dispatcher], None]] = []

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

    def set_dispatcher(self, disp: Dispatcher):
        self.dispatcher = disp

    def send(self, buffer: AMFBuffer,):
        buffer.encode()
        self.socket.sendall(buffer.buffer)

    def receive(self,):
        while True:
            data = self.socket.recv(1024 * 256)
            self.dispatcher.dispatch(data, self)


class MyTask(threading.Thread):
    task: typing.Callable[[Client, Dispatcher], None]
    cancelation_source: CancellationToken
    task_id: int
    timeout: int
    client: Client
    dp: Dispatcher

    def __init__(
        self, 
        task: typing.Callable[[Client, Dispatcher], None], 
        task_id: int,
        timeout: int,
        client: Client,
        dp: Dispatcher
    ):
        threading.Thread.__init__(self)

        self.timeout = timeout
        self.task = task
        self.task_id = task_id
        self.client = client
        self.dp = dp

        self.cancelation_source = CancellationToken()
    
    def cancel(self,):
        self.cancelation_source.cancel()

    def run(self,):
        logger.debug(f'Task {self.task_id} started')
        while (self.cancelation_source.cancel_requested == False):
            if (self.client.is_connected == False):
                logger.debug('Client is not connected waiting for next tick...')
                time.sleep(self.timeout)
                continue
            self.task(self.client, self.dp)
            time.sleep(self.timeout)