from datetime import date, datetime
from utils.item_info_dump import LotItemDB
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
from db.item_kinds_db import ItemKindDB
from time import sleep
from datetime import timedelta

client = Client(LOGIN, PASSWORD, 'TEST_KILL', is_silent_login=True)

client.user_config = UserConfig()

client.user_config.host = "game2.drako.ru"
client.user_config.port = 7704
client.user_config.env = 2
client.user_config.user_key = "85860adb9d7367e72e2712a233ce9d14"
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


@dp.task(1)
def start_fight(client: Client, dp: Dispatcher):
    logger.warning(f'is in fight {client.in_fight}')
    if (client.in_fight == False):
        logger.warning('not in fight now')
        logger.warning(f'last battle was in {client.last_fight_time.strftime("%Y/%m/%d, %H:%M:%S")}')
        logger.warning(f'current time {datetime.now().strftime("%Y/%m/%d, %H:%M:%S")}')
        logger.warning(f'next battle can be in {(timedelta(seconds=client.fight_cooldown) + client.last_fight_time).strftime("%Y/%m/%d, %H:%M:%S")}')
        if (timedelta(seconds=client.fight_cooldown) + client.last_fight_time) < datetime.now():
            logger.warning(f'! attacking')
            a = command('attackBot')
            a['id'] = 7

            client.send(a)
            client.in_fight = True

@dp.handler(EventType.AreaBots)
def attack_bot(client: Client, dp: Dispatcher, event: Event):
    #a = command('attackBot')
    #a['id'] = 6

    #client.send(a)
    ...
    



@dp.handler(EventType.PersListChange)
def pers_list_change(client: Client, dp: Dispatcher, event: Event):
    client.global_fight_state.update_pers(event.data)

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

        if (hp_procent < 45):
            if (elixir is not None):
                cmd = command('castSpell')
                cmd['srcType'] = elixir.src_type # always 2
                cmd['srcId'] = elixir.src_id
                cmd['targetId'] = client.global_fight_state.me.cid

                client.send(cmd)
                logger.warning(f'drink elixir of health')

        spell = client.global_fight_state.me.get_spell_by_name(attack_now.mp, 'огненный шар')#get_spell(attack_now.mp, can_be_auxilary=False)

        

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

    #client.in_fight = True

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
    ...


@dp.handler(EventType.ItemInfo)
def item_info(client: Client, dp: Dispatcher, event: Event):
    res = ItemInfo.from_dict(event.data)
    ItemInfoDB.get_instance().add_item(res)


@dp.handler(EventType.FightResults)
def fight_results(client: Client, dp: Dispatcher, event: Event):
    res = FightResults.from_dict(event.data)
    item_info_db = ItemInfoDB.get_instance()

    if (res.team == res.winner_team):
        client.fight_cooldown = 2
    else:
        client.fight_cooldown = 35

    report = f"{datetime.now().strftime('%Y/%m/%d, %H:%M:%S')}\nБой {res.fight_title} закончен: <b>{'Победа' if res.team == res.winner_team else 'Проигрыш'}</b> <a href='https://drako.ru/game/fight.php?id={res.fight_id}'>ссылка</a>"
    report += f"\nУрон: {res.dmg} Exp: {res.exp} Money: {res.money}"
    report += f"\nДроп: "
    for i in res.drop_items:
        report += f'\t\n {item_info_db.get_item_description(i.item_id).get("title", "")} - {i.count}'

    client.log_telegram(report)
    client.in_fight = False
    client.last_fight_time = datetime.now()
    #time.sleep(20)

    #a = command('attackBot')
    #a['id'] = 6

    #client.send(a)
    


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
        from_user = client.global_fight_state.get_by_id(dmg.pers_id)
        to_user = client.global_fight_state.get_by_id(dmg.target_id)

        if dmg.evt == 'damage':
            report += f'\nUser {from_user.get_name()} damaged {to_user.get_name()} for {dmg.hp} with {DamageType(dmg.dmg_type)}' + str(resist[dmg.armor]) + ('(blocked)' if dmg.block else '') + ('(critical)' if dmg.crit else '')
        elif dmg.evt == 'heal':
            report += f'\nUser {from_user.get_name()} healed {to_user.get_name()} for {dmg.hp} with {DamageType(dmg.dmg_type)}' + str(resist[dmg.armor]) + ('(blocked)' if dmg.block else '') + ('(critical)' if dmg.crit else '')

    logger.warning(report)

@dp.handler(EventType.ChatMessage)
def chat_handler(client: Client, dp: Dispatcher, event: Event):
    parsed_event = ChatMessage.from_dict(event)
    if (parsed_event.channel == 1):
        ...
    logger.debug(f"{parsed_event.chat_message_from}: {parsed_event.msg}")

@dp.handler(EventType.Enter)
def enter_handler(client: Client, dp: Dispatcher, event: Event):
    logger.debug(event)

@dp.handler(EventType.Ping)
def ping_handler(client: Client, dp: Dispatcher, event: Event):
    ...



if __name__ == "__main__":
    client.start()
