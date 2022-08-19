"""
≛ <b>Commands Available</b> ≛

──────────────────────
<code>/gen</code> bin || <reply_to_msg> - Generate cards sempai.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""


import os
import re
import time
import requests

from telethon import Button

from .utils.tools import cc_gen
from mills.decorators import bot_cmd
from mills.plugins.checkers.utils.userinfo import get_user_info
from mills.plugins.checkers.utils.bininfo import get_bin_info, get_bin_info_all
from mills.plugins.checkers.utils.tools import checkLuhn



@bot_cmd(cmd="gen", text_only = True)
async def _(m):
    cards = ''
    text = m.pattern_match.group(1)
    if len(text) < 6:
        await m.sod("Invalid bin.", time= 5)
        return
    input = re.findall(r"[0-9]+", text)
    if len(input) == 0:
        await m.sod("Your Bin Is Empty", time = 5)
    if len(input) == 1:
        cc = input[0]
        mes = 'x'
        ano = 'x'
        cvv = 'x'
    elif len(input[0]) < 6 or len(input[0]) > 16:
        await m.sod("Your Bin Is Incorrect", time = 5)
    if len(input) == 2:
        cc = input[0]
        mes = input[1]
        ano = 'x'
        cvv = 'x'
    if len(input) == 3:
        cc = input[0]
        mes = input[1]
        ano = input[2]
        cvv = 'x'
    if len(input) == 4:
        cc = input[0]
        mes = input[1]
        ano = input[2]
        cvv = input[3]
    else:
        bin_info = get_bin_info(str(cc[:6]))
        ccs = cc_gen(cc,mes,ano,cvv)
        cards = '\n'.join(ccs)
        if not bin_info:
            return await m.sod("Bin not found.", time= 5)
    mess = f"""
<b>Card Generator</b>:
<b>Bin</b>: <code>{cc}</code>
<b>Bank</b>: <b>{bin_info['bank_name']}</b> - <b>{bin_info['iso']}</b>
<b>Info</b>: <b>{bin_info['type']}</b> - <b>{bin_info['level']}</b>
<b>User</b>:  <a href="tg://user?id={m.sender_id}">{m.full_name()}</a> 
<b>Cards</b>: 
{cards}
"""
    buttons = [
        Button.inline("Gen Again", f'gen_{cc}_{mes}_{ano}_{cvv}'),
    ]
    await m.sod(mess, buttons = buttons)