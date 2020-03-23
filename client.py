import socket
import threading
import time
import typing

from loguru import logger

from AMFBuffer import AMFBuffer
from dispatcher import Dispatcher
from tasks.task import MyTask


class Client:
    onstart_handlers: typing.List[typing.Callable[['Client', Dispatcher], None]]
    user_key: str

    dispatcher: Dispatcher
    receiver: threading.Thread

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        
        self.dispatcher = None

        self.receiver = None
        self.user_key = ""

        self.onstart_handlers = []

    def onstart(self,):
        def decorator(callback: typing.Callable[['Client', Dispatcher], None]):
            self.onstart_handlers.append(callback)

            return callback

        return decorator

    def start(self, user_key: str):
        self.user_key = user_key

        logger.debug('Client connecting...')
        try:
            self.socket.connect((self.host, self.port))
            self.is_connected = True
            logger.debug('Client connected!')

            logger.debug('Invoking on start handlers')
            for callback in self.onstart_handlers:
                logger.debug(f'Invoking {callback.__name__} handler')
                callback(self, self.dispatcher)
            
        except socket.error as err:
            logger.debug('Can`t connect ', err)
        
        self.receiver = threading.Thread(target=self.receive,)
        self.receiver.start()

        logger.debug('Starting tasks')
        self.dispatcher._start_tasks()
        logger.debug('Tasks started!')

    def set_dispatcher(self, disp: Dispatcher,):
        self.dispatcher = disp

    def send(self, buffer: AMFBuffer,):
        buffer.encode()
        self.socket.sendall(buffer.buffer)

    def receive(self,):
        while True:
            data = self.socket.recv(1024 * 256)
            buffer = AMFBuffer()
        
            #length = data[:4]
            #print(length)
            #length = int.from_bytes(bytes=length, byteorder='big')
            #print(length)

            updates = buffer.decode(data[4:])
            self.dispatcher.dispatch(updates, self)
