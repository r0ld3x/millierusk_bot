"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/kickme</code>: Kick your Self.
──────────────────────
- <code>/decide</code>: Decide Between Yes, No, May, Idk.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import calendar
from datetime import datetime
import inspect
import io
import json
import os
import random
import time
from telethon import utils
# from telethon import Button
from telethon.tl.custom import Button
from googletrans import LANGCODES, LANGUAGES, Translator


from mills import ADMINS, client
from mills.decorators import bot_cmd
from mills import start_time
from mills.plugins.checkers.utils.userinfo import get_user_info
from ._helpers.tools import make_cmds
from mills.func.tools import time_formatter, json_parser
from ._helpers.strings  import get_strings



@bot_cmd(cmd="kickme")
async def kickme(m):
    if m.sender_id in ADMINS:
        return await m.sod("I am not gonna kick you my Admin.", time = 5)
    try:
        client.kick_participant(m.chat_id, m.sender_id)
    except Exception as er:
        return await m.sod(str(er), time = 5)
    return await m.sod("Ok! bye bye.", time = 5)


@bot_cmd(cmd="decide")
async def decide(m):
    arr = ['Yes', 'No', 'May', 'Idk']
    rand = random.choice(arr)
    await m.sod(rand, time = 10)

