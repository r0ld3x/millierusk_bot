"""
≛ <b>Commands Available</b> ≛
──────────────────────
- <code>/vbv</code> cc cvv mes ano || <reply_to_msg>
➛ Vbv Check b3
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""


import os
import re
import time
import requests
from mills import LOG_CHAT

from mills.decorators import bot_cmd
from mills.func.tools import web_search
from mills.plugins.checkers.utils.gateinfo import get_gate_info
from mills.plugins import rand_user_base
from mills.plugins.checkers.utils.getcards  import get_cards
from mills.plugins._helpers.strings import get_strings
from mills.plugins.checkers.funcs.vbv_defs import vbv_one,vbv_two




@bot_cmd(cmd="vbv", text_only = True)
@get_gate_info("vbv")
@get_cards()
@get_strings("card_chk")
async def _vbv(m, gate_db, user_db, cards, lang):
    start_time = int(time.time())
    cc,mes,ano,cvv, bin_info = cards
    message = await m.reply(lang['fir_msg'].format(
        gate_name = gate_db['gate_name'],
        name = m.full_name(),
        id = m.sender_id,
        taken = int(time.time()) - start_time,
    ))
    r = requests.Session()
    rand_user = rand_user_base.rand_user()
    if proxy:= await m.adb.get_key('use_proxy'):
        r.proxies = {'http': proxy, 'https': proxy}
    bearer = vbv_one(r, rand_user)
    if not bearer:
        return await message.edit("Error while checking your card. trying again....")
    await message.edit(lang['mid_msg'].format(
        gate_name = gate_db['gate_name'],
        name = m.full_name(),
        id = m.sender_id,
        taken = int(time.time()) - start_time,
    ))
    last = vbv_two(r,rand_user,bearer,cc,mes,ano,cvv)
    if not last:
        return await message.edit("Error while checking your card. trying again....")
    r_text, r_logo , r_respo = last
    await message.edit(lang['fin_msg'].format(
        gate_name = gate_db['gate_name'],
        card = f"{cc}|{mes}|{ano}|{cvv}",
        status = r_respo,
        logo = r_logo,
        message =  r_text,
        vendor = bin_info['vendor'],
        type = bin_info['type'],
        bank_name = bin_info['bank_name'],
        country = bin_info['iso'],
        flag = bin_info['flag'],
        name = m.full_name(),
        id = m.sender_id,
        role = user_db['role'],
        taken = int(time.time()) - start_time,
    ), link_preview = False)
    await m.adb.set_key(f'antispam_{str(m.sender_id)}', time.time())
    return