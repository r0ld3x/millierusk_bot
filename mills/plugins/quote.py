"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/quote</code> : Get a random quote.
──────────────────────
- <code>/quotepic</code> : Get a random quote in picture.
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

from ._helpers.tools import Carbon1
from . import QUOTES


from mills.decorators import bot_cmd
from ._helpers.strings  import get_strings



@bot_cmd(cmd="quote")
async def quote(m):
    random_choice = random.choice(QUOTES)
    await m.sod(f"{random_choice['text']} - {random_choice['author']}")



@bot_cmd(cmd="quotepic")
async def quotepic(m):
    random_choice = random.choice(QUOTES)
    text = f"`{random_choice['text']}`"
    res = await Carbon1(text)
    if os.path.exists(res):
        await m.sod(file = res, supports_streaming =True)
        os.remove(res)
    else:
        await m.sod("Error")
    return

