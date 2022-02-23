import yaml

from re          import compile as re_compile
from dataclasses import dataclass
from typing      import Dict, Tuple, Optional, Pattern, List

@dataclass
class Config(object):
    server:   Tuple[str, int, bool]
    nickname: str
    username: str
    realname: str
    channel: str

    reportformat: str
    processbl: List[Pattern]
    messagebl: List[Pattern]
    listen_addr: str
    listen_port: int

    password: Optional[str]
    sasl: Optional[Tuple[str, str]]

def load(filepath: str):
    with open(filepath) as file:
        config_yaml = yaml.safe_load(file.read())

    nickname = config_yaml["nickname"]

    server   = config_yaml["server"]
    hostname, port_s = server.split(":", 1)
    tls      = False

    listen_addr, listen_port = config_yaml["listen"].split(":")

    if port_s.startswith("+"):
        tls    = True
        port_s = port_s.lstrip("+")
    port = int(port_s)

    if "sasl" in config_yaml:
        sasl = (config_yaml["sasl"]["username"], config_yaml["sasl"]["password"])
    else:
        sasl = None

    return Config(
        (hostname, port, tls),
        nickname,
        config_yaml.get("username", nickname),
        config_yaml.get("realname", nickname),
        config_yaml["channel"],
        config_yaml["reportformat"],
        [re_compile(pattern) for pattern in config_yaml.get("processbl", [])],
        [re_compile(pattern) for pattern in config_yaml.get("messagebl", [])],
        listen_addr,
        listen_port,
        config_yaml.get("password", None),
        sasl
    )
