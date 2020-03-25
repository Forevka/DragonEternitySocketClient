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
    OppNew = auto()         #
    Cast = auto()
    ObsNew = auto()         #
    PairChange = auto()
    AttackNow = auto()
    AttackWait = auto()     #
    EffDrop = auto()
    FightFinish = auto()
    ItemInfo = auto()
    SocEvent = auto()
    FightResults = auto()
    Damage = auto()
    ItemDrop = auto()