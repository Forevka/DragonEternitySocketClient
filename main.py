from dispatcher import Dispatcher
from client import Client
import random
from AMFFactory import command
from config import HOST, PORT
from loguru import logger
from models.BaseEvent import Event
from models.ChatMessage import ChatMessage
from events import EventType
from auth.seamles_login import seamles_login
from auth.silent_login import silent_login

client = Client(HOST, PORT)
dp = Dispatcher(client)

client.set_dispatcher(dp)

@client.onstart()
def enter(client: Client, dp: Dispatcher,):
    def randomString(stringLength = 12):
        """Generate a random string of fixed length """
        letters = '123456789ABCDEF'
        return ''.join(random.choice(letters) for i in range(stringLength))

    logger.info(client.user_key)

    a = command('enter')
    a['env'] = 1
    a['key'] = client.user_key
    a['ccid'] = randomString()#'4D4BCF747B3C'
    a['lang'] = 'ru'
    a['cid'] = '21128101'
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
    #user_key = silent_login('TEST_KILL')
    user_key = seamles_login()
    logger.info(user_key)
    client.start(user_key)