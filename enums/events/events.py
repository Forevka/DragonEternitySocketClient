from enum import Enum, auto

class EventType(Enum):
    QueueInfo = auto()
    CalendarDiff = auto()
    ChatMessage = auto()
    Enter = auto()
    Ping = auto()
    PunishmentInfo = auto()
    ChatUsers = auto()
    UserInfo = auto()
    EventsInfo = auto()
    ChatUsersDiff = auto()
    EventUpdated = auto()
    NewLogin = auto()
    AreaBots = auto()
    AttackBot = auto()
    FightState = auto()
    PersListChange = auto() #когда в бой ктото заходит
    PersListState = auto()  
    Mana = auto()           #когда изменяется мана
    NewRound = auto()       #
    OppNew = auto()         #когда напротив тебя становится новый оппонент
    Cast = auto()
    ObsNew = auto()         #
    PairChange = auto()
    AttackNow = auto()      #атакуем
    AttackWait = auto()     #ждём чтоб наш оппонент сделал ход
    EffDrop = auto()
    FightFinish = auto()
    ItemInfo = auto()
    SocEvent = auto()
    FightResults = auto()
    Damage = auto()
    ItemDrop = auto()
    FriendList = auto()
    FriendInfo = auto()
    AddAttr = auto()
    PartyMemberInfo = auto()


    Lots = auto() ##my custom event