from datetime import datetime
from utils.item_info_dump import LotItemDB
from models.UserGlobal import UserGlobal
from models.game_state.Fight import Fight
from models.UserConfig import UserConfig
from loguru import logger

from AMFFactory import command
from client import Client
from config import LOGIN, PASSWORD
from dispatcher import Dispatcher
from enums.events.events import EventType
from fsm.finite_state_machine import UserState
from models.BaseEvent import Event
from models.ChatMessage import ChatMessage
from db.item_kinds_db import ItemKindDB
from time import sleep

client = Client(LOGIN, PASSWORD, 'TEST_KILL', is_silent_login=True)

client.user_config = UserConfig()
client.user_config.in_game = False
client.user_config.host = "game2.drako.ru"
client.user_config.port = 7704
client.user_config.env = 2
client.user_config.user_key = "5c34012a7478d263c1ec30ade7503d5c"
client.user_config.user_ccid = "5D4BCF747B3C"
client.user_config.user_lang = "ru"
client.user_config.user_id = "21263678"

client.global_fight_state = Fight()
client.global_user_state = UserGlobal()

dp = Dispatcher(client)

client.set_dispatcher(dp)

state = UserState()
state.state(UserState.StartState.Welcome)


@client.onstart()
def enter(client: Client, dp: Dispatcher,):
    a = command('enter')
    a['env'] = client.user_config.env
    a['key'] = client.user_config.user_key
    a['ccid'] = client.user_config.user_ccid
    a['lang'] = client.user_config.user_lang
    a['cid'] = client.user_config.user_id

    client.send(a)
    

@dp.task(5)
def ping(client: Client, dp: Dispatcher,):
    a = command('ping')

    client.send(a)


@dp.task(5)
def dump_auc(client: Client, dp: Dispatcher):
    if client.user_config.in_game:
        client.log_telegram(f"{datetime.now().strftime('%Y/%m/%d, %H:%M:%S')}: Start dumping auction...")
        all_kinds = ItemKindDB.get_instance().get_all_kinds()
        for n, i in enumerate(all_kinds):
            a = command('auctionQuery')
            a['order'] = 'time'
            a['kindId'] = i
            #a['categoryId'] = 8398

            client.send(a)
            logger.debug(f'sent {i} auctionQuery {n}/{len(all_kinds)}')
            sleep(2)
        
        client.log_telegram(f"{datetime.now().strftime('%Y/%m/%d, %H:%M:%S')}: Auction dumped!")



@dp.handler(EventType.UserInfo)
def user_info(client: Client, dp: Dispatcher, event: Event):
    client.user_config.in_game = True

@dp.handler(EventType.Lots)
def handle_lots(client: Client, dp: Dispatcher, event: Event):
    logger.warning('LOTS')
    db = LotItemDB.get_instance()
    for i in event.data.get('lots'):
        db.write_lot(i)
    
    db.commit()


@dp.handler(EventType.ChatMessage)
def chat_handler(client: Client, dp: Dispatcher, event: Event):
    parsed_event = ChatMessage.from_dict(event)

    logger.debug(f"{parsed_event.chat_message_from}: {parsed_event.msg}")

@dp.handler(EventType.Ping)
def ping_handler(client: Client, dp: Dispatcher, event: Event):
    ...



if __name__ == "__main__":
    client.start()
