from AMFBuffer import AMFBuffer 

def command(cmd: str,) -> AMFBuffer:
    buf = AMFBuffer()
    buf['cmd'] = cmd
    return buf