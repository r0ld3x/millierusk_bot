"""
≛ <b>Commands Available</b> ≛

- <code>/pin</code>: Pin Replied Message.
──────────────────────
- <code>/promote</code>: promote replied user.
──────────────────────
- <code>/demote</code>: Demote replied user.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import inspect
import io
import json
import os
import time
import requests
from telethon import utils
# from telethon import Button
from telethon.tl.custom import Button


from mills import client
from mills.decorators import bot_cmd
from ._helpers.strings  import get_strings




@bot_cmd(cmd="pin", groups_only = True,  gadmins_only = True,  pin_messages = True)
async def pin(m):
    if not await m.get_reply_message():
        return await m.sod("Reply to message", time = 5)
    x = await client.get_permissions(m.chat.id, m.sender_id)
    if not (x.is_admin or x.is_creator):
        return await m.sod("You are not admin here.", time = 8)
    if not  x.pin_messages:
        return await m.sod("You dont have pin messages rights.", time = 8)
    chk = await client.pin_message(m.chat,await m.get_reply_message(), notify = True)
    if chk:
        return await m.sod("Message Pinned.", time = 5)
    else:
        return await m.sod("Error while pinning message.", time= 5)




@bot_cmd(cmd="promote", groups_only = True, gadmins_only = True, is_admin = True)
async def promote(m):
    title = m.pattern_match.group(1).strip() or "Admin"
    reply = await m.get_reply_message()
    if not await m.get_reply_message():
        return await m.sod("reply to message", time = 5)
    
    if reply.sender_id == client.me.id:
        return await m.sod("I can't promote myself. btw i am already a admin here.")
    x = await client.get_permissions(m.chat.id, m.sender_id)
    if not (x.is_admin or x.is_creator):
        return await m.sod("You are not admin here.", time = 8)
    if not x.add_admins:
        return await m.sod("You dont have add admins right.", time = 8)
    
    chk = await client.edit_admin(
        m.chat.id,
        reply.sender_id,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        title=title,
    )
    if chk:
        return await m.sod("Promoted.", time = 5)
    else:
        return await m.sod("Error while promoting.", time = 5)
        



@bot_cmd(cmd="demote", groups_only = True, gadmins_only = True, is_admin = True)
async def demote(m):
    reply = await m.get_reply_message()
    if not await m.get_reply_message():
        return await m.sod("reply to message", time = 5)
    
    if reply.sender_id == client.me.id:
        return await m.sod("I can't demote myself. btw i am already a admin here.")
    x = await client.get_permissions(m.chat.id, m.sender_id)
    if not (x.is_admin or x.is_creator):
        return await m.sod("You are not admin here.", time = 8)
    if not x.add_admins:
        return await m.sod("You dont have add admins right.", time = 8)
    rperms = await client.get_permissions(m.chat.id, reply.sender_id)
    if not rperms.is_admin:
        return await m.sod("User not admin", time = 5)
    
    chk = await client.edit_admin(
        m.chat.id,
        reply.sender_id,
        invite_users=False,
        change_info=False,
        ban_users=False,
        delete_messages=False,
        pin_messages=False,
    )
    if chk:
        return await m.sod("Demoted.", time = 5)
    else:
        return await m.sod("Error while Demoting.")
        

