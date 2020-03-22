from DataMixin import DataMixin
from miniamf import decode, encode

class AMFBuffer(DataMixin):

    def __init__(self,):
        self.buffer = bytes()
        
    def encode(self,):
        self.buffer += encode(self.data)._buf.getbuffer().tobytes()
        self._write_length()

    def decode(self, data):
        decoded = decode(data)
        d = next(decoded)

        while(d is not None):
            print('!!!!!!!!!!!')
            print(d)
            try:
                d = next(decoded)
            except StopIteration as stop_ex:
                print(stop_ex)
                d = None
            #except Exception as e:
            #    print(e)



    def _write_length(self,):
        length_buffer = int.to_bytes(len(self.buffer), length = 4, byteorder='big')
        self.buffer = length_buffer + self.buffer
