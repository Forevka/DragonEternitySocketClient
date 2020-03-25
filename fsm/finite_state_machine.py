import typing
from enum import Enum

class StateType(Enum):
    State = 1
    InternalState = 2

class State:
    name: str

    def __init__(self,):
        self.name = "" 

    def __str__(self,) -> str:
        return self.name

class FSMachine:
    name: str
    state_list: typing.Dict[StateType, State]

    current_state: State

    def __init__(self,):
        self.fields = [a for a in dir(self) if not a.startswith('__') and a[0] == a[0].capitalize()]
        for i in self.fields:
            if (isinstance(self.__class__.__dict__[i], State)):
                self.__class__.__dict__[i].name = self.__class__.__name__ + i
                continue
            if (issubclass(self.__class__.__dict__[i], FSMachine)):
                self.__dict__[i] = self.__class__.__dict__[i]()
                self.__dict__[i].name = self.__dict__[i].__class__.__name__
                continue


    def state(self, new_state: State):
        self.current_state = new_state
    
    def current(self,) -> State:
        return self.current_state
    
    def __str__(self,) -> str:
        return self.name

class UserState(FSMachine):
    Test = State()
    class StartState(FSMachine):
        Welcome = State()
    
    class FightState(FSMachine):
        Included = State()

if __name__ == "__main__":

    u = UserState()
    u.state(UserState.StartState.Welcome)
    print(u.current_state)