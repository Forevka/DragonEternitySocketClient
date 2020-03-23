import typing
from urllib.parse import parse_qs

def parse_game_config(page_html: str) -> typing.Dict[str, typing.List[str]]:
    flashvars = page_html[page_html.find("flashvars:"):page_html.find("flashvars:") + page_html[page_html.find("flashvars:"):].find(",")]
    flashvars = flashvars.replace("flashvars: '", '')
    flashvars = flashvars.replace("'", "")

    return parse_qs(flashvars)
