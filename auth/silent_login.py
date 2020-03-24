import time
import sys
import requests
import typing
from config import http_headers as headers
from utils.utils import parse_game_config
from models.UserConfig import UserConfig

from auth.models.login import LoginModel

def auth(user_id: int, cookies: dict) -> str:
    params = (
        ('action', 'enter'),
        ('output', 'json'),
    )

    data = {
        'uid': str(user_id),
        'loginOnly': '1'
    }

    response = requests.post('http://drako.ru/game/auth.php', headers=headers, params=params, cookies=cookies, data=data)

    return response.cookies.get('user')


def silent_login(login: str, password: str, user_name: str) -> UserConfig:
    params = (
        ('action', 'login'),
        ('output', 'json'),
    )

    data = f'email={login}&password={password}&remember=1'

    response = requests.post('http://drako.ru/game/auth.php', headers=headers, params=params, data=data)

    logged = LoginModel.from_dict(response.json())

    cookies = {
        'cid': logged.set_cookie_cid,
        'account': logged.set_cookie_account,#'mKiJ1RWny-X4Ai_3Y3RyY4d1d-cJVgP5fL85Vk1DO_4.eyJpZCI6MjY5Njg4ODcsImVtYWlsIjoiemViZXN0Zm9yZXZrYUBnbWFpbC5jb20iLCJzaGFyZHMiOiJydTEiLCJjdGltZSI6MTU4NDk2MDQ0NCwibG9uZyI6MX0',
        'user': logged.set_cookie_user,#'ZAbN0D4HtxDu98oGluP-f1igNABHZM08LX3oV_AVcCQ.eyJ1aWQiOjIxMTI4MTAxLCJndWVzdERhdGEiOiIiLCJjdGltZSI6MTU4NDk2MDU3OCwibG9uZyI6MX0',
        'sess': logged.set_cookie_sess,#'ltaq19vhmmkktf6pa4en150s93',
    }

    response = requests.get('http://drako.ru/game/main.php', headers=headers, cookies=cookies)

    return parse_game_config(response.text)
