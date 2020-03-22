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