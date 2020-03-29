from datetime import datetime
from enums.damage_type import DamageType
from db.item_info import ItemInfoDB
from models.ItemInfo import ItemInfo
from models.FightResults import FightResults
from enums.attacks.attacks import Attack
from models.NewRound import NewRound
from models.AttackNow import AttackNow
from models.UserGlobal import UserGlobal
from auth.models.login import User
from models.game_state.Fight import Fight, UserInFight
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
from models.Cast import Cast

client = Client(LOGIN, PASSWORD, 'TEST_KILL', is_silent_login=True)

client.user_config = UserConfig()

client.user_config.host = "game2.drako.ru"
client.user_config.port = 7701
client.user_config.env = 1
client.user_config.user_key = "cd497537693f58643b4c6636ff3839ed"
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
def attack_now_handler(client: Client, dp: Dispatcher, event: Event):
    attack_now = AttackNow.from_dict(event.data)
    
    if (attack_now.pers_id == client.global_fight_state.me.cid):
        logger.warning('need to attack!')

        elixir = client.global_fight_state.me.get_elixir_for_heal()

        hp_procent = (attack_now.hp / client.global_fight_state.me.max_hp) * 100

        if (hp_procent < 50):
            if (elixir is not None):
                cmd = command('castSpell')
                cmd['srcType'] = elixir.src_type # always 2
                cmd['srcId'] = elixir.src_id
                cmd['targetId'] = client.global_fight_state.me.cid

                client.send(cmd)

        spell = client.global_fight_state.me.get_spell(attack_now.mp, can_be_auxilary=False)

        

        logger.warning(f'Current hp procent: {round(hp_procent, 2)}')
        logger.warning(f'Current mp: {attack_now.mp}')
        if (spell):
            logger.warning(f'Can cast spell: {spell.get("title", "")}')
        else:
            logger.warning(f'Cant cast any spell')


        if (spell is not None):
            logger.warning(f'Casting spell')
            cmd = command('castSpell')
            cmd['srcType'] = 3
            cmd['srcId'] = spell.get('id')
            cmd['targetId'] = client.global_fight_state.opp.cid
            cmd['key'] = '1#1'
            
            client.send(cmd)
        else:
            logger.warning(f'Physic attack')
            cmd = command('castSpell')
            cmd['srcType'] = 1
            cmd['srcId'] = Attack.Mana.value
            cmd['targetId'] = client.global_fight_state.opp.cid

            client.send(cmd)




@dp.handler(EventType.FightState)
def fight_state(client: Client, dp: Dispatcher, event: Event):
    client.global_fight_state = Fight.load(event.data)
    logger.warning(str(client.global_fight_state))

    cmd = command('fightReady')
    client.send(cmd)

@dp.handler(EventType.NewRound)
def fight_state(client: Client, dp: Dispatcher, event: Event):
    new_round = NewRound.from_dict(event.data)

    #if (new_round.pers_id != client.global_fight_state.me.cid):
    #    client.global_fight_state.opp_id = new_round.pers_id


@dp.handler(EventType.OppNew)
def new_opponent(client: Client, dp: Dispatcher, event: Event):
    #opponent_new = OpponentNew.from_dict(event.data)
    logger.warning('new opponent')
    client.global_fight_state.opp = UserInFight.load_user(event.data)

@dp.handler(EventType.ObsNew)
def new_obs(client: Client, dp: Dispatcher, event: Event):
    new_ally = NewAlly.from_dict(event.data)
    ...

@dp.handler(EventType.UserInfo)
def user_info(client: Client, dp: Dispatcher, event: Event):
    #a = command('attackBot')
    #a['id'] = 6

    #client.send(a)

    a = command('auctionQuery')
    a['order'] = 'buyout'
    #a['kindId'] = 896
    a['categoryId'] = 8398

    client.send(a)

@dp.handler(EventType.Lots)
def handle_lots(client: Client, dp: Dispatcher, event: Event):
    for i in event.data.get('lots'):
        logger.warning(i)
        logger.warning(i.item.item_info())

@dp.handler(EventType.ItemInfo)
def item_info(client: Client, dp: Dispatcher, event: Event):
    res = ItemInfo.from_dict(event.data)
    item_info_db = ItemInfoDB.get_instance().add_item(res)


@dp.handler(EventType.FightResults)
def fight_results(client: Client, dp: Dispatcher, event: Event):
    res = FightResults.from_dict(event.data)
    item_info_db = ItemInfoDB.get_instance()

    report = f"{datetime.now().strftime('%Y/%m/%d, %H:%M:%S')}\nБой {res.fight_title} закончен: <b>{'Победа' if res.team == res.winner_team else 'Проигрыш'}</b> <a href='https://drako.ru/game/fight.php?id={res.fight_id}'>ссылка</a>"
    report += f"\nУрон: {res.dmg} Exp: {res.exp} Money: {res.money}"
    report += f"\nДроп: "
    for i in res.drop_items:
        report += f'\t\n {item_info_db.get_item_description(i.item_id).get("title", "")} - {i.count}'

    client.log_telegram(report)
    a = 1


@dp.handler(EventType.Cast)
def damage(client: Client, dp: Dispatcher, event: Event):
    cast = Cast.from_dict(event.data)

    resist = {}
    resist[0] = ' '
    resist[1] = ' (resisted 25%)'
    resist[2] = ' (resisted 50%)'
    resist[3] = ' (resisted 50%)'

    report = ''

    for dmg in cast.events:
        if dmg.evt == 'damage':
            report += f'\nUser {dmg.pers_id} damaged {dmg.target_id} for {dmg.hp} with {DamageType(dmg.dmg_type)}' + str(resist[dmg.armor]) + ('(blocked)' if dmg.block else '') + ('(critical)' if dmg.crit else '')
        elif dmg.evt == 'heal':
            report += f'\nUser {dmg.pers_id} healed {dmg.target_id} for {dmg.hp} with {DamageType(dmg.dmg_type)}' + str(resist[dmg.armor]) + ('(blocked)' if dmg.block else '') + ('(critical)' if dmg.crit else '')

    logger.warning(report)

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
