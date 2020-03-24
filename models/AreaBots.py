from utils.parse import *

@dataclass
class Bot:
    area_bot_id: int
    id: int

    @staticmethod
    def from_dict(obj: Any) -> 'Bot':
        assert isinstance(obj, dict)
        area_bot_id = from_int(obj.get("areaBotId"))
        id = from_int(obj.get("id"))
        return Bot(area_bot_id, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["areaBotId"] = from_int(self.area_bot_id)
        result["id"] = from_int(self.id)
        return result


@dataclass
class AreaBots:
    bots: List[Bot]
    evt: str

    @staticmethod
    def from_dict(obj: Any) -> 'AreaBots':
        assert isinstance(obj, dict)
        bots = from_list(Bot.from_dict, obj.get("bots"))
        evt = from_str(obj.get("evt"))
        return AreaBots(bots, evt)

    def to_dict(self) -> dict:
        result: dict = {}
        result["bots"] = from_list(lambda x: to_class(Bot, x), self.bots)
        result["evt"] = from_str(self.evt)
        return result