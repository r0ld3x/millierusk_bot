from io import BytesIO
import os
import re
import sys
import inspect

from pathlib import Path
from asyncio import sleep
from time import gmtime, strftime
from traceback import format_exc

from telethon.tl.types import InputWebDocument
from telethon import Button, __version__ as tv
from telethon.events import NewMessage
from telethon import events
from telethon.utils import get_display_name
from telethon.tl.types import Message
from telethon.errors.common import *
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError
from telethon.events import CallbackQuery, InlineQuery, NewMessage


from mills import ADMINS, BOT_PIC, HANDLERS, LOG_CHAT, client, __version__
from mills.func.tools import cmd_regex_replace
from mills.utils.locals import send
from mills.utils.logger import log
from mills.plugins import LIST




IN_BTTS = [
    [
        Button.url(
            "Owner",
            url="https://t.me/r0ld3x",
        ),
        Button.url("Support", url="https://t.me/RoldexVerse"),
    ]
]



def compile_pattern(data, hndlr):
    if data.startswith("^"):
        data = data[1:]
    if data.startswith("."):
        data = data[1:]
    if hndlr in [" ", "NO_HNDLR"]:
        # No Hndlr Feature
        return re.compile("^" + data)
    x = re.compile(hndlr + data)
    return x



def bot_cmd(pattern=None, *args, **kwargs):
    cmd_name = kwargs.get("cmd", False) or kwargs.get("cmds", False)
    groups_only = kwargs.get("groups_only", False)
    gadmins_only = kwargs.get("gadmins_only", False)
    perm = kwargs.get("perm", False)
    admins_only = kwargs.get("admins_only", False)
    private_only = kwargs.get("private_only", False)
    text_only = kwargs.get("text_only", False)
    funcc = kwargs.get("func", lambda e: not e.via_bot_id)
    re_pattern = r"^[{}]".format(''.join(HANDLERS)) or "/"
    if not pattern and not cmd_name:
        log.critical("no pattern or cmds are found.")
        sys.exit(1)
    if cmd_name and not pattern:
        cmd = r"{}( (.*)|@{}|$)".format(cmd_name , client.me.username)
    else:
        if pattern.endswith("$"):
            cmd = pattern[:-1] + r"(|@{}|$)".format(client.me.username)
        else:
            cmd = cmd_name
    def inner_dec(dec):
        async def wrap(m: Message):
            if not m.sender_id:
                return await m.sod("Use your real account")
            chat = m.chat
            if groups_only and m.is_private:
                return await send(m, "Use only in Groups or Channel.")
            if admins_only and m.sender_id not in ADMINS:
                return await send(m, "Only For Admins.")
            if gadmins_only:
                perms = await client.get_permissions(m.chat, client.me.id)
                if hasattr(m.chat,'admins_rights') and not m.chat.admins_rights or  not (perms.is_admin or perms.is_creator):
                    return await m.sod("I am not admin here. first promote me.",time = 8)
                if  kwargs.get("is_admin", False) and not perms.is_admin:
                    return await m.sod("You dont have add admins rights.",time = 8)
                if  kwargs.get("ban_users", False) and not perms.ban_users:
                    return await m.sod("You dont have ban users rights.",time = 8)
                if  kwargs.get("pin_messages", False) and not perms.pin_messages:
                    return await m.sod("You dont have pin messages rights.",time = 8)
                if  kwargs.get("invite_users", False) and not perms.invite_users:
                    return await m.sod("You dont have invite users rights.",time = 8)
                if  kwargs.get("delete_messages", False) and not perms.delete_messages:
                    return await m.sod("You dont have Delete message rights.",time = 8)
                if  kwargs.get("change_info", False) and not perms.change_info:
                    return await m.sod("You dont have change info rights.",time = 8)
            if private_only and not m.is_private:
                return await send(m, "Use only in private.")
            if text_only and not m.text:
                return await send(m, "Only Text Allowed.")
            try:
                await dec(m)
            except FloodWaitError as e:
                await client.send_message(LOG_CHAT, "Please wait for {} seconds.".format(e.x))
                await client.disconnect()
                await sleep(e.seconds + 15)
                await client.connect()
                await client.send_message(LOG_CHAT, "Reconnected after {} seconds.".format(e.seconds))
                return
            except AlreadyInConversationError as e:
                await send(m, "AlreadyInConversationError: {}".format(e))
                return
            except AuthKeyDuplicatedError as e:
                await client.send_message(LOG_CHAT, "Session File Is Dublicated. Make New Session.")
                return
            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except Exception as e:
                date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                name = get_display_name(chat)
                text = f"""
{client.name} Error in {name}[{m.chat.id}]
Python3 Version: {sys.version_info.major} {sys.version_info.minor}
{client.name} Version: {__version__}
Telethon Version: {tv}
------- Logs -------
Date: {date}
Chat: {name}
Error Message: {e}
Sender Id: {m.sender_id}
Event Trigger: <code>{m.text}</code>
------- Traceback -------

<code>{format_exc()}</code>
""" 
                if len(text) > 4096:
                    with BytesIO(text.encode()) as buffer:
                        buffer.name = 'mille_error.txt'
                        await client.send_message(LOG_CHAT, file=buffer)
                else:
                    await client.send_message(LOG_CHAT, text)
                return
        patt = compile_pattern(cmd, re_pattern)
        client.add_event_handler(wrap,
                        NewMessage(
                            incoming=True,
                            pattern=patt,
                            func=funcc,
                        ))
        file = Path(inspect.stack()[1].filename)   
        if pattern or cmd_name:
            cmd1 = re.sub(r"[^a-zA-Z0-9]","",cmd_name or pattern)
            if not admins_only:
                if LIST.get(file.stem):
                    LIST[file.stem].append(cmd1)
                else:
                    LIST.update({file.stem: [cmd1]})
        return wrap
    return inner_dec



def in_pattern(pattern=None, owner=False, **kwargs):
    """Assistant's inline decorator."""

    def don(func):
        async def wrapper(event):
            if owner and  event.sender_id not in ADMINS:
                MSG = f"""
Hello! I am [{client.name}](tg://user?id={client.botid}).
A Multi functional bot for telegram written in python3.
<b>Owner</b>: <a href="https://t.me/r0ld3x">Roldex</a>
<b>Support</b>: <a href="https://t.me/roldexverse">RoldexVerse</a>
<b>Github</b>: <a href="https://github.com/r0ld3x">r0ld3x</a>
(c) RoldexVerse
"""
                res = [
                    await event.builder.article(
                        title= f"{client.name} - @{client.botname}",
                        url="https://t.me/RoldexVerse",
                        description="(c) RoldexVerse",
                        text=MSG,
                        thumb=InputWebDocument(
                            BOT_PIC,
                            0,
                            "image/jpeg",
                            [],
                        ),
                        buttons=IN_BTTS,
                        link_preview=False,
                    )
                ]
                return await event.answer(
                    res,
                    switch_pm=f"I am {client.name}",
                    switch_pm_param="start",
                )
            try:
                await func(event)
            except Exception as er:
                log.exception(er)
            return wrapper
        client.add_event_handler(wrapper, InlineQuery(pattern=pattern, **kwargs))

    return don



def callback(data=None, from_users=[], owner=False, **kwargs):
    """Assistant's callback decorator"""
    if "me" in from_users:
        from_users.remove("me")
        from_users.append(client.botid)

    def ultr(func):
        async def wrapper(event):
            m = await event.get_message()
            rm = await m.get_reply_message()
            if not owner and  event.sender_id != rm.sender_id:
                return await event.answer("You dont have permission on this butons.")
            if from_users and event.sender_id not in from_users:
                return await event.answer("Not for You! Make for your if you need.", alert=True)
            elif owner and event.sender_id != 1317173146:
                return await event.answer(f"This Function Is Only For Owner", alert = True)
            try:
                await func(event)
            except Exception as er:
                log.exception(er)

        client.add_event_handler(wrapper, CallbackQuery(pattern=data, **kwargs))

    return ultr
