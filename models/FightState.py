from dataclasses import dataclass
from typing import Any, List, Optional, Dict, TypeVar, Callable, Type, cast
from uuid import UUID


T = TypeVar("T")


def from_int(x: Any) -> int:
    if (x is not None):
        return int(x)
    return -1


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    return str(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


@dataclass
class PersList:
    bot_tpl_id: int
    dead: bool
    id: int
    kind: int
    level: int
    nick: str
    norm_nick: str
    rank: int
    rank2: int
    register_lang: str
    state: int
    team: int
    unbound: bool

    @staticmethod
    def from_dict(obj: Any) -> 'PersList':
        assert isinstance(obj, dict)
        bot_tpl_id = from_int(obj.get("botTplId"))
        dead = from_bool(obj.get("dead"))
        id = from_int(obj.get("id"))
        kind = from_int(obj.get("kind"))
        level = from_int(obj.get("level"))
        nick = from_str(obj.get("nick"))
        norm_nick = from_str(obj.get("normNick"))
        rank = from_int(obj.get("rank"))
        rank2 = from_int(obj.get("rank2"))
        register_lang = from_str(obj.get("registerLang"))
        state = from_int(obj.get("state"))
        team = from_int(obj.get("team"))
        unbound = from_bool(obj.get("unbound"))
        return PersList(bot_tpl_id, dead, id, kind, level, nick, norm_nick, rank, rank2, register_lang, state, team, unbound)

    def to_dict(self) -> dict:
        result: dict = {}
        result["botTplId"] = from_int(self.bot_tpl_id)
        result["dead"] = from_bool(self.dead)
        result["id"] = from_int(self.id)
        result["kind"] = from_int(self.kind)
        result["level"] = from_int(self.level)
        result["nick"] = from_str(self.nick)
        result["normNick"] = from_str(self.norm_nick)
        result["rank"] = from_int(self.rank)
        result["rank2"] = from_int(self.rank2)
        result["registerLang"] = from_str(self.register_lang)
        result["state"] = from_int(self.state)
        result["team"] = from_int(self.team)
        result["unbound"] = from_bool(self.unbound)
        return result


@dataclass
class Outward:
    looks: List[int]

    @staticmethod
    def from_dict(obj: Any) -> 'Outward':
        assert isinstance(obj, dict)
        looks = from_list(from_int, obj.get("looks"))
        return Outward(looks)

    def to_dict(self) -> dict:
        result: dict = {}
        result["looks"] = from_list(from_int, self.looks)
        return result


@dataclass
class The1:
    item_tpl_id: int
    src_id: int
    src_type: int

    @staticmethod
    def from_dict(obj: Any) -> 'The1':
        assert isinstance(obj, dict)
        item_tpl_id = from_int(obj.get("itemTplId"))
        src_id = from_int(obj.get("srcId"))
        src_type = from_int(obj.get("srcType"))
        return The1(item_tpl_id, src_id, src_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["itemTplId"] = from_int(self.item_tpl_id)
        result["srcId"] = from_int(self.src_id)
        result["srcType"] = from_int(self.src_type)
        return result


@dataclass
class The5_E791:
    cnt: int
    item_tpl_id: int
    src_id: UUID
    src_type: int

    @staticmethod
    def from_dict(obj: Any) -> 'The5_E791':
        assert isinstance(obj, dict)
        cnt = from_int(obj.get("cnt"))
        item_tpl_id = from_int(obj.get("itemTplId"))
        src_id = UUID(obj.get("srcId"))
        src_type = from_int(obj.get("srcType"))
        return The5_E791(cnt, item_tpl_id, src_id, src_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cnt"] = from_int(self.cnt)
        result["itemTplId"] = from_int(self.item_tpl_id)
        result["srcId"] = str(self.src_id)
        result["srcType"] = from_int(self.src_type)
        return result


@dataclass
class Spell:
    the_1: Optional[The1] = None
    the_2: Optional[The1] = None
    the_3: Optional[The1] = None
    the_8: Optional[The1] = None
    the_9: Optional[The1] = None
    the_5_e791875_4_c96_0101_ea9_a_a64_b772_eda4_e: Optional[The5_E791] = None
    the_5_e79195_f_532_b_0101_ab25_3267_a830_db82: Optional[The5_E791] = None
    the_5_e7917_e8_4924010156_fa_77534_ed2_b5_f0: Optional[The5_E791] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Spell':
        assert isinstance(obj, dict)
        the_1 = from_union([The1.from_dict, from_none], obj.get("1"))
        the_2 = from_union([The1.from_dict, from_none], obj.get("2"))
        the_3 = from_union([The1.from_dict, from_none], obj.get("3"))
        the_8 = from_union([The1.from_dict, from_none], obj.get("8"))
        the_9 = from_union([The1.from_dict, from_none], obj.get("9"))
        the_5_e791875_4_c96_0101_ea9_a_a64_b772_eda4_e = from_union([The5_E791.from_dict, from_none], obj.get("5e791875-4c96-0101-ea9a-a64b772eda4e"))
        the_5_e79195_f_532_b_0101_ab25_3267_a830_db82 = from_union([The5_E791.from_dict, from_none], obj.get("5e79195f-532b-0101-ab25-3267a830db82"))
        the_5_e7917_e8_4924010156_fa_77534_ed2_b5_f0 = from_union([The5_E791.from_dict, from_none], obj.get("5e7917e8-4924-0101-56fa-77534ed2b5f0"))
        return Spell(the_1, the_2, the_3, the_8, the_9, the_5_e791875_4_c96_0101_ea9_a_a64_b772_eda4_e, the_5_e79195_f_532_b_0101_ab25_3267_a830_db82, the_5_e7917_e8_4924010156_fa_77534_ed2_b5_f0)

    def to_dict(self) -> dict:
        result: dict = {}
        result["1"] = from_union([lambda x: to_class(The1, x), from_none], self.the_1)
        result["2"] = from_union([lambda x: to_class(The1, x), from_none], self.the_2)
        result["3"] = from_union([lambda x: to_class(The1, x), from_none], self.the_3)
        result["8"] = from_union([lambda x: to_class(The1, x), from_none], self.the_8)
        result["9"] = from_union([lambda x: to_class(The1, x), from_none], self.the_9)
        result["5e791875-4c96-0101-ea9a-a64b772eda4e"] = from_union([lambda x: to_class(The5_E791, x), from_none], self.the_5_e791875_4_c96_0101_ea9_a_a64_b772_eda4_e)
        result["5e79195f-532b-0101-ab25-3267a830db82"] = from_union([lambda x: to_class(The5_E791, x), from_none], self.the_5_e79195_f_532_b_0101_ab25_3267_a830_db82)
        result["5e7917e8-4924-0101-56fa-77534ed2b5f0"] = from_union([lambda x: to_class(The5_E791, x), from_none], self.the_5_e7917_e8_4924010156_fa_77534_ed2_b5_f0)
        return result


@dataclass
class PersSelf:
    dead: bool
    dmg: int
    effects: List[Any]
    fight_graph_point_id: int
    gender: int
    have_dragon: bool
    hp: int
    id: int
    level: int
    max_hp: int
    max_mp: int
    mp: int
    next_stands: List[Any]
    nick: str
    norm_nick: str
    outward: Outward
    pair_state: List[Any]
    parts: List[Any]
    register_lang: str
    round: int
    spell_cd: List[Any]
    spell_costs: List[Any]
    spell_gcd_time: float
    spell_used_cnt: List[Any]
    spells: Dict[str, Spell]
    stand: int
    team: int
    trend: int

    @staticmethod
    def from_dict(obj: Any) -> 'PersSelf':
        assert isinstance(obj, dict)
        dead = from_bool(obj.get("dead"))
        dmg = from_int(obj.get("dmg"))
        effects = from_list(lambda x: x, obj.get("effects"))
        fight_graph_point_id = from_int(obj.get("fightGraphPointId"))
        gender = from_int(obj.get("gender"))
        have_dragon = from_bool(obj.get("haveDragon"))
        hp = from_int(obj.get("hp"))
        id = from_int(obj.get("id"))
        level = from_int(obj.get("level"))
        max_hp = from_int(obj.get("maxHp"))
        max_mp = from_int(obj.get("maxMp"))
        mp = from_int(obj.get("mp"))
        next_stands = obj.get("nextStands", {})
        nick = from_str(obj.get("nick"))
        norm_nick = from_str(obj.get("normNick"))
        outward = Outward.from_dict(obj.get("outward"))
        pair_state = obj.get("pairState", {})
        parts = from_list(lambda x: x, obj.get("parts"))
        register_lang = from_str(obj.get("registerLang"))
        round = from_int(obj.get("round"))
        spell_cd = from_list(lambda x: x, obj.get("spellCd"))
        spell_costs = from_list(lambda x: x, obj.get("spellCosts"))
        spell_gcd_time = from_float(obj.get("spellGcdTime"))
        spell_used_cnt = from_list(lambda x: x, obj.get("spellUsedCnt"))
        spells = from_dict(Spell.from_dict, obj.get("spells"))
        stand = from_int(obj.get("stand"))
        team = from_int(obj.get("team"))
        trend = from_int(obj.get("trend"))
        return PersSelf(dead, dmg, effects, fight_graph_point_id, gender, have_dragon, hp, id, level, max_hp, max_mp, mp, next_stands, nick, norm_nick, outward, pair_state, parts, register_lang, round, spell_cd, spell_costs, spell_gcd_time, spell_used_cnt, spells, stand, team, trend)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dead"] = from_bool(self.dead)
        result["dmg"] = from_int(self.dmg)
        result["effects"] = from_list(lambda x: x, self.effects)
        result["fightGraphPointId"] = from_int(self.fight_graph_point_id)
        result["gender"] = from_int(self.gender)
        result["haveDragon"] = from_bool(self.have_dragon)
        result["hp"] = from_int(self.hp)
        result["id"] = from_int(self.id)
        result["level"] = from_int(self.level)
        result["maxHp"] = from_int(self.max_hp)
        result["maxMp"] = from_int(self.max_mp)
        result["mp"] = from_int(self.mp)
        result["nextStands"] = from_list(lambda x: x, self.next_stands)
        result["nick"] = from_str(self.nick)
        result["normNick"] = from_str(self.norm_nick)
        result["outward"] = to_class(Outward, self.outward)
        result["pairState"] = from_list(lambda x: x, self.pair_state)
        result["parts"] = from_list(lambda x: x, self.parts)
        result["registerLang"] = from_str(self.register_lang)
        result["round"] = from_int(self.round)
        result["spellCd"] = from_list(lambda x: x, self.spell_cd)
        result["spellCosts"] = from_list(lambda x: x, self.spell_costs)
        result["spellGcdTime"] = to_float(self.spell_gcd_time)
        result["spellUsedCnt"] = from_list(lambda x: x, self.spell_used_cnt)
        result["spells"] = from_dict(lambda x: to_class(Spell, x), self.spells)
        result["stand"] = from_int(self.stand)
        result["team"] = from_int(self.team)
        result["trend"] = from_int(self.trend)
        return result


@dataclass
class FightState:
    area_id: int
    arena_area_id: int
    evt: str
    finished: bool
    id: UUID
    level: int
    pers_list: List[PersList]
    pers_self: PersSelf
    pvp: bool
    started: bool
    title: str

    @staticmethod
    def from_dict(obj: Any) -> 'FightState':
        assert isinstance(obj, dict)
        area_id = from_int(obj.get("areaId"))
        arena_area_id = from_int(obj.get("arenaAreaId"))
        evt = from_str(obj.get("evt"))
        finished = from_bool(obj.get("finished"))
        id = UUID(obj.get("id"))
        level = from_int(obj.get("level"))
        pers_list = from_list(PersList.from_dict, obj.get("persList"))
        pers_self = PersSelf.from_dict(obj.get("persSelf"))
        pvp = from_bool(obj.get("pvp"))
        started = from_bool(obj.get("started"))
        title = from_str(obj.get("title"))
        return FightState(area_id, arena_area_id, evt, finished, id, level, pers_list, pers_self, pvp, started, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["areaId"] = from_int(self.area_id)
        result["arenaAreaId"] = from_int(self.arena_area_id)
        result["evt"] = from_str(self.evt)
        result["finished"] = from_bool(self.finished)
        result["id"] = str(self.id)
        result["level"] = from_int(self.level)
        result["persList"] = from_list(lambda x: to_class(PersList, x), self.pers_list)
        result["persSelf"] = to_class(PersSelf, self.pers_self)
        result["pvp"] = from_bool(self.pvp)
        result["started"] = from_bool(self.started)
        result["title"] = from_str(self.title)
        return result


def fight_state_from_dict(s: Any) -> FightState:
    return FightState.from_dict(s)


def fight_state_to_dict(x: FightState) -> Any:
    return to_class(FightState, x)
