import os,sys

from mills import client, LOG_CHAT
from mills.utils.logger import log
from mills.config import del_key


async def startup():
    if LOG_CHAT and not str(LOG_CHAT).startswith("-100"):
        try:
            _ = await client.get_entity(LOG_CHAT)
        except BaseException as e:
            log.exception(e)
            del_key("LOG_CHANNEL")
            log.error("LOG_CHANNEL is not valid")
            sys.exit(1)
        