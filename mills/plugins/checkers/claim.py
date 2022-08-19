"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/claim</code>: Claim your premium key
➛ Parameters:
    - <b>Key</b>: Key which you got from the admin of this bot.
➻ Example: <code>/claim *key*</code>
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""


import os,sys
import random
from time import gmtime, strftime
import time

from mills import LOG_CHAT
from mills.decorators import bot_cmd
from mills.plugins.checkers.utils.userinfo  import user_info



@bot_cmd(cmd="claim")
async def _(m):
    params = m.pattern_match.group(1).strip()
    if not params or not ( params.startswith('MILLIE-') and params.endswith('-PREMIUM') ):
        await m.sod("Wrong Input Check Example: `/claim *key*`", time = 5)
        return
    is_key = await m.mdb.find_one('keys', {'_id': params})
    if not is_key:
        await m.sod("Provided key not found Example: `/gkey key`", time = 5)
        return
    user = await user_info(m)
    if user['type'] == 'P' and params.startswith('MILLIE-') and params.endswith('-PREMIUM'):
        await m.sod("You are a premium user. please user your current plans then go for this.", time = 5)
        return
    
    exp = is_key['data'] * 3600 if is_key['time_type'] == 'hour' else is_key['data'] * 86400
    filter = {'_id': m.sender_id}
    data = {
        '$addToSet': {
            'keys': params,
            'claimed_date': strftime("%Y-%m-%d", gmtime()),
        },
        '$set': {
            'type': 'P',
            'role': 'Premium User',
            'antispam_time': 30,
            'expire_days': int(time.time()) + exp,
        }
    }
    
    insert = await m.mdb.update_one('users', filter,data)
    if insert:
        await m.sod("You have claimed your key successfully. now your **Premium** plan will expire on {} {}".format(is_key['data'], is_key['time_type']), time = 5) 
        await m.client.send_message(LOG_CHAT,  f"{m.sender_id} Claimed Key: {params}")
    else:
        await m.sod("Error while claiming key", time = 5)