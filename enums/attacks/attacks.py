from enum import Enum, auto

class Attack(Enum):
    """
        Я думаю что это список анимаций
        которыми может ударить герой при физ
        атаке
    """
    Defence = 1
    Simple = 2
    Mana = 3

    Hit_Top = 111
    Hit_Front = 72
    Hit_Bottom = 112
    Reviver = 31687

