import random

from loguru import logger

from AMFFactory import command
from client import Client
from config import LOGIN, PASSWORD
from dispatcher import Dispatcher
from events import EventType
from models.BaseEvent import Event
from models.ChatMessage import ChatMessage

client = Client(LOGIN, PASSWORD, 'TEST_KILL', is_silent_login=True)
dp = Dispatcher(client)

client.set_dispatcher(dp)

@client.onstart()
def enter(client: Client, dp: Dispatcher,):
    logger.info(client.user_key)

    a = command('enter')
    a['env'] = client.env
    a['key'] = client.user_key
    a['ccid'] = client.user_ccid
    a['lang'] = client.user_lang
    a['cid'] = client.user_id
    a['seq'] = 1

    client.send(a)

@dp.task(5)
def ping(client: Client, dp: Dispatcher,):
    a = command('ping')
    client.send(a)

@dp.handler(EventType.ChatMessage)
def chat_handler(client: Client, dp: Dispatcher, event: Event):
    event = ChatMessage.from_dict(event)

    logger.debug(f"{event.chat_message_from}: {event.msg}")

@dp.handler(EventType.Enter)
def enter_handler(client: Client, dp: Dispatcher, event: Event):
    logger.debug(event)

@dp.handler(EventType.Ping)
def ping_handler(client: Client, dp: Dispatcher, event: Event):
    logger.debug(f'ping {event}')

if __name__ == "__main__":
    client.start()
