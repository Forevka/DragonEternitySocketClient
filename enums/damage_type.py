from enum import Enum


class DamageType(Enum):
    NotHaveType = 0
    Default = 1
    Fire = 2
    Light = 4
    Earth = 8
    Water = 16
    Chaos = 32
    Life = 128 #heal
    Destruction = 256
    Time = 512
    Death = 1024
    Imba = 2048 #Неуворачиваемая нерезистящаяся неотражаемая
    Throw = 4096 #бросок наверное на ездовом который
    Curse = 8192