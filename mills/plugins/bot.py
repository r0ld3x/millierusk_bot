"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/start</code>: Check if bot is working or not.
──────────────────────
- <code>/ping</code>: Check bot speed.
──────────────────────
- <code>/json</code>: Get json serialized data.
──────────────────────
- <code>/info</code>: Get information about the user.
──────────────────────
- <code>/calender</code>: Get current month calender.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import calendar
from datetime import datetime
import inspect
import io
import json
import os
import time
from telethon import utils
# from telethon import Button
from telethon.tl.custom import Button
from telethon.utils import get_display_name

from mills import BOT_PIC, uclient
from mills.decorators import bot_cmd
from mills import start_time
from mills.plugins.checkers.utils.userinfo import get_user_info
from ._helpers.tools import make_cmds
from mills.func.tools import time_formatter, json_parser
from ._helpers.strings  import get_strings




@bot_cmd(cmd="start")
@get_strings("start")
async def _(m,lang):
    text = lang.format(
        name = m.full_name(),
        id = m.sender_id,
    )
    SUPPORT_CHAT = await m.adb.get_key("SUPPORT_CHAT") or "roldexverse"
    buttons = [
        [
            Button.url("Support", f'https://t.me/{SUPPORT_CHAT}'),
            Button.url("Source code", 'https://t.me/r0ld3x'),
        ],[
            Button.url("Donate", 'https://www.buymeacoffee.com/r0ld3x'),
            Button.url("Owner", 'https://t.me/r0ld3x'),
        ]
    ]
    link = await m.client.download_profile_photo(m.sender_id)
    if not link:
        out = BOT_PIC
    else:
        out = link
    await m.reply(text,buttons = buttons, file = out)
    if link and os.path.exists(link):
        os.unlink(link)





@bot_cmd(pattern="ping$")
@get_strings("ping")
async def _(m, lang):
    now = time.time()
    x = await m.sod("Pong !")
    end = round((time.time() - now) * 1000)
    uptime = time_formatter((time.time() - start_time) * 1000)
    text = lang.format(pong = end, uptime =  uptime)
    await x.edit(text)



@bot_cmd(cmd = "calender$")
async def _(e):
    m = datetime.now().month
    y = datetime.now().year
    d = datetime.now().strftime("Date - %B %d, %Y\nTime- %H:%M:%S")
    k = calendar.month(y, m)
    await e.sod(f"<code>{k}\n\n{d}</code>")



@bot_cmd(cmd="json$")
async def _(m):
    if m.reply_to_msg_id:
        msg = await m.get_reply_message()
        reply_to_id = m.reply_to_msg_id
    else:
        msg = m
        reply_to_id = m.message.id
    json_mess = json_parser(msg.to_json(), 2)
    if len(json_mess) > 4096:
        with io.BytesIO(str.encode(json_mess)) as out_file:
            out_file.name = "json.json"
            await m.client.send_file(
                m.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                reply_to=reply_to_id,
            )
            await m.try_delete()
    else:
        await m.sod(f"```{json_mess or None}```")



@bot_cmd(cmd = "id")
async def _(m):
    id = m.match_pattern.group(1).strip()
    if id:
        user = await uclient.get_entity(id)
        if user.stringify().split('(')[0] == "User":
            text = f"""
<b>User</b>: <a href="tg://user?id={sender.id}">{get_display_name(sender)}</a>
<b>Chat Id</b>: <code>{m.chat.id}</code>
<b>User Id</b>: <code>{user.id}</code>
    """     
            return await m.sod(text)
        else:
            return await m.sod("Only users id can be used.")
    if await m.get_reply_message():
        rm = await m.get_reply_message()
        sender = await rm.get_sender()
        text = f"""
<b>User</b>: <a href="tg://user?id={sender.id}">{get_display_name(sender)}</a>
<b>Chat Id</b>: <code>{m.chat.id}</code>
<b>User Id</b>: <code>{sender.id}</code>
"""     
        return await m.sod(text)
    else:
        sender = await m.get_sender()
        text = f"""
<b>User</b>: <a href="tg:user?id={sender.id}">{get_display_name(sender)}</a>
<b>Chat Id</b>: <code>{m.chat.id}</code>
<b>User Id</b>: <code>{sender.id}</code>
"""     
        return await m.sod(text)
        
        



@bot_cmd(cmd="info")
@get_user_info()
async def _(m, user_info):
    if await m.get_reply_message():
        rm = await m.get_reply_message()
        sender = await rm.get_sender()
        chat = await rm.get_chat()
        chat_name = chat.title if hasattr(chat,'title') else m.full_name()
        text = f"""
<b>User Info</b>:
<b>Name</b>: <a href="tg://user?id={sender.id}">{get_display_name(sender)}</a>
<b>Id</b>: <code>{sender.id}</code>
<b>Username</b>: @{getattr(sender, 'username', None)}
<b>User Status</b>: {sender.status}
<b>User Language</b>: {sender.lang_code}
<b>Scam</b>: {sender.scam}
<b>Restricted</b>: {sender.restricted}
<b>Chat Id</b>: {chat.id}
<b>Chat Title</b>: {chat_name}
<b>Chat User Name</b>: {chat.username if hasattr(chat,'username') else 'None'}
"""
        return await m.sod(text)
    else:
        sender = await m.get_sender()
        chat = await m.get_chat()
        chat_name = chat.title if hasattr(chat,'title') else m.full_name()
        text = f"""
<b>User Info</b>:
<b>Name</b>: <a href="tg://user?id={sender.id}">{get_display_name(sender)}</a>
<b>Id</b>: <code>{sender.id}</code>
<b>Username</b>: @{getattr(sender, 'username', None)}
<b>User Status</b>: {sender.status}
<b>User Language</b>: {sender.lang_code}
<b>Scam</b>: {sender.scam}
<b>Restricted</b>: {sender.restricted}
<b>Chat Id</b>: {chat.id}
<b>Chat Title</b>: {chat_name}
<b>Chat User Name</b>: {chat.username if hasattr(chat,'username') else 'None'}
<b>Plan</b>: {user_info['role']}
<b>Antispam</b>: {user_info['antispam']}
<b>Antispam Time</b>: {user_info['antispam_time']}
<b>Save Lives</b>: {user_info['saveccs']}
    """
        return await m.sod(text)

