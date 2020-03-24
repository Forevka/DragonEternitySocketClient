import random

from loguru import logger

from AMFFactory import command
from client import Client
from config import LOGIN, PASSWORD
from dispatcher import Dispatcher
from events import EventType
from models.BaseEvent import Event
from models.ChatMessage import ChatMessage
from fsm.finite_state_machine import UserState

client = Client(LOGIN, PASSWORD, 'TEST_KILL', is_silent_login=True)
dp = Dispatcher(client)

client.set_dispatcher(dp)

@client.onstart()
def enter(client: Client, dp: Dispatcher,):
    logger.info(client.user_key)

    a = command('enter')
    a['env'] = client.user_config.env
    a['key'] = client.user_config.user_key
    a['ccid'] = client.user_config.user_ccid
    a['lang'] = client.user_config.user_lang
    a['cid'] = client.user_config.user_id
    a['seq'] = 1

    client.send(a)

@dp.task(5)
def ping(client: Client, dp: Dispatcher,):
    a = command('ping')
    client.send(a)

@dp.handler(EventType.AreaBots)
def attack_bot(client: Client, dp: Dispatcher, event: Event):
    a = command('attackBot')
    a['id'] = 6

    client.send(a)


@dp.handler(EventType.ChatMessage)
def chat_handler(client: Client, dp: Dispatcher, event: Event):
    parsed_event = ChatMessage.from_dict(event)

    logger.debug(f"{parsed_event.chat_message_from}: {parsed_event.msg}")

@dp.handler(EventType.Enter)
def enter_handler(client: Client, dp: Dispatcher, event: Event):
    logger.debug(event)

@dp.handler(EventType.Ping)
def ping_handler(client: Client, dp: Dispatcher, event: Event):
    ...



if __name__ == "__main__":
    client.start()
