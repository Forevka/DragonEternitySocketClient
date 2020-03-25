import time

class RPCGenerator:
    data: dict

    def __init__(self,):
        self.data = {}
    
    def __iter__(self):
        return self

    def __next__(self):
        while (self.data.get('seq', None) is None):
            time.sleep(0.3)
        return self.data