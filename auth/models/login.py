from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable, Union
from utils.parse import from_bool, from_int, from_list, from_none, from_str, to_class

@dataclass
class DataCallback:
    pass

    @staticmethod
    def from_dict(obj: Any) -> 'DataCallback':
        assert isinstance(obj, dict)
        return DataCallback()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


@dataclass
class Session:
    logged_in: bool
    long_session: bool
    create_time: int
    validity: int
    update_interval: int
    additional_cookie_names: None
    data_callback: DataCallback
    name: str
    domain: str

    @staticmethod
    def from_dict(obj: Any) -> 'Session':
        assert isinstance(obj, dict)
        logged_in = from_bool(obj.get("loggedIn"))
        long_session = from_bool(obj.get("longSession"))
        create_time = from_int(obj.get("createTime"))
        validity = from_int(obj.get("validity"))
        update_interval = from_int(obj.get("updateInterval"))
        additional_cookie_names = from_none(obj.get("additionalCookieNames"))
        data_callback = DataCallback.from_dict(obj.get("dataCallback"))
        name = from_str(obj.get("name"))
        domain = from_str(obj.get("domain"))
        return Session(logged_in, long_session, create_time, validity, update_interval, additional_cookie_names, data_callback, name, domain)

    def to_dict(self) -> dict:
        result: dict = {}
        result["loggedIn"] = from_bool(self.logged_in)
        result["longSession"] = from_bool(self.long_session)
        result["createTime"] = from_int(self.create_time)
        result["validity"] = from_int(self.validity)
        result["updateInterval"] = from_int(self.update_interval)
        result["additionalCookieNames"] = from_none(self.additional_cookie_names)
        result["dataCallback"] = to_class(DataCallback, self.data_callback)
        result["name"] = from_str(self.name)
        result["domain"] = from_str(self.domain)
        return result


@dataclass
class User:
    norm_nick: str
    level: int
    gender: int
    kind: int
    clan_id: int
    clan: None
    rank: int
    rank_icon: None
    rank2: int
    rank2_icon: None
    flags: int
    access: int
    login_time: int
    ref_id: str
    referred_by: int
    shard: str
    reg_lang: str
    reg_platform: int
    sid: None
    session: Session
    uid: int
    nick: str

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        norm_nick = from_str(obj.get("normNick"))
        level = from_int(obj.get("level"))
        gender = from_int(obj.get("gender"))
        kind = from_int(obj.get("kind"))
        clan_id = from_int(obj.get("clanId"))
        clan = from_none(obj.get("clan"))
        rank = from_int(obj.get("rank"))
        rank_icon = from_none(obj.get("rankIcon"))
        rank2 = from_int(obj.get("rank2"))
        rank2_icon = from_none(obj.get("rank2Icon"))
        flags = from_int(obj.get("flags"))
        access = from_int(obj.get("access"))
        login_time = from_int(obj.get("loginTime"))
        ref_id = from_str(obj.get("refId"))
        referred_by = from_int(obj.get("referredBy"))
        shard = from_str(obj.get("shard"))
        reg_lang = from_str(obj.get("regLang"))
        reg_platform = int(from_str(obj.get("regPlatform")))
        sid = from_none(obj.get("sid"))
        session = Session.from_dict(obj.get("session"))
        uid = from_int(obj.get("uid"))
        nick = from_str(obj.get("nick"))
        return User(norm_nick, level, gender, kind, clan_id, clan, rank, rank_icon, rank2, rank2_icon, flags, access, login_time, ref_id, referred_by, shard, reg_lang, reg_platform, sid, session, uid, nick)

    def to_dict(self) -> dict:
        result: dict = {}
        result["normNick"] = from_str(self.norm_nick)
        result["level"] = from_int(self.level)
        result["gender"] = from_int(self.gender)
        result["kind"] = from_int(self.kind)
        result["clanId"] = from_int(self.clan_id)
        result["clan"] = from_none(self.clan)
        result["rank"] = from_int(self.rank)
        result["rankIcon"] = from_none(self.rank_icon)
        result["rank2"] = from_int(self.rank2)
        result["rank2Icon"] = from_none(self.rank2_icon)
        result["flags"] = from_int(self.flags)
        result["access"] = from_int(self.access)
        result["loginTime"] = from_int(self.login_time)
        result["refId"] = from_str(self.ref_id)
        result["referredBy"] = from_int(self.referred_by)
        result["shard"] = from_str(self.shard)
        result["regLang"] = from_str(self.reg_lang)
        result["regPlatform"] = from_str(str(self.reg_platform))
        result["sid"] = from_none(self.sid)
        result["session"] = to_class(Session, self.session)
        result["uid"] = from_int(self.uid)
        result["nick"] = from_str(self.nick)
        return result


@dataclass
class LoginModel:
    email: str
    users: List[User]
    social_ids: List[Any]
    selected_uid: int
    status: bool
    set_cookie_cid: str
    set_cookie_fbm: str
    set_cookie_fbsr: str
    set_cookie_sess: str
    set_cookie_account: str
    set_cookie_update: int
    set_cookie_user: str

    @staticmethod
    def from_dict(obj: Any) -> 'LoginModel':
        print(obj)
        assert isinstance(obj, dict)
        email = from_str(obj.get("email"))
        users = from_list(User.from_dict, obj.get("users"))
        social_ids = from_list(lambda x: x, obj.get("socialIds"))
        selected_uid = from_int(obj.get("selectedUid"))
        status = from_bool(obj.get("status"))
        set_cookie_cid = from_str(obj.get("setCookie[cid]", ''))
        #set_cookie_fbm_101651603250615 = from_str(obj.get("setCookie[fbm_101651603250615]"))
        #set_cookie_fbsr_101651603250615 = from_str(obj.get("setCookie[fbsr_101651603250615]"))
        set_cookie_sess = from_str(obj.get("setCookie[sess]", ''))
        set_cookie_account = from_str(obj.get("setCookie[account]"))
        set_cookie_update = from_int(obj.get("setCookie[update]"))
        set_cookie_user = from_str(obj.get("setCookie[user]"))
        return LoginModel(email, users, social_ids, selected_uid, status, set_cookie_cid, '', '', set_cookie_sess, set_cookie_account, set_cookie_update, set_cookie_user)

    def to_dict(self) -> dict:
        result: dict = {}
        result["email"] = from_str(self.email)
        result["users"] = from_list(lambda x: to_class(User, x), self.users)
        result["socialIds"] = from_list(lambda x: x, self.social_ids)
        result["selectedUid"] = from_int(self.selected_uid)
        result["status"] = from_bool(self.status)
        result["setCookie[cid]"] = from_str(self.set_cookie_cid)
        #result["setCookie[fbm_101651603250615]"] = from_str(self.set_cookie_fbm_101651603250615)
        #result["setCookie[fbsr_101651603250615]"] = from_str(self.set_cookie_fbsr_101651603250615)
        result["setCookie[sess]"] = from_str(self.set_cookie_sess)
        result["setCookie[account]"] = from_str(self.set_cookie_account)
        result["setCookie[update]"] = from_int(self.set_cookie_update)
        result["setCookie[user]"] = from_str(self.set_cookie_user)
        return result

    def get_user_name(self, name: str) -> Union[User, None]:
        for i in self.users:
            if (i.norm_nick.lower() == name.lower()):
                return i
