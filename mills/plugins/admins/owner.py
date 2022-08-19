"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/leavebot</code>: bot will leave the chat.
──────────────────────
- <code>/stop</code>: Bot will stop working and exit.
──────────────────────
- <code>/del_key</code>: Delete key if exists
➛ Params: <b>key</b>
➻ Example: <code>/del_key *key*</code> 
"""


import os,sys
import random
from time import gmtime, strftime
import time

from mills import LOG_CHAT, client
from mills.decorators import bot_cmd
from ..checkers.utils.userinfo  import user_info




@bot_cmd(cmd="leavebot", owner_only = True)
async def _(m):
    await client.kick_participant(m.chat.id, client.me.id)



@bot_cmd(cmd="stopbot", owner_only = True)
async def _(m):
    await client.disconnect()



