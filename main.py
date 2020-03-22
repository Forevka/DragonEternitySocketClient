from dispatcher import Dispatcher
from client import Client
from AMFFactory import command
from config import HOST, PORT

client = Client(HOST, PORT)
dp = Dispatcher()

client.set_dispatcher(dp)

@client.onstart()
def enter(client: Client, dp: Dispatcher,):
    a = command('enter')
    a['env'] = 1
    a['key'] = '9f719be99b37483962d736b7cf7683a3'
    a['ccid'] = '5D4BCF747B3C'
    a['lang'] = 'ru'
    a['cid'] = '21128101'
    a['seq'] = 1

    client.send(a)

@client.task(5)
def ping(client: Client, dp: Dispatcher,):
    a = command('ping')
    client.send(a)

if __name__ == "__main__":
    client.start()

    #client.add_task(ping, 5)

    #client.send(a.buffer)