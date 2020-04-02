from db.bot_info_db import BotInfoDB
import random
from enums.target_type import TargetType
from db.items import ItemDB
from AMFFactory import command
from utils.parse import load_item_type
from models.game_state.FightItem import FightItem
from enums.items.consumable import Elixir, Orb
import typing
from enums.attacks import Magic, Attack, DeveloperItems, Nephelim


class UserInFight:
    cid: int

    is_dead: bool
    is_bot: bool
    bot_tpl_id: int

    have_dragon: bool

    hp: int
    max_hp: int
    mp: int
    max_mp: int

    level: int
    dmg: int

    team: int # can be 1 or 2

    nick: str

    fight_spells: typing.List[FightItem]

    physic_attacks: typing.List[FightItem]

    orbs: typing.List[FightItem]

    belt1: typing.List[FightItem]
    belt2: typing.List[FightItem]

    def get_spell(self, mp: int, can_be_auxilary: bool = False):
        db = ItemDB.get_instance()
        possible_magic = db.get_possible_magic([i.data.get('id', 0) for i in self.fight_spells])

        possible_by_mana = []

        for i in possible_magic:
            if i.get('spellManaCost', 9999) < mp:
                target_type = i.get('spellTargetType', 0)
                if (can_be_auxilary):
                    if (target_type in [TargetType.Auxilary, TargetType.Opponent]):
                        possible_by_mana.append(i)
                else:
                    if (target_type in [TargetType.Opponent]):
                        possible_by_mana.append(i)
        
        if possible_by_mana:
            return random.choice(possible_by_mana)
        
        return None
    
    def get_spell_by_name(self, mp: int, spell_name: str):
        db = ItemDB.get_instance()
        possible_magic = db.get_possible_magic([i.data.get('id', 0) for i in self.fight_spells])

        possible_by_mana = []

        for i in possible_magic:
            if i.get('spellManaCost', 9999) * 2 < mp:
                target_type = i.get('spellTargetType', 0)
                if (spell_name.lower() in i.get('title', '').lower()):
                    if (target_type in [TargetType.Auxilary, TargetType.Opponent]):
                        possible_by_mana.append(i)
        
        if possible_by_mana:
            return random.choice(possible_by_mana)
        
        return None


    def get_elixir_for_heal(self,) -> typing.Union[FightItem, None]:
        health_elixirs = [i for i in self.belt1 if 'эликсир жизни' in i.data.get('title', '').lower()]

        if (health_elixirs):
            return health_elixirs[0]

    def get_name(self,) -> str:
        if (self.is_bot):
            return BotInfoDB.get_instance().get_by_id(self.bot_tpl_id).get('title', '')
        
        return self.nick

    @staticmethod
    def load_spells(data: dict) -> typing.List:
        spells = []

        for m in data.values():
            item = FightItem()
            #item.item_type = load_item_type(m.get("itemTplId", 0))
            item.src_id = m.get("srcId", 0)
            item.src_type = m.get("srcType", 0)
            item.cnt = m.get("cnt", 0)
            item.data = ItemDB.get_instance().get_item(m.get("itemTplId", 0))

            spells.append(item)


        return spells

    @staticmethod
    def load_user(data: dict) -> 'UserInFight':
        u = UserInFight()
        u.nick = data.get("normNick", "")
        u.cid = data.get("id", 0)
        u.is_dead = data.get("dead", False)
        u.is_bot = data.get('bot', False)
        u.bot_tpl_id = data.get('botTplId', 0)
        u.have_dragon = data.get("haveDragon", False)
        u.hp = data.get("hp", 0)
        u.max_hp = data.get("maxHp", 0)
        u.mp = data.get("mp", 0)
        u.max_mp = data.get("max_mp", 0)
        u.level = data.get("level", 0)
        u.dmg = data.get('dmg', 0)
        u.team = data.get("team", 1)

        spells = data.get("spells", {})
        u.physic_attacks = UserInFight.load_spells(spells.get("1", {}))
        u.belt1 = UserInFight.load_spells(spells.get("2", {}))
        u.fight_spells = UserInFight.load_spells(spells.get("3", {}))
        u.orbs = UserInFight.load_spells(spells.get("4", {}))
        u.belt2 = UserInFight.load_spells(spells.get("5", {}))


        return u


class Fight:
    title: str

    is_pvp: bool
    fight_id: str

    opp_id: int    

    me: UserInFight
    opp: UserInFight

    users: typing.List[UserInFight] = []

    def __str__(self,):
        description = f"\n-- Fight {self.title} pvp {self.is_pvp} --"
        description += f"\nPossible attacks:\n\t"
        for i in self.me.physic_attacks:
            description += f"{i.data.get('title')}; "

        description += f"\nPossible magic:\n\t"
        for i in self.me.fight_spells:
            description += f"{i.data.get('title')}; "

        description += f"\nPossible orbs:\n\t"
        for i in self.me.orbs:
            description += f"{i.data.get('title')} {i.cnt}; "

        description += f"\nPossible belt1 item:\n\t"
        for i in self.me.belt1:
            description += f"{i.data.get('title')} {i.cnt}; "
            
        description += f"\nPossible belt2 item:\n\t"
        for i in self.me.belt2:
            description += f"{i.data.get('title')} {i.cnt}; "

        description += f"\nUsers in fight:"
        for i in self.users:
            description += f"\n\tid {i.cid} hp {i.hp}"
        
        return description

    @staticmethod
    def load(data: dict) -> 'Fight':
        f = Fight()
        f.title = data.get("title", "")
        f.is_pvp = data.get("pvp", False)
        f.fight_id = data.get("id", "")
        f.me = UserInFight.load_user(data.get("persSelf", {}))

        for i in data.get("persList", []):
            f.update_pers(i)

        return f

    def get_by_id(self, user_id):
        for i in self.users:
            if (i.cid == user_id):
                return i
        
        return None

    def update_pers(self, data):
        user = UserInFight.load_user(data)
        to_insert = None

        for num, i in enumerate(self.users):
            if i.cid == user.cid:
                to_insert = num
        
        if (to_insert is None):
            self.users.append(user)
        else:
            self.users[to_insert] = user
        