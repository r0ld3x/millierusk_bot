"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/cmds</code>: Get all available commands with detailed information with telegraph.
──────────────────────
- <code>/help<code>: Get all available commands with detailed information.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import inspect
import io
import json
import os
import time
from fuzzywuzzy.process import extractOne
from telethon import utils
# from telethon import Button
from telethon.tl.custom import Button

from mills import BOT_PIC, client
from mills.decorators import bot_cmd
from mills.func.tools import cmd_regex_replace
from mills.plugins._helpers.tools import make_buttons,count_keys, make_cmds, short_list
from . import ADMIN_HELP, LIST, MOD_HELP




@bot_cmd(cmd="cmds")
async def _(m):
    match = m.pattern_match.group(1).strip().replace('@'+ client.me.username,'')
    __buttons = [
            [ Button.inline(f" {x} ", data = f"help_{x}_")
                for x in sorted(MOD_HELP.keys())
            ],
            [
                Button.inline("☒", data="close"),
            ]
        ]
    if not match:
        text = f"""
<b>Total Commands</b>: {count_keys(MOD_HELP)}

<b>User Name</b>: {m.sender.username}
<b>User Id</b>: <code>{m.sender_id}</code>
<b>Chat Id</b>: <code>{m.chat_id}</code>

<i>Select One Button From Below.</i>
"""
        await m.reply(text,buttons=__buttons, file = BOT_PIC)
    else:
        file = None
        strings = []
        for x in LIST:
            if match in x:
                file = x
            for xx in LIST[x]:
                regexed = cmd_regex_replace(xx)
                strings.append(regexed)
                if match in regexed:
                    file = x
        if file:
            for x in MOD_HELP:
                if file == x:
                    best_match = extractOne(match,strings)
                    return await m.sod("{} is not a valid plugin. Do you mean `{}`".format(file, best_match))
                else:
                    for xx in MOD_HELP[x]:
                        if file in xx:
                            out = f"<b>Command</b> <code>{match}</code> <b>is found in {file}</b>.\n"
                            out += MOD_HELP[x][xx]
                            await m.sod(out, file = BOT_PIC)

        if not file:
            best_match = extractOne(match,strings)
            return await m.sod("{} is not a valid plugin. Do you mean `{}`".format(file, best_match))



@bot_cmd(cmd="acmds", admins_only = True)
async def _(m):
    __buttons = [
        [
            Button.inline("Open", data = f"acmds")
        ],
        [
            Button.inline("☒", data="closeadmin"),
        ]
                ]
    text = f"""
<b>Total Commands</b>: {count_keys(ADMIN_HELP)}

<b>User Name</b>: {m.sender.username}
<b>User Id</b>: <code>{m.sender_id}</code>
<b>Chat Id</b>: <code>{m.chat_id}</code>

<i>Select One Button From Below.</i>
"""
    await m.reply(text,buttons=__buttons, file = BOT_PIC)



@bot_cmd(cmd="help")
async def _(m):
    match = m.pattern_match.group(1).strip().replace('@'+ client.me.username,'')
    if not match:
        await make_cmds(m)
    else:
        file = None
        for x in LIST:
            if match in x:
                file = x
            # for xx in LIST[x]:
            #     regexed = cmd_regex_replace(xx)
            #     if match in regexed:
            #         file = x
        if file:
            for x in MOD_HELP:
                if file == x:
                    return await m.sod("{} is not a valid plugin. ".format(file))
                else:
                    for xx in MOD_HELP[x]:
                        if file in xx:
                            out = f"<b>Command</b> <code>{match}</code> <b>is found in {file}</b>.\n"
                            out += MOD_HELP[x][xx]
                            await m.sod(out, file = BOT_PIC)
                        else:
                            return await m.sod("{} is not a valid plugin. ".format(file))
                                
        if not file:
            return await m.sod("{} is not a valid plugin. ".format(file))


