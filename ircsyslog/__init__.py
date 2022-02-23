import asyncio, re

from ircrobots import Bot
from irctokens import build
from typing    import Dict

from .config import Config
from .common import severity_str, format_string, LogFacility, LogSeverity

RE_SYSLOG = re.compile(r"^<(?P<pri>\d+)>(?P<time>\S+ \S+ \S+) (?P<hostname>\S+) (?P<process>\S+): (?P<message>.*)")

class SysLogServer(object):
    def __init__(self,
        bot: Bot,
        config: Config):

        self.bot: Bot = bot
        self.config: Config = config

    def snuffed(self, vars: Dict):
        for pattern in self.config.processbl:
            if pattern.search(vars["process"]):
                print(f"blocked due to prcbl {pattern.pattern}")
                return True

        for pattern in self.config.messagebl:
            if pattern.search(vars["message"]):
                print(f"blocked due to msgbl {pattern.pattern}")
                return True

        return False

    async def _report(self, msg: str):
        if self.bot.servers:
            server = list(self.bot.servers.values())[0]
            await server.send(
                build("PRIVMSG", [self.config.channel, msg])
            )

    async def _handle(self, reader, writer):
        while True:
            data = await reader.readline()
            clean_data = data.decode().replace("\n", "")

            m = RE_SYSLOG.search(clean_data)
            if m:
                vars = m.groupdict().copy()

                if self.snuffed(vars):
                    continue

                facility, severity = divmod(int(vars["pri"]), 8)

                try:
                    vars["facility"] = LogFacility(facility).name
                except ValueError:
                    vars["facility"] = "\x02\x0308UNKNOWN\x03\x02"
                try:
                    vars["severity"] = severity_str(LogSeverity(severity))
                except:
                    vars["severity"] = "\x02\x0308UNKNOWN\x03\x02"

                await self._report(format_string(self.config.reportformat, vars))
            else:
                print(f"no match for {clean_data}")

    async def run(self):
        server = await asyncio.start_server(
            self._handle, "10.48.0.1", 11514)

        addrs = ", ".join(
            f"{sock.getsockname()[0]}:{sock.getsockname()[1]}"
            for sock in server.sockets
        )

        async with server:
            await server.serve_forever()
