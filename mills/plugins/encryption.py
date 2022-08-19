"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/encode</code>: Base64 encode the given text.
──────────────────────
- <code>/decode</code>: base64 decode the given hash.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import inspect
import io
import json
import os
import time
import requests
import base64
from io import BytesIO
from telethon import utils
# from telethon import Button
from telethon.tl.custom import Button



from mills.decorators import bot_cmd
from ._helpers.strings  import get_strings
from ._helpers.tools import mediainfo
from mills import client


@bot_cmd(cmd="encode")
async def encode(m):
    text = m.pattern_match.group(1)
    if not text : #and not m.reply_to
        await m.sod("Give me a valid text.", time = 5)
    message_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    if not base64_message:
        return await m.sod("Error while encoding.")
    await m.sod("Encoded: `{}`".format(base64_message))
    return
    # if m.reply_to:
    #     reply_msg = await m.get_reply_message()
    #     if not reply_msg.media:
    #         await m.sod("I didn'nt found any image in replied text. please reply to a image.")
    #         return
    #     if not mediainfo(reply_msg.media).startswith('pic'):
    #         await m.sod("reply with a image. i only support image encoding now.")
    #         return
    #     __ = await client.download_media(reply_msg)
    #     if not __:
    #         await m.sod("Invalid image.")
    #         return
    #     with open(__, 'rb') as f:
    #         data = base64.b64encode(f.read())
    #         print(data.decode('ascii'))
    #     os.remove(__)





@bot_cmd(cmd="decode")
async def decode(m):
    text = m.pattern_match.group(1)
    if not text or not text.endswith('='): #and not m.reply_to
        await m.sod("Give me a valid hash.", time = 5)
    message_bytes = text.encode('ascii')
    base64_bytes = base64.b64decode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    if not base64_message:
        return await m.sod("Error while decoding.")
    await m.sod("Decoded: `{}`".format(base64_message))
    return