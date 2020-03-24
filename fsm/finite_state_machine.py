import typing
from enum import Enum

class StateType(Enum):
    State = 1
    InternalState = 2

class State:
    name: str

    def __init__(self,):
        ...

class FSMachine:
    state_list: typing.Dict[StateType, State]

    def __init__(self,):
        ...
        '''self.fields = [a for a in dir(self) if not a.startswith('__')]
        for i in self.fields:
            print(self.__class__.__dict__[i])
            if (type(self.__class__.__dict__[i]) == 'class') 
            if (issubclass(FSMachine, self.__class__.__dict__[i])):
                print('subclass', i)
            else:
                ...'''

class UserState(FSMachine):
    class StartState(FSMachine):
        Welcome = State()
    
    class FightState(FSMachine):
        Included = State()

if __name__ == "__main__":

    u = UserState()