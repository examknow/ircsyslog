import asyncio

from argparse  import ArgumentParser
from ircrobots import Bot, ConnectionParams, SASLUserPass
from .config   import Config, load as config_load
from .         import SysLogServer

async def main(config: Config):
    bot = Bot()

    host, port, tls      = config.server

    params = ConnectionParams(
        config.nickname,
        host,
        port,
        tls,
        username=config.username,
        realname=config.realname,
        password=config.password,
        autojoin=[config.channel]
    )
    if config.sasl is not None:
        sasl_user, sasl_pass = config.sasl
        params.sasl = SASLUserPass(sasl_user, sasl_pass)
    await bot.add_server(host, params)

    syslog = SysLogServer(bot, config)
    await asyncio.gather(
        bot.run(),
        syslog.run()
    )

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("config")
    args   = parser.parse_args()

    config = config_load(args.config)
    asyncio.run(main(config))
