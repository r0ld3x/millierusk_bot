"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/randuser</code> : Get a random user infomation.
──────────────────────
- <code>/randpic</code> : Get a random user pic.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import inspect
import io
import json
import os
import random
import time
import requests
from telethon import utils
# from telethon import Button
from telethon.tl.custom import Button
from faker import Faker
from faker.providers import internet


from mills.decorators import bot_cmd
from mills.func.tools import web_search
from ._helpers.strings  import get_strings

from mills.classes.rand_user import RandUser


@bot_cmd(cmd="randuser")
async def ipinfo(m):
    fake = Faker()
    name = str(fake.name())
    fake.add_provider(internet)
    address = str(fake.address())
    ip = fake.ipv4_private()
    cc = fake.credit_card_full()
    email = fake.ascii_free_email()
    job = fake.job()
    pc = fake.chrome()
    await m.reply(
        f"<b><u> Fake Information Generated</b></u>\n<b>Name :-</b><code>{name}</code>\n\n<b>Address:-</b><code>{address}</code>\n\n<b>IP ADDRESS:-</b><code>{ip}</code>\n\n<b>credit card:-</b><code>{cc}</code>\n\n<b>Email Id:-</b><code>{email}</code>\n\n<b>Job:-</b><code>{job}</code>\n\n<b>Pc user agent:-</b><code>{pc}</code>",
        parse_mode="HTML",
    )


@bot_cmd(cmd="randpic")
async def randpic(m):
    cont = await web_search('https://thispersondoesnotexist.com/image', r_content = True)
    with io.BytesIO(cont) as pic:
        await m.sod(file = pic)