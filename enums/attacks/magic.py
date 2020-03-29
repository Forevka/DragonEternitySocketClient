from enum import Enum, auto

class Magic(Enum):
    """
        Основная магия
        ТИП_Уровень
    """
    Chaos_1 = 910
    Earth_1 = 134
    Water_1 = 131


    idk_1 = 5951
    idk_2 = 6036
    idk_3 = 7042
    idk_4 = 7046
    idk_5 = 7058
    idk_6 = 7062

    """
        Травилки
        ТИП_Уровень
    """
    Auxilary_Chaos_1 = 1343
    Auxilary_Earth_1 = 1340
    Auxilary_Water_1 = 1339


if __name__ == "__main__":
    print(Magic(90))