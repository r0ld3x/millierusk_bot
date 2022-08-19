
import asyncio
from datetime import datetime
import io
import math
import os, sys
import re
import time
from markdown import markdown
from pymongo import MongoClient
import pymongo

from telethon import Button
from mills import ADMINS, BOT_PIC, sdb
from mills.plugins.checkers.utils.bininfo import get_bin_info, get_bin_info_all

from mills.plugins.checkers.utils.tools import cc_gen
from mills.decorators import callback
from mills.func.funcs import progress
from mills.func.tools import humanbytes, time_formatter
from . import ADMIN_HELP, MOD_HELP, Telegraph_client
from mills.plugins._helpers.tools import make_buttons,count_keys, make_buttons_checkers, short_list
from mills import client, start_time
from mills.func.FastTelethon import upload_file



@callback(re.compile("help_(.*)"))
async def _(m):
    key, index = m.data_match.group(1).decode("utf-8").split('_')
    if key == 'checkers':
        cols= make_buttons_checkers()
        return await m.edit("Click on buttons for gates cmds.", buttons = cols)   
    else:
        if key in MOD_HELP:
            cmds = MOD_HELP[key]
            text = f"""
<b>Module Name</b>: {key}
<b>Page Number</b>: {index}
<b>Total Commands</b>: {count_keys(cmds)}
    """     
            butt = make_buttons(index, key)
            await m.edit(text,buttons = butt)
        else:
            await m.answer("No Module Found With This Name. You Can Use <code>.help</code> To See All Modules.")


@callback(re.compile("cmds_(.*)"))
async def _(m):
    key, index = m.data_match.group(1).decode("utf-8").split('_')
    if key in MOD_HELP:
        cmds = MOD_HELP[key]
        text = f"""
<b>Module Name</b>: {key}
<b>Page  Number</b>: {index}
<b>Total Commands</b>: {count_keys(cmds)}
"""     
        await m.edit(text,buttons = make_buttons(index, key))
    else:
        await m.answer("No Module Found With This Name. You Can Use <code>.help</code> To See All Modules.")



@callback(re.compile("admins_(.*)"))
async def _(m):
    key= m.data_match.group(1).decode("utf-8")
    if key in ADMIN_HELP:
        cmds = ADMIN_HELP[key]
        __buttons = [
            [
                Button.inline("Back", data = f"acmds")
            ],
            [
                Button.inline("☒", data="closeadmin"),
            ]
            ]
        await m.edit(cmds, buttons = __buttons)
    else:
        await m.answer("No Module Found With This Name. You Can Use <code>.help</code> To See All Modules.")



##gen
@callback(re.compile("gen_(.*)"))
async def _(m):
    mm = await m.get_message()
    mm = await mm.get_reply_message()
    cc,mes,ano,cvv= m.data_match.group(1).decode("utf-8").split('_')
    bin_info = get_bin_info(str(cc[:6]))
    ccs = cc_gen(cc,mes,ano,cvv)
    cards = '\n'.join(ccs)
    mess = f"""
<b>Card Generator</b>:
<b>Bin</b>: <code>{cc}</code>
<b>Bank</b>: <b>{bin_info['bank_name']}</b> - <b>{bin_info['iso']}</b>
<b>Info</b>: <b>{bin_info['type']}</b> - <b>{bin_info['level']}</b>
<b>User</b>:  <a href="tg://user?id={m.sender_id}">{mm.full_name()}</a> 
<b>Cards</b>: 
{cards}
"""
    buttons = [
        Button.inline("Gen Again", f'gen_{cc}_{mes}_{ano}_{cvv}')
    ]
    await m.edit(mess, buttons = buttons)



@callback(re.compile("acmds"))
async def _(m):
    __buttons = [ Button.inline(f" {x} ", data = f"admins_{x}") for x in sorted(ADMIN_HELP.keys())]
    rows = short_list(__buttons, 3)
    cols = short_list(rows, 4)
    buttons =  cols[0] if cols else []
    buttons.append([
        Button.inline("☒", data="closeadmin"),
    ])
    mm = await m.get_message()
    mm = await mm.get_reply_message()
    text = f"""
<i>Select One Button From Below.</i>
"""         
    await m.edit(text, buttons = buttons)



@callback(re.compile("closeadmin"))
async def _(m):
    try:
        await m.delete()
    except:
        pass






@callback(re.compile("plugins_(.*)"))
async def _(m):
    key, index = m.data_match.group(1).decode("utf-8").split('_')
    if key in MOD_HELP['plugins']:
        text = MOD_HELP['plugins'][key]
        buttons = [
            [
                Button.inline('Back', f"cmds_plugins_{index}")
            ]
        ]
        await m.edit(text,buttons = buttons)
    else:
        await m.answer("No Module Found With This Name. You Can Use <code>.help</code> To See All Modules.")



@callback("main")
async def _(m):
    mm = await m.get_message()
    mm = await mm.get_reply_message()
    text = f"""
<b>Total commands</b>: {count_keys(MOD_HELP)}

<b>User Name</b>: {getattr(mm.sender, 'username', None)}
<b>User Id</b>: <code>{mm.sender_id}</code>
<b>Chat Id</b>: <code>{mm.chat_id}</code>

<i>Select One Button From Below.</i>
"""     
    __buttons = [
            [ Button.inline(x, data = f"help_{x}_")
                for x in sorted(MOD_HELP.keys())
            ],
            [
                Button.inline("☒", data="close"),
            ]
        ]
    await m.edit(text,buttons=__buttons)



@callback(data="close")
async def on_plug_in_callback_query_handler(event):
    await event.edit(
        "<b>Menu Closed</b>.",
        buttons=Button.inline("Open Again", data="main"),
    )



@callback(data="auth")
async def auth(event):
# ───────────────────────
    text = f"""
╭─━━━━━━━━━━━━━━━━━━━─╮
                <b>Auth Gates</b>
╰─━━━━━━━━━━━━━━━━━━━─╯e
"""
    finded = sdb['gate'].find({'gate_type': 'auth'}, {'_id':0, 'cmd_name': 1 , 'status_logo': 1, 'gate_name': 1, 'is_paid': 1}).sort("abc",pymongo.DESCENDING)
    finded = list(finded)
    iter_length = len(finded)
    text += f"Total Auth gates: {iter_length}\n\n"
    for a in finded:
        text += f"""
───────────────────────
[×] {a['gate_name']}:- <code>/{a['cmd_name']}</code>
[×] State: {a['status_logo']} | Paid: {a['is_paid']}
"""
        # text += f"<code>/{a['cmd_name']}</code> - {a['gate_name']} - {a['status_logo']} - {a['is_paid']}\n───────────────────────\n"
    text += "\n───────────────────────\n<i>Choose other buttons for other gates</i>."
    butt = [
            # Button.inline(" Auth ", data = f"auth"),
            Button.inline(" Charge ", data = f"charge"),
            Button.inline(" Others ", data = f"other"),
            Button.inline(" Mass ", data = f"mass"),
            Button.inline(" Tools ", data = f"tools"),
        ]
    rows = short_list(butt, 3)
    cols = short_list(rows, 4)
    buttons =  cols[0] if cols else []
    buttons.append([Button.inline("« Back", data="main"),Button.inline("☒", data="close")])
    return await event.edit(text, buttons = buttons)



@callback(data="charge")
async def charge(event):
    text = f"""
╭─━━━━━━━━━━━━━━━━━━━─╮
              <b>Charge Gates</b>
╰─━━━━━━━━━━━━━━━━━━━─╯
"""
    finded = sdb['gate'].find({'gate_type': 'charge'}, {'_id':0, 'cmd_name': 1 , 'status_logo': 1, 'gate_name': 1, 'is_paid': 1, 'charge_amount': 1, }).sort("abc",pymongo.DESCENDING)
    finded = list(finded)
    iter_length = len(finded)
    text += f"<b>Total charge gates</b>: {iter_length}\n\n" 
    for a in finded:
        text += f"""
───────────────────────
[×] {a['gate_name']} ${a['charge_amount']}:- <code>/{a['cmd_name']}</code>
[×] State: {a['status_logo']} | Paid: {a['is_paid']}
"""
        # text += f"<code>/{a['cmd_name']}</code> - {a['gate_name']}-${a['charge_amount']} - {a['status_logo']} - {a['is_paid']}\n───────────────────────\n"
    text += "\n───────────────────────\n<i>Choose other buttons for other gates</i>."
    butt = [
            Button.inline(" Auth ", data = f"auth"),
            # Button.inline(" Charge ", data = f"charge"),
            Button.inline(" Others ", data = f"other"),
            Button.inline(" Mass ", data = f"mass"),
            Button.inline(" Tools ", data = f"tools"),
        ]
    rows = short_list(butt, 3)
    cols = short_list(rows, 4)
    buttons =  cols[0] if cols else []
    buttons.append([Button.inline("« Back", data="main"),Button.inline("☒", data="close")])
    return await event.edit(text, buttons = buttons)




@callback(data="other")
async def other(event):
    text = f"""
╭─━━━━━━━━━━━━━━━━━━━─╮
               <b>Other Gates</b>
╰─━━━━━━━━━━━━━━━━━━━─╯
"""
    finded = sdb['gate'].find({'gate_type': 'other'}, {'_id':0, 'cmd_name': 1 , 'status_logo': 1, 'gate_name': 1, 'is_paid': 1, 'charge_amount': 1}).sort("abc",pymongo.DESCENDING)
    finded = list(finded)
    iter_length = len(finded)
    text += f"Total other gates: {iter_length}\n\n"
    for a in finded:
        text += f"""
───────────────────────
[×] {a['gate_name']}:- <code>/{a['cmd_name']}</code>
[×] State: {a['status_logo']} | Paid: {a['is_paid']}
"""
        # text += f"<code>/{a['cmd_name']}</code> - {a['gate_name']} - {a['status_logo']} - {a['is_paid']}\n───────────────────────\n"
    text += "<i>Choose other buttons for other gates.</i>"
    butt = [
            Button.inline(" Auth ", data = f"auth"),
            Button.inline(" Charge ", data = f"charge"),
            # Button.inline(" Others ", data = f"other"),
            Button.inline(" Mass ", data = f"mass"),
            Button.inline(" Tools ", data = f"tools"),
        ]
    rows = short_list(butt, 3)
    cols = short_list(rows, 4)
    buttons =  cols[0] if cols else []
    buttons.append([Button.inline("« Back", data="main"),Button.inline("☒", data="close")])
    return await event.edit(text, buttons = buttons)



@callback(data="mass")
async def mass(event):
    text = f"""
╭─━━━━━━━━━━━━━━━━━━━─╮
               <b>Mass Gates</b>
╰─━━━━━━━━━━━━━━━━━━━─╯
"""
    finded = sdb['gate'].find({'gate_type': 'mass'}, {'_id':0, 'cmd_name': 1 , 'status_logo': 1, 'gate_name': 1, 'is_paid': 1, 'charge_amount': 1}).sort("abc",pymongo.DESCENDING)
    finded = list(finded)
    iter_length = len(finded)
    text += f"Total mass gates: {iter_length}\n\n"
    for a in finded:
        text += f"""
───────────────────────
[×] {a['gate_name']}:- <code>/{a['cmd_name']}</code>
[×] State: {a['status_logo']} | Paid: {a['is_paid']}
"""
        # text += f"`/{a['cmd_name']}` - {a['gate_name']} - {a['status_logo']} - {a['is_paid']}\n───────────────────────\n"
    text += "\n───────────────────────\n<i>Choose other buttons for other gates</i>."
    butt = [
            Button.inline(" Auth ", data = f"auth"),
            Button.inline(" Charge ", data = f"charge"),
            Button.inline(" Others ", data = f"other"),
            # Button.inline(" Mass ", data = f"mass"),
            Button.inline(" Tools ", data = f"tools"),
        ]
    rows = short_list(butt, 3)
    cols = short_list(rows, 4)
    buttons =  cols[0] if cols else []
    buttons.append([Button.inline("« Back", data="main"),Button.inline("☒", data="close")])
    return await event.edit(text, buttons = buttons)



@callback(data="tools")
async def tools(event):
    text = f"""
╭─━━━━━━━━━━━━━━━━━━━─╮
                <b>Tools</b>
╰─━━━━━━━━━━━━━━━━━━━─╯
<code>/bin bin</code> - Check bin
───────────────────────
<code>/claim key</code> - Claim premium key
───────────────────────
<code>/gen bin</code> - Generate cards from bin
───────────────────────
<code>/scrape username amount</code> - Scrape amount no. cards from the username
───────────────────────
<code>/sk sk_key</code> - Check Sk key

"""
    
    butt = [
            Button.inline(" Auth ", data = f"auth"),
            Button.inline(" Charge ", data = f"charge"),
            Button.inline(" Others ", data = f"other"),
            Button.inline(" Mass ", data = f"mass"),
            # Button.inline(" Tools ", data = f"tools"),
        ]
    rows = short_list(butt, 3)
    cols = short_list(rows, 4)
    buttons =  cols[0] if cols else []
    buttons.append([Button.inline("« Back", data="main"),Button.inline("☒", data="close")])
    return await event.edit(text, buttons = buttons)




@callback(data="pkng", owner=True)
async def _(event):
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds
    pin = f"🌋Pɪɴɢ = {ms} microseconds"
    await event.answer(pin, cache_time=0, alert=True)
    



@callback(data="upp", owner=True)
async def _(event):
    uptime = time_formatter((time.time() - start_time) * 1000)
    pin = f"Uptime = {uptime}"
    await event.answer(pin, cache_time=0, alert=True)


from pytube import YouTube

No_Flood= {}


async def progress(current, total, event, start,file_name):
    bar_len = 20
    filled_len = int(round(bar_len * current / float(total)))

    percents = round(100.0 * current / float(total), 1)
    bar = '|' * filled_len + '-' * (bar_len - filled_len)
    text = "Downloading File: {%s}\nProgress: [%s%s] %s%s%s\r" % (file_name, bar, percents, '%')
    await event.edit(text)
#     now = time.time()
#     if No_Flood.get(event.chat_id):
#         if No_Flood[event.chat_id].get(event.id):
#             if (now - No_Flood[event.chat_id][event.id]) < 1.1:
#                 return
#         else:
#             No_Flood[event.chat_id].update({event.id: now})
#     else:
#         No_Flood.update({event.chat_id: {event.id: now}})
#     diff = time.time() - start
# # if round(diff % 10.00) == 0 or current == total:
#     percentage = current * 100 / total
#     speed = current / diff
#     time_to_completion = round((total - current) / speed) * 1000
#     progress_str = "`[{0}{1}] {2}%`\n\n".format(
#         "".join("█" for i in range(math.floor(percentage / 5))),
#         "".join("" for i in range(20 - math.floor(percentage / 5))),
#         round(percentage, 2),
#     )

#     tmp = (
#         progress_str
#         + "Uploaded: {0} of {1}\nSpeed: `{2}/s`\nETA: `{3}`\n\n".format(
#             humanbytes(current),
#             humanbytes(total),
#             humanbytes(speed),
#             time_formatter(time_to_completion),
#         )
#     )
#     if file_name:
#         await event.edit(
#             "\n\nFile Name: `{}`\nProgress: `{}`".format(file_name, tmp)
#         )
#     else:
#         await event.edit("`\n\n{}".format(tmp))




@callback(re.compile("yt_down_(.*)"))
async def _(m):
    link, id = m.data_match.group(1).decode("utf-8").split("_")
    link = 'https://youtube.com' + link
    try:
        yt = YouTube(link)
    except:
        return await m.answer("Unkown Error")  
    xx = await m.reply("Wait Trying to download youtube media...")
    mess = await m.get_message()
    if id == 'mp3':
        get = yt.streams.filter(only_audio=True).first()
        out_file = get.download('downloads/')
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        cap = f"""
Title: {get.title}
Length: {yt.length}
Author: {yt.author}
Type: {get.type}
Resolution: {get.resolution}
Channel Link:  <a href="{yt.channel_url}">{yt.author}</a>
Download Link: <a href="{get.url}">Click</a> """
        await xx.delete()
        await client.send_file(mess.chat,reply_to = mess.id,file = new_file,supports_streaming = True, caption =cap)
        os.unlink(new_file) #progress_callback = lambda a,b: progress(a,b,xx,deff,get.title)
        return
    get = yt.streams.get_by_itag(id)
    path = get.download('downloads/')
    cap = f"""
Title: {get.title}
Length: {yt.length}
Author: {yt.author}
Type: {get.type}
Resolution: {get.resolution}
Channel Link:  <a href="{yt.channel_url}">{yt.author}</a>
Download Link: <a href="{get.url}">Click</a> 
"""
    await xx.delete()
    await client.send_file(mess.chat,reply_to = mess.id,file = path,supports_streaming = True,caption= cap )
    os.unlink(path) #progress_callback = lambda a,b: progress(a,b,xx,deff,get.title)
    return