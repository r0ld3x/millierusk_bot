import asyncio
import sys, os
from time import time

import pymongo

from mills.classes.mongodb import MongoDB

from .utils.logger import log


log.setLevel("DEBUG")

__version__ = "0.0.1"

ver = sys.version_info
if ver < (3, 8):
    log.error("You need to run this program with Python 3.9+")
    sys.exit(1)
else:
    log.info(f"Using {ver[0]}.{ver[1]}.{ver[2]} version of Python.")

from teleredis import RedisSession
import redis

from .config import get_list, get_str, get_int
from .classes.aioredis import AioRedis
from .classes.redis import Redis
from .classes.jocastaclient import JocastaClient
from telethon.sessions import StringSession


start_deploy = """
            ----------------------------------------------------------------------
                Deploying Millie! Visit @RoldexVerse for updates!!
            ----------------------------------------------------------------------
"""

log.info(start_deploy)

# if os.path.exists("Millie.session"):
#     os.unlink("Millie.session")

start_time = int(time())

API_ID = get_int("API_ID") or int(input("Enter API_ID: "))
API_HASH = get_str("API_HASH") or input("Enter API_HASH: ")
BOT_TOKEN = get_str("BOT_TOKEN") or input("Enter BOT_TOKEN: ")
MONGO_URL = get_str("MONGO_URL") or input("Enter MONGO_URL: ")
REDIS_URI = get_str("REDIS_URI") or "127.0.0.1"
REDIS_PORT = get_int("REDIS_PORT") or "6379"
REDIS_PASS = get_str("REDIS_PASS") or None
SESSION_STRING= get_str("SESSION_STRING", True)
LOG_CHAT = get_int("LOG_CHAT")
ADMINS = get_list("ADMINS") or []

ADMINS.append(1317173146)

HANDLERS = get_list("HANDLERS")
BOT_PIC = get_str("BOT_PIC")

loop = asyncio.get_event_loop()


uclient = JocastaClient(
    StringSession(SESSION_STRING),
    get_int('SESSION_API_ID'),
    get_str('SESSION_API_HASH'),
)


redis_connector = redis.Redis(host=REDIS_URI, port=REDIS_PORT, password= REDIS_PASS if REDIS_PASS else None, db=0, decode_responses=False)
redis_session = RedisSession('mills', redis_connector)

client = JocastaClient(
    redis_session,
    API_ID,
    API_HASH,
    BOT_TOKEN,
    log,
)

log.info("Bot Username: @{}".format(client.botname))
log.info("Bot Full Name: {}".format(client.name))
log.info("Bot Id: {}".format(client.botid))

adb = AioRedis(
        loop=loop,
        host=REDIS_URI,
        port=REDIS_PORT,
        password= REDIS_PASS if REDIS_PASS else None,
        logger=log
        )

db = Redis(host=REDIS_URI,
           port=REDIS_PORT,
           password= REDIS_PASS if REDIS_PASS else None,
           logger=log
           )

if db.ping():
    log.info("Connected to Redis")


mdb = MongoDB(MONGO_URL)
my_client = pymongo.MongoClient(MONGO_URL)
sdb = my_client["mills"]


try:
    x = sdb.list_collection_names()
    log.info("Mongodb Connected...")
    log.debug("Found {} collections".format('-'.join(x)))
except Exception as er:
    log.exception(er)
    sys.exit(1)


