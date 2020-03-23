import time
import sys
import requests
from config import LOGIN, PASSWORD

from auth.models.login import LoginModel

def auth(user_id: int, cookies: dict) -> str:
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Sec-Fetch-Dest': 'empty',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://drako.ru',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://drako.ru/',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,pl;q=0.5,fr;q=0.4,es;q=0.3',
    }

    params = (
        ('action', 'enter'),
        ('output', 'json'),
    )

    data = {
        'uid': str(user_id),
        'loginOnly': '1'
    }

    response = requests.post('http://drako.ru/game/auth.php', headers=headers, params=params, cookies=cookies, data=data)
    print(response.headers)
    print(response.cookies)
    return response.cookies.get('user')

#def enter(user_id: str) -> List[str]:
#    ...

def silent_login(user_name: str) -> str:
    headers = {
        'Host': 'drako.ru',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Sec-Fetch-Dest': 'empty',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://drako.ru',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://drako.ru/',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,pl;q=0.5,fr;q=0.4,es;q=0.3',
    }

    params = (
        ('action', 'login'),
        ('output', 'json'),
    )

    data = f'email={LOGIN}&password={PASSWORD}&remember=1'

    response = requests.post('http://drako.ru/game/auth.php', headers=headers, params=params, data=data)

    logged = LoginModel.from_dict(response.json())
    print(logged)

    user = logged.get_user_name(user_name)

    cookies = {
        'cid': logged.set_cookie_cid,
        'account': logged.set_cookie_account,#'mKiJ1RWny-X4Ai_3Y3RyY4d1d-cJVgP5fL85Vk1DO_4.eyJpZCI6MjY5Njg4ODcsImVtYWlsIjoiemViZXN0Zm9yZXZrYUBnbWFpbC5jb20iLCJzaGFyZHMiOiJydTEiLCJjdGltZSI6MTU4NDk2MDQ0NCwibG9uZyI6MX0',
        'user': logged.set_cookie_user,#'ZAbN0D4HtxDu98oGluP-f1igNABHZM08LX3oV_AVcCQ.eyJ1aWQiOjIxMTI4MTAxLCJndWVzdERhdGEiOiIiLCJjdGltZSI6MTU4NDk2MDU3OCwibG9uZyI6MX0',
        'sess': logged.set_cookie_sess,#'ltaq19vhmmkktf6pa4en150s93',
    }

    # user_session = auth(user.uid, cookies)
    #cookies['user'] = user_session
    #print(cookies)

    response = requests.get('http://drako.ru/game/main.php', headers=headers, cookies=cookies)
    print(response.text)

    html_source = response.text
    t = html_source[html_source.find("key="):html_source.find("key=") + html_source[html_source.find("key="):].find("&")][4:]
    return t



if __name__ == "__main__":
    silent_login()
    #open_browser()