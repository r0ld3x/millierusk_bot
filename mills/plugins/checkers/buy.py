"""
≛ <b>Commands Available</b> ≛

──────────────────────────
- <code>/buy<code>: Check Available plans for unlocking paid checker gates.
──────────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import inspect
import io
import json
import os
import time
from fuzzywuzzy.process import extractOne
from telethon import utils
# from telethon import Button
from telethon.tl.custom import Button

from mills import BOT_PIC, client
from mills.decorators import bot_cmd


@bot_cmd(pattern="buy$")
async def _(m):
    text = f"""

┌──────────────────────────┐
    • Premium Plans •

◦ 5$ - Get access to all gates for 28 days.
◦ 10$ - Get access to all gates. for 70 days
◦ 20$ - Get access to all gates. for 200 days

○ Payment methods: Crypto, Bank Transfer, Airtm (No Paypal)

└──────────────────────────┘
"""
    buttons = [
        Button.url('Buy Now', 'https://t.me/r0ld3x'),
        Button.url('Test Keys', 'https://t.me/roldexverse'),
    ]
    await m.reply(text,buttons= buttons, file = BOT_PIC)