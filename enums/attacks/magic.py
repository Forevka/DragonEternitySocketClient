from enum import Enum, auto

class Magic(Enum):
    """
        Основная магия
        ТИП_Уровень
    """
    Chaos_1 = 910
    Earth_1 = 134
    Water_1 = 131

    """
        Травилки
        ТИП_Уровень
    """
    Auxilary_Chaos_1 = 1343
    Auxilary_Earth_1 = 1340
    Auxilary_Water_1 = 1339


if __name__ == "__main__":
    print(Magic(90))