class UserConfig:
    user_id: str
    user_ccid: str
    user_key: str
    user_lang: str
    env: int

    host: str
    port: int

    @staticmethod
    def load(data: dict) -> 'UserConfig':
        cfg = UserConfig()
        cfg.host = data.get('host')[0]
        cfg.port = int(data.get('port')[0])

        cfg.user_id = data.get('cid')[0]
        cfg.user_ccid = data.get('ccid')[0]
        cfg.user_key = data.get('key')[0]
        cfg.user_lang = data.get('lang')[0]
        cfg.env = int(data.get('env')[0])
        return cfg