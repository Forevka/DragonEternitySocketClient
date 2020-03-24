import typing
from urllib.parse import parse_qs
from models.UserConfig import UserConfig

def parse_game_config(page_html: str) -> UserConfig:
    flashvars = page_html[page_html.find("flashvars:"):page_html.find("flashvars:") + page_html[page_html.find("flashvars:"):].find(",")]
    flashvars = flashvars.replace("flashvars: '", '')
    flashvars = flashvars.replace("'", "")

    return UserConfig.load(parse_qs(flashvars))


def interact():
    import code
    code.InteractiveConsole(locals=globals() + locals()).interact()
