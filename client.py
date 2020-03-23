import socket
import threading
import time
import typing

from loguru import logger
from auth.seamles_login import seamles_login
from auth.silent_login import silent_login

from AMFBuffer import AMFBuffer
from dispatcher import Dispatcher
from tasks.task import MyTask


class Client:
    onstart_handlers: typing.List[typing.Callable[['Client', Dispatcher], None]]

    dispatcher: Dispatcher
    receiver: threading.Thread

    user_config: typing.Dict[str, typing.List[str]]

    user_id: str
    user_ccid: str
    user_key: str
    user_lang: str
    env: int


    def __init__(self, 
        login: str, 
        password: str, 
        user_name: str, 
        is_silent_login: bool = True
    ):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        
        self.dispatcher = None

        self.receiver = None
        self.user_key = ""

        self.onstart_handlers = []

        if (is_silent_login):
            user_config = silent_login(login, password, user_name)
        else:
            user_config = seamles_login(user_name)

        
        self.host = user_config.get('host')[0]
        self.port = int(user_config.get('port')[0])

        self.user_id = user_config.get('cid')[0]
        self.user_ccid = user_config.get('ccid')[0]
        self.user_key = user_config.get('key')[0]
        self.user_lang = user_config.get('lang')[0]
        self.env = int(user_config.get('env')[0])


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
