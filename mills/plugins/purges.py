"""
≛ <b>Commands Available</b> ≛

──────────────────────
<code>/del</code>: delete the message .
──────────────────────
<code>/purge</code>: delete from replied message .
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""

# from telethon import Button
from telethon.tl.custom import Button
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError

from mills import client
from mills.decorators import bot_cmd
from ._helpers.strings  import get_strings




@bot_cmd(cmd="del", groups_only = True, delete_messages = True)
async def pin(m):
    if not await m.get_reply_message():
        return await m.sod("reply to message", time = 5)
    rm = await m.get_reply_message()
    msgs = [m.id, rm.id]
    await client.delete_messages(m.chat.id, msgs)
   
    


@bot_cmd(cmd="purge", groups_only = True, delete_messages = True)
async def pin(m):
    if not await m.get_reply_message():
        return await m.sod("reply to message", time = 5)
    rm = await m.get_reply_message()
    msg_id = rm.id
    delete_to = m.id
    chat_id = m.chat.id
    
    msgs = []
    for m_id in range(int(delete_to), msg_id - 1, -1):
        msgs.append(m_id)
        if len(msgs) == 100:
            await client.delete_messages(chat_id, msgs)
            msgs = []

    try:
        await client.delete_messages(chat_id, msgs)
    except MessageDeleteForbiddenError:
        await m.sod("Errot while purging")
        return

    return await m.sod("Purge completed", time = 6)

    


