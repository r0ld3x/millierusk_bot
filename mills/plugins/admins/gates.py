"""
≛ <b>Commands Available</b> ≛
──────────────────────
- <code>/add_auth</code>: Add new auth gate if not exists.
➻ Example: <code>/add_auth chk Stripe </code>
──────────────────────
- <code>/add_charge</code>: Add new charge gate if not exists.
➻ Example: <code>/add_charge chk Stripe 5</code>
──────────────────────
- <code>/add_other</code>: Add new other gate if not exists.
➻ Example: <code>/add_other chk Stripe</code>
──────────────────────
<code>/del_gate</code>: Delete the gate if exists.
➛ param: <b>Command name</b>
➻ Example: <code>/del_gate chk<code>
──────────────────────
<code>/cha_gate</code>: Change the gate type to paid or free if gate is paid else free to paid.
➛ param: <b>Command name</b>
➻ Example: <code>/cha_gate chk<code>
──────────────────────
<code>/open_gate</code>: Open gate if closed.
➛ param: <b>Command name</b>
➻ Example: <code>/cha_gate chk<code>
──────────────────────
<code>/list_gate<code>: List of all gates added in bot
➻ Example: <code>/list_gate<code>
──────────────────────
©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""


import os,sys
import re
from time import gmtime, strftime

from mills import LOG_CHAT
from mills.decorators import bot_cmd
from mills.plugins.checkers.utils.gateinfo import get_gate_info
from mills.plugins._helpers.strings  import get_strings



@bot_cmd(cmd="add_auth", admins_only = True)
async def _(m):
    params = m.pattern_match.group(1).strip().split(maxsplit=1)
    if len(params) < 2:
        await m.sod("Wrong Input Check Example: <code>/add_auth cmd_name gate_name</code>", time = 5)
        return
    is_gate = await m.mdb.find_one('gate',  params[0].lower())
    if is_gate:
        await m.sod("Gate Already Exists", time = 5)
        return
    gate_dict = {
        '_id': params[0].lower(),
        'status': True,
        'status_logo': '✅',
        'gate_type': 'auth',
        'cmd_name': params[0],
        'gate_name': params[1].title(),
        'made_by_id': m.sender_id,
        'made_by_name': m.full_name(),
        'is_paid': True,
        'date': strftime("%Y-%m-%d", gmtime())
    }
    insert = await m.mdb.insert_one('gate',  gate_dict)
    if insert:
        await m.client.send_message(LOG_CHAT,  f"Gate Added: <code>{params[0]}</code> with name <code>{params[1]}</code> by <a href='tg://user?id={m.sender_id}'>{m.full_name()}</a>")
        await m.sod("Gate Added Successfully", time = 5)
    else:
        await m.sod("Error While Adding Gate", time = 5)




@bot_cmd(cmd="add_charge", admins_only = True)
async def _(m):
    params = m.pattern_match.group(1).strip().split(maxsplit=1)
    if len(params) < 2:
        await m.sod("Wrong Input Check Example: <code>/add_charge cmd_name gate_name charge_amount</code>", time = 5)
        return
    is_gate = await m.mdb.find_one('gate',  params[0].lower())
    if is_gate:
        await m.sod("Gate Already Exists", time = 5)
        return
    dig = re.findall('\d+', params[1])
    amount_name = dig[-1] if dig else None
    if not amount_name:
        return await m.sod("Wrong Input Check Example: <code>/add_charge cmd_name gate_name charge_amount</code>", time = 5)
    gate_name = params[1].replace(amount_name, '').strip().title()
    gate_dict = {
    '_id': params[0].lower(),
    'status': True,
    'status_logo': '✅',
    'gate_type': 'charge',
    'charge_amount': amount_name,
    'cmd_name': params[0],
    'gate_name': gate_name,
    'made_by_id': m.sender_id,
    'made_by_name': m.full_name(),
    'is_paid': True,
    'date': strftime("%Y-%m-%d", gmtime())
    }
    insert = await m.mdb.insert_one('gate',  gate_dict)
    if insert:
        await m.client.send_message(LOG_CHAT,  f"Gate Added: <code>{params[0]}</code> with name <code>{params[1]}</code> by <a href='tg://user?id={m.sender_id}'>{m.full_name()}</a>")
        await m.sod("Gate Added Successfully", time = 5)
    else:
        await m.sod("Error While Adding Gate", time = 5)




@bot_cmd(cmd="add_other", admins_only = True)
async def _(m):
    params = m.pattern_match.group(1).strip().split(maxsplit=1)
    if len(params) < 2:
        await m.sod("Wrong Input Check Example: <code>/add_other cmd_name gate_name</code>", time = 5)
        return
    is_gate = await m.mdb.find_one('gate',  params[0].lower())
    if is_gate:
        await m.sod("Gate Already Exists", time = 5)
        return
    gate_dict = {
        '_id': params[0].lower(),
        'status': True,
        'status_logo': '✅',
        'gate_type': 'other',
        'cmd_name': params[0],
        'gate_name': params[1].title(),
        'made_by_id': m.sender_id,
        'made_by_name': m.full_name(),
        'is_paid': True,
        'date': strftime("%Y-%m-%d", gmtime())
    }
    insert = await m.mdb.insert_one('gate',  gate_dict)
    if insert:
        await m.client.send_message(LOG_CHAT,  f"Gate Added: <code>{params[0]}</code> with name <code>{params[1]}</code> by <a href='tg://user?id={m.sender_id}'>{m.full_name()}</a>")
        await m.sod("Gate Added Successfully", time = 5)
    else:
        await m.sod("Error While Adding Gate", time = 5)




@bot_cmd(cmd="add_mass", admins_only = True)
async def _(m):
    params = m.pattern_match.group(1).strip().split(maxsplit=1)
    if len(params) < 2:
        await m.sod("Wrong Input Check Example: <code>/add_mass cmd_name gate_name</code>", time = 5)
        return
    is_gate = await m.mdb.find_one('gate',  params[0].lower())
    if is_gate:
        await m.sod("Gate Already Exists", time = 5)
        return
    gate_dict = {
        '_id': params[0].lower(),
        'status': True,
        'status_logo': '✅',
        'gate_type': 'mass',
        'cmd_name': params[0],
        'gate_name': params[1].title(),
        'made_by_id': m.sender_id,
        'made_by_name': m.full_name(),
        'is_paid': True,
        'date': strftime("%Y-%m-%d", gmtime())
    }
    insert = await m.mdb.insert_one('gate',  gate_dict)
    if insert:
        await m.client.send_message(LOG_CHAT,  f"Gate Added: <code>{params[0]}</code> with name <code>{params[1]}</code> by <a href='tg://user?id={m.sender_id}'>{m.full_name()}</a>")
        await m.sod("Gate Added Successfully", time = 5)
    else:
        await m.sod("Error While Adding Gate", time = 5)





@bot_cmd(cmd="del_gate", admins_only = True)
async def _(m):
    params = m.pattern_match.group(1).strip().split()
    if len(params) < 1 or not params[0].isalpha():
        await m.sod("Wrong Input Check Example: <code>/del_gate cmd_name</code>", time = 5)
        return
    is_gate = await m.mdb.find_one('gate',  params[0].lower())
    if not is_gate:
        await m.sod("Gate Doesn't Exists", time = 5)
        return
    insert = await m.mdb.delete('gate', {'_id': params[0].lower()})
    if insert:
        await m.client.send_message(LOG_CHAT,  f"Gate Removed: <code>{params[0]}</code> by <a href='tg://user?id={m.sender_id}'>{m.full_name()}</a>")
        await m.sod("Gate Removed Successfully", time = 5)
    else:
        await m.sod("Error While Removing Gate", time = 5)




@bot_cmd(cmd="cha_gate", admins_only = True)
async def _(m):
    params = m.pattern_match.group(1).strip().split()
    if len(params) < 1 or not params[0].isalpha() :
        await m.sod("Wrong Input Check Example: <code>/cha_gate cmd_name</code>", time = 5)
        return
    is_gate = await m.mdb.find_one('gate',  params[0].lower())
    if not is_gate:
        await m.sod("Gate Doesn't Exists", time = 5)
        return
    update = await m.mdb.update_one('gate', {'_id': params[0].lower()}, {'$set': {'is_paid': True if not is_gate['is_paid'] else False}})
    if update:
        await m.client.send_message(LOG_CHAT,  f"Gate Updated: <code>{params[0]}</code> with <code>{True if not is_gate['is_paid'] else False}</code>  by <a href='tg://user?id={m.sender_id}'>{m.full_name()}</a>")
        await m.sod("Gate Updated Successfully", time = 5)
    else:
        await m.sod("Error While Removing Gate", time = 5)




@bot_cmd(cmd="open_gate", admins_only = True)
async def _(m):
    params = m.pattern_match.group(1).strip().split()
    if len(params) < 1 or not params[0].isalpha() :
        await m.sod("Wrong Input Check Example: <code>/open_gate cmd_name</code>", time = 5)
        return
    is_gate = await m.mdb.find_one('gate',  params[0].lower())
    if not is_gate:
        await m.sod("Gate Doesn't Exists", time = 5)
        return
    update = await m.mdb.update_one('gate', {'_id': params[0].lower()}, {
        '$set': {
            'status': True if not is_gate['status'] else False},
            '$set': {'status_logo': '✅' if is_gate['status'] else '❌'}
            })            
    if update:
        await m.client.send_message(LOG_CHAT,  f"Gate Updated: <code>{params[0]}</code> with <code>{True if not is_gate['status'] else False}</code> by <a href='tg://user?id={m.sender_id}'>{m.full_name()}</a> ")
        await m.sod("Gate Updated Successfully", time = 5)
    else:
        await m.sod("Error While Removing Gate", time = 5)



@bot_cmd(cmd="list_gate", admins_only = True)
async def _(m):
    count = await m.mdb.get_count('gate')
    await m.sod("I got a count of {} gates".format(count))
