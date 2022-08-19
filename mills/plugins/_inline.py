
import datetime
import os, sys
import re
import time
from markdown import markdown
from telegraph import upload_file



from telethon.tl.types import InputWebDocument, Message
from telethon import Button
from mills import ADMINS, BOT_PIC, mdb,adb

from mills.decorators import callback, in_pattern
from mills.func.tools import time_formatter, web_search
from mills.plugins._helpers.tools import Carbon1
from mills.plugins.checkers.utils.bininfo import get_bin_info
from mills import client
from mills.plugins.checkers.utils.tools import cc_gen





SUP_BUTTONS = [
    [
        Button.url("• Github •", url="https://github.com/r0ld3x"),
        Button.url("• Support •", url="t.me/roldexverse"),
    ],
    [
        Button.inline("• Up Time •", "upp"),
        Button.inline("• Ping •","pkng"),
    ],
]


HELP_BUTTONS = [
    [
        Button.url("• Owner •", url="https://t.me/r0ld3x"),
        Button.url("• Support •", url="https://t.me/roldexverse"),
    ],
]

@in_pattern(func=lambda x: not x.text)
async def inline_alive(m):
    
    RES = [
        await m.builder.article(
            text=f"☰ <b><i>Bin lookup</i></b>\n<b>Example</b>:  <code>@{client.botname} bin 458529</code>",
            buttons=HELP_BUTTONS,
            title="Bin lookup",
            description="Get bin lookup.",
            thumb=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
            content=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
        ),
        await m.builder.article(
            text=f"☰ <b><i>Store text online </i></b>\n<b>Example</b>:  <code>@{client.botname} paste text</code>",
            buttons=HELP_BUTTONS,
            title="Paste Bin",
            description="Store text online.",
            thumb=InputWebDocument('https://pastebin.com/themes/pastebin/img/pastebin_logo_side_outline_support_ukraine.png', 0, "image/jpg", []),
            content=InputWebDocument('https://pastebin.com/themes/pastebin/img/pastebin_logo_side_outline_support_ukraine.png', 0, "image/jpg", []),
        ),
        await m.builder.article(
            text=f"☰ <b><i>Generate cards from bin</i></b>\n<b>Example</b>:  <code>@{client.botname} gen 458596</code>",
            buttons=HELP_BUTTONS,
            title="Cards Generator",
            description="Generate cards from bin.",
            thumb=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
            content=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
        ),
        # await m.builder.article(
        #     text=f"☰ <b><i>Create and share beautiful images of your source code. </i></b>\n<b>Example</b>:  <code>@{client.botname} carbon code</code>",
        #     buttons=HELP_BUTTONS,
        #     title="Carbon",
        #     description="Create and share beautiful images of your text.",
        #     thumb=InputWebDocument('https://te.legra.ph/file/06642535b70e47519aea6.jpg', 0, "image/jpg", []),
        #     content=InputWebDocument('https://te.legra.ph/file/06642535b70e47519aea6.jpg', 0, "image/jpg", []),
        # ),
    ]
    if m.sender_id in ADMINS:
        text = f"""
Hey Master! Nice to see you again!
I am <a href="tg://user?id={client.botid}">{client.name}</a>.
<b>Total Users</b>: {await mdb.get_count('users')}
<b>Total Gates</b>: {await mdb.get_count('gate')}
<b>Total Keys</b>: {await mdb.get_count('keys')}
<b>Total Approved Chats</b> : {len(await adb.keys('approved*'))}
"""
        web0 = InputWebDocument(
            BOT_PIC, 0, "image/jpg", []
        )
        RES.append(await m.builder.article(
            text=text,
            buttons=SUP_BUTTONS,
            title=client.name.title(),
            description="ai hodnes checking cards.",
            thumb=web0,
            content=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
        ))
        
    await m.answer(
        RES,
        # private=True,
        # cache_time=300,
        # switch_pm="MILLIE RUSK",
        # switch_pm_param="start",
    )
    


@in_pattern("paste (.*)")
async def _(event):
    text = event.pattern_match.group(1).strip()
    if text:
        doc = await web_search('https://www.toptal.com/developers/hastebin/documents', json = str(text),r_json= True)
        if 'key' in doc:
            raw_key = doc['key']
            raw = 'https://www.toptal.com/developers/hastebin/raw/'+ raw_key
    else:
        x = await event.builder.article(
            text=f"☰ <b><i>Store text online </i></b>\n<b>Example</b>:  <code>@{client.botname} paste text</code>",
            buttons=HELP_BUTTONS,
            title="Paste Bin",
            description="Store text online.",
            thumb=InputWebDocument('https://pastebin.com/themes/pastebin/img/pastebin_logo_side_outline_support_ukraine.png', 0, "image/jpg", []),
            content=InputWebDocument('https://pastebin.com/themes/pastebin/img/pastebin_logo_side_outline_support_ukraine.png', 0, "image/jpg", []),
        ),
        return await event.answer([x])
    if raw:
        result = await event.builder.article(
            title="Pasted",
            text="Pasted to Hastebin",
            description="Paste Text To Hastbin",
            buttons=[
                [
                    Button.url("Hastbin", url=raw),
                    Button.url("Raw", url=raw),
                ],
            ],
        )
        await event.answer([result])
    else:
        result = await event.builder.article(
            title="Give me Text",
            text="Paste Text On Online (Hastebin)",
            description="Give me Text to post in hastebin",
            thumb=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
            content=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
            buttons=[
                [
                    Button.url(client.name, url="t.me/{}".format(client.botname)),
                    Button.url("Channel", url="t.me/roldexverse"),
                ],
            ],
        )
        await event.answer([result])



@in_pattern(re.compile("gen (.*)"))
async def _(m):
    text = m.pattern_match.group(1).strip()
    if len(text) < 6:
        result = await m.builder.article(
            title="Cards Generator",
            text="No bin to generate",
            description="Generate cards from bin.",
            buttons=[
                [
                    Button.url(client.name, url="t.me/{}".format(client.botname)),
                    Button.url("Channel", url="t.me/roldexverse"),
                ],
            ],
        )
        return await m.answer([result])
    input = re.findall(r"[0-9]+", text)
    if len(input) == 0:
        result = await m.builder.article(
            title="Cards Generator",
            text="No bin to generate",
            description="Generate cards from bin.",
            buttons=[
                [
                    Button.url(client.name, url="t.me/{}".format(client.botname)),
                    Button.url("Channel", url="t.me/roldexverse"),
                ],
            ],
            thumb=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
            content=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
        )
        return await m.answer([result])
    if len(input) == 1:
        cc = input[0]
        mes = 'x'
        ano = 'x'
        cvv = 'x'
    elif len(input[0]) < 6 or len(input[0]) > 16:
        result = await m.builder.article(
            title="Cards Generator",
            text="No bin to generate",
            description="Generate cards from bin.",
            buttons=[
                [
                    Button.url(client.name, url="t.me/{}".format(client.botname)),
                    Button.url("Channel", url="t.me/roldexverse"),
                ],
            ],
            thumb=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
            content=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
        )
        return await m.answer([result])
    if len(input) == 2:
        cc = input[0]
        mes = input[1]
        ano = 'x'
        cvv = 'x'
    if len(input) == 3:
        cc = input[0]
        mes = input[1]
        ano = input[2]
        cvv = 'x'
    if len(input) == 4:
        cc = input[0]
        mes = input[1]
        ano = input[2]
        cvv = input[3]
    else:
        bin_info = get_bin_info(str(cc))
        if not bin_info:
            return await m.answer("Unkown Error.")
        ccs = cc_gen(cc,mes,ano,cvv)
        cards = '\n'.join(ccs)
    if not bin_info:
        result = await m.builder.article(
            title="Cards Generator",
            text="Bin Info Not Found",
            description="Generate cards from bin.",
            buttons=[
                [
                    Button.url(client.name, url="t.me/{}".format(client.botname)),
                    Button.url("Channel", url="t.me/roldexverse"),
                ],
            ],
            thumb=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
            content=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
        )
        return await m.answer([result])
    mess = f"""
<b>Card Generator</b>:
<b>Bin</b>: <code>{cc}</code>
<b>Bank</b>: <b>{bin_info['bank_name']}</b> - <b>{bin_info['iso']}</b>
<b>Info</b>: <b>{bin_info['type']}</b> - <b>{bin_info['level']}</b>
<b>Cards</b>: 
{cards}
"""
    result = await m.builder.article(
            title="Cards Generator",
            text=mess,
            description="Generate cards from bin.",
            buttons=[
                [
                    Button.url(client.name, url="t.me/{}".format(client.botname)),
                    Button.url("Channel", url="t.me/roldexverse"),
                ],
            ],
            thumb=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
            content=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
        )
    return await m.answer([result])
        
    


@in_pattern("bin (.*)")
async def ibuild(e):
    n = e.pattern_match.group(1).strip()
    builder = e.builder
    if not n.isdigit() or len(n) < 6:
        ans = [
            e.builder.article(
            text=f"☰ <b><i>Bin lookup</i></b>\n<b>Example</b>:  <code>@{client.botname} bin 458529</code>",
            buttons=HELP_BUTTONS,
            title="Bin lookup",
            description="Get bin lookup.",
            thumb=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
            content=InputWebDocument(BOT_PIC, 0, "image/jpg", []),
        )
        ]
        return await e.answer(ans)
    
    bin = n[:6]
    bin_info = get_bin_info(bin)
    if not bin_info:
        mess = "Bin Info Not Found."
    else:
        mess = f"""
<b>Bin</b>: <code>{bin}</code>
<b>Vendor</b>: <b>{bin_info['vendor']}</b>
<b>Type</b>: <b>{bin_info['type']}</b>
<b>Level</b>: <b>{bin_info['level']}</b>
<b>Prepaid</b>: <b>{bin_info['prepaid']}</b>
<b>Bank name</b>: <b>{bin_info['bank_name']}</b>
<b>Iso</b>: <b>{bin_info['iso']} {bin_info['flag']}</b>
<b>Country</b>: <b>{bin_info['country']}</b>
""" 

    web0 = InputWebDocument(
        BOT_PIC, 0, "image/jpg", []
    )
    
    result = await builder.article(
        thumb=web0,
        title="Bin Information",
        text=mess,
        description="your bin information is ready...",
        # buttons=btn,
        link_preview=False,
    )
    await e.answer([result])


# @in_pattern("tr (.*)")
# async def ibuild(e):
#     n = e.pattern_match.group(1).strip()
#     builder = e.builder
#     if not n.isdigit() or len(n) < 6:
#         return
    
#     language = text.split(maxsplit = 1)
#     if language[0] in LANGCODES or language[0] in LANGUAGES: 
#         t_lang= language[0]
#     else: t_lang = "auto"
#     translator = Translator()
#     print(msg)
#     tr = translator.translate(msg, dest= t_lang)
#     print(tr)
#     print(dir(tr))

#     web0 = InputWebDocument(
#         BOT_PIC, 0, "image/jpg", []
#     )
    
#     result = await builder.article(
#         thumb=web0,
#         title="Bin Search",
#         text=mess,
#         description='@' + client.me.username,
#         # buttons=btn,
#         link_preview=False,
#     )
#     await e.answer([result])


# @in_pattern("upp", owner=True)
# async def upp(event):
#     await event.answer(time_formatter(datetime.datetime.now() - start_time) * 1000)


