"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/mchk</code> cards || <reply_to_msg>.
➛ Charge 10$.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""


import json
import os
import re
import time
import requests
import concurrent.futures
from mills.plugins.checkers.funcs.mchk_defs import new_func


from mills.decorators import bot_cmd
from mills.plugins.checkers.utils.gateinfo import get_gate_info
from mills.plugins import rand_user_base
from mills.plugins._helpers.strings import get_strings
from mills.plugins.checkers.utils.tools import checkLuhn



@bot_cmd(cmd="mchk", text_only = True)
@get_gate_info("mchk")
@get_strings("card_chk")
async def _(m, gate_db, user_db, lang):
    start_time = int(time.time())
    kk = await m.reply("Wait gettting valid cards from your input.")
    all_cards = m.text.split('\n')
    if len(all_cards) > 15:
        await kk.edit("Give Me Less Then 15 Cards Gay.")
        pass
    cards = []
    for x in all_cards:
        input = re.findall(r"[0-9]+", x)
        if not input or len(input) < 3:
            continue
        if len(input) == 3:
                cc = input[0]
                if len(input[1]) == 3:
                    mes = input[2][:2]
                    ano = input[2][2:]
                    cvv = input[1]
                else:
                    mes = input[1][:2]
                    ano = input[1][2:]
                    cvv = input[2]
        else:
            cc = input[0]
            if len(input[1]) == 3:
                mes = input[2]
                ano = input[3]
                cvv = input[1]
            else:
                mes = input[1]
                ano = input[2]
                cvv = input[3]
            if  len(mes) == 2 and (mes > '12' or mes < '01'):
                ano1 = mes
                mes = ano
                ano = ano1
        if cc and not checkLuhn(cc): continue
        if (cc, mes, ano, cvv):
            cards.append([cc, mes , ano , cvv])
        else:
            continue
    
    len_cards = len(cards)
    if not len_cards:
        return await kk.edit("not found any cards from your input. thats bad.")
    await kk.edit("Found {} Cards from your input now i am checking them.".format(len_cards))
    text = f"""
<b>Gate</b>: <b>{gate_db['gate_name']}</b>
<b>Total Time</b>: {int(time.time()) - start_time}'s
<b>User</b>: <a href="tg://user?id={m.sender_id}">{m.full_name()}</a>
<b>Total</b>: {len_cards} 
Responses: 

"""
    rand_user = rand_user_base.rand_user()
    r = requests.Session()
    for inp in cards:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(new_func, r, inp[0], inp[3], inp[1], inp[2], rand_user)
            return_value = future.result()
            text += return_value
            await kk.edit(text, link_preview = False)
    text += "<i>All Cards Checked</i>"
    await kk.edit(text)