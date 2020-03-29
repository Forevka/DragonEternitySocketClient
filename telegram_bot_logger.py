from config import BOT_TOKEN, CHAT_ID
import requests 

class TelegramBotLogger:
    def __init__(self,):
        self.token = BOT_TOKEN
        self.chat_id = CHAT_ID

        self.base_url = f'https://api.telegram.org/bot{self.token}/'

    def send_message(self, msg: str):
        res = requests.post(self.base_url + 'sendMessage', data = {
            'chat_id': self.chat_id,
            'text': msg,
            'parse_mode': 'html',
        })
        return res


if __name__ == "__main__":
    t = TelegramBotLogger()
    t.send_message('qwewqe')