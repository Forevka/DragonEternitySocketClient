from models.UserGlobal import UserGlobal
from auth.models.login import User
from models.game_state.Fight import Fight
import time
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
from models.FightState import FightState
from models.OpponentNew import OpponentNew
from models.AttackWait import AttackWait
from models.NewAlly import NewAlly

client = Client(LOGIN, PASSWORD, 'TEST_KILL', is_silent_login=True)

client.user_config = UserConfig()

client.user_config.host = "game2.drako.ru"
client.user_config.port = 7701
client.user_config.env = 1
client.user_config.user_key = "fae0b38de0ed5093fbd8aeb9d23965df"
client.user_config.user_ccid = "5D4BCF747B3C"
client.user_config.user_lang = "ru"
client.user_config.user_id = "21262955"
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

#@dp.handler(EventType.AreaBots)
#def attack_bot(client: Client, dp: Dispatcher, event: Event):
#    a = command('attackBot')
#    a['id'] = 6

#    client.send(a)

@dp.handler(EventType.AttackWait)
def attack_wait(client: Client, dp: Dispatcher, event: Event):
    attack_wait = AttackWait.from_dict(event.data)
    logger.warning('waiting for opponent attack...')


@dp.handler(EventType.AttackNow)
def attack_now(client: Client, dp: Dispatcher, event: Event):
    persId = event.data.get('persId', -1)
    if (persId == client.global_fight_state.me.cid):
        logger.warning('need to attack!')
        cmd = command('castSpell')
        cmd['srcType'] = 1
        cmd['srcId'] = 2
        cmd['targetId'] = 2

        client.send(cmd)




@dp.handler(EventType.FightState)
def fight_state(client: Client, dp: Dispatcher, event: Event):
    client.global_fight_state = Fight.load(event.data)
    logger.warning(str(client.global_fight_state))

    cmd = command('fightReady')
    client.send(cmd)

@dp.handler(EventType.NewRound)
def fight_state(client: Client, dp: Dispatcher, event: Event):
    ...

@dp.handler(EventType.OppNew)
def new_opponent(client: Client, dp: Dispatcher, event: Event):
    opponent_new = OpponentNew.from_dict(event.data)

@dp.handler(EventType.ObsNew)
def new_obs(client: Client, dp: Dispatcher, event: Event):
    new_ally = NewAlly.from_dict(event.data)
    ...

@dp.handler(EventType.UserInfo)
def user_info(client: Client, dp: Dispatcher, event: Event):
    a = command('attackBot')
    a['id'] = 6

    client.send(a)


@dp.handler(EventType.Damage)
def damage(client: Client, dp: Dispatcher, event: Event):
    ...

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
