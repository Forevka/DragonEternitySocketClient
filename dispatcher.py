from AMFBuffer import AMFBuffer


class Dispatcher:

    def __init__(self,):
        self.handlers = []
    
    def dispatch(self, data, client: 'Client'):
        #length = data[:4]
        #print(length)
        #length = int.from_bytes(bytes=length, byteorder='big')
        #print(length)
        a = AMFBuffer()
        a.decode(data[4:])

