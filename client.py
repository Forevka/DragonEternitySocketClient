from models.UserGlobal import UserGlobal
from auth.models.login import User
from models.game_state.Fight import Fight
import socket
import threading
import time
import typing

from loguru import logger
from models.UserConfig import UserConfig
from auth.seamles_login import seamles_login
from auth.silent_login import silent_login

from AMFBuffer import AMFBuffer
from dispatcher import Dispatcher


class Client:
    onstart_handlers: typing.List[typing.Callable[['Client', Dispatcher], None]]

    dispatcher: Dispatcher

    user_config: UserConfig

    sequence_list: typing.Any
    sequence_counter: int

    global_fight_state: Fight
    global_user_state: UserGlobal

    def __init__(self, 
        login: str, 
        password: str, 
        user_name: str, 
        is_silent_login: bool = True
    ):
        self.sequence_counter = 0
        self.sequence_list = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False

        self.user_key = ""

        self.onstart_handlers = []
        '''
        if (is_silent_login):
            self.user_config = silent_login(login, password, user_name)
        else:
            self.user_config = seamles_login(login, password, user_name)
        '''


    def onstart(self,):
        def decorator(callback: typing.Callable[['Client', Dispatcher], None]):
            self.onstart_handlers.append(callback)

            return callback

        return decorator

    def start(self,):
        logger.debug('Client connecting...')
        try:
            self.socket.connect((self.user_config.host, self.user_config.port))
            self.is_connected = True
            logger.debug('Client connected!')

            logger.debug('Invoking on start handlers')
            for callback in self.onstart_handlers:
                logger.debug(f'Invoking {callback.__name__} handler')
                callback(self, self.dispatcher)
            
        except socket.error as err:
            logger.debug('Can`t connect ', err)

        logger.debug('Starting tasks')
        self.dispatcher._start_tasks()
        logger.debug('Tasks started!')

        self.receive()

    def set_dispatcher(self, disp: Dispatcher,):
        self.dispatcher = disp

    def send(self, buffer: AMFBuffer,):
        buffer.encode()
        self.socket.sendall(buffer.buffer)
    
    def send_rpc(self, buffer: AMFBuffer,):
        self.sequence_counter += 1
        buffer['seq'] = self.sequence_counter

        self.send(buffer)


    def receive(self,):
        while True:
            try:
                data = self.socket.recv(1024 * 256)
                buffer = AMFBuffer()
            
                #length = data[:4]
                #print(length)
                #length = int.from_bytes(bytes=length, byteorder='big')
                #print(length)

                updates = buffer.decode(data[4:])
                self.dispatcher.dispatch(updates)
            except KeyboardInterrupt as kb_interrupt:
                logger.info('Stopping client...')
                self.socket.close()
                self.is_connected = False
                logger.info('Stopping tasks...')
                self.dispatcher._stop_tasks()
                logger.info('Stopped')
                break


