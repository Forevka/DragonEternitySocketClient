from dispatcher import Dispatcher
from client import Client
from AMFFactory import command
from config import HOST, PORT
from loguru import logger
from models.BaseEvent import Event
from models.ChatMessage import ChatMessage
from events import EventType

client = Client(HOST, PORT)
dp = Dispatcher(client)

client.set_dispatcher(dp)

@client.onstart()
def enter(client: Client, dp: Dispatcher,):
    a = command('enter')
    a['env'] = 1
    a['key'] = '79ca025553b74445b1ac6020d6f00ecc'
    a['ccid'] = '5D4BCF747B3C'
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
    print(event)
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

    #client.add_task(ping, 5)

    #client.send(a.buffer)