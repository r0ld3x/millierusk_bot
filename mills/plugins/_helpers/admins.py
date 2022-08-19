
import asyncio
import time
import uuid

from telethon import Button
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl import functions, types






async def admin_check(event, require=None):
    if ( isinstance(event.sender, (types.Chat, types.Channel)) and event.sender_id == event.chat_id):
        await event.reply("I Don't Support Private Chats Or channels now.")
        return False
    if event.is_private:
        await event.reply("I Don't Support Private Chats Or channels now.")
        return False
    if isinstance(event.sender, types.Channel):
        await event.reply("I Don't Support Channels now.")
        return False
    user = event.sender
    try:
        perms = await event.client.get_permissions(event.chat_id, user.id)
    except UserNotParticipantError:
        await event.reply("You need to join this chat First!")
        return False
    if not perms.is_admin:
        await event.reply("Only Admins can use this command!")
        return
    if require and not getattr(perms, require, False):
        await event.eor(f"You are missing the right of `{require}`", time=8)
        return False
    return True
