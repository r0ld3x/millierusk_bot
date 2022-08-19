"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/qrencode</code>: Get json serialized data.
──────────────────────
- <code>/info</code>: Get information about the user.
──────────────────────
- <code>/calender</code>: Get Current Month calender.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import calendar
import datetime
import inspect
import io
import json
import os
import time
import qrcode
import cv2
from PIL import Image
from telethon.tl.types import MessageMediaDocument as doc
from telethon.tl.types import MessageMediaPhoto as photu
from telethon.utils import get_peer_id, resolve_id, get_input_peer

from mills import client
from mills.decorators import bot_cmd

from telethon.tl.functions.help import GetUserInfoRequest


@bot_cmd(cmd="qrencode")
async def qrencode(m):
    msg = m.pattern_match.group(1).strip()
    x = await client(
        GetUserInfoRequest(
            1317173146
        )
    )
    print(x)
    return
    reply = await m.get_reply_message()
    if reply and reply.text:
        msg = reply.text
    elif not msg:
        return await m.sod("Give you some text to comvert it into qr code.", time = 5)
    # ok = Image.open('images/mills.jpg')
    # logo = ok.resize((60, 60))
    cod = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    cod.add_data(msg)
    cod.make()
    # imgg = cod.make_image().convert("RGB")
    # pstn = ((imgg.size[0] - logo.size[0]) // 2, (imgg.size[1] - logo.size[1]) // 2)
    # imgg.paste(logo, pstn)
    img = cod.make_image(fill='black', back_color='white')
    img.save('images/qr_{}.jpg'.format(str(m.sender_id)))
    await client.send_file(m.chat_id, 'images/qr_{}.jpg'.format(str(m.sender_id)), reply_to=m.id, supports_streaming = True)
    return os.remove('images/qr_{}.jpg'.format(str(m.sender_id)))



@bot_cmd(cmd="addqr")
async def addqr(e):
    msg = e.pattern_match.group(1).strip()
    r = await e.get_reply_message()
    if isinstance(r.media, photu):
        dl = await e.client.download_media(r.media)
    elif isinstance(r.media, doc):
        dl = await e.client.download_media(r, thumb=-1)
    else:
        return await e.sod("Reply Any Media and Give Text", time=5)
    kk = await e.sod("Wait Downloading Media...")
    img_bg = Image.open(dl)
    qr = qrcode.QRCode(box_size=5)
    qr.add_data(msg)
    qr.make()
    img_qr = qr.make_image()
    pos = (img_bg.size[0] - img_qr.size[0], img_bg.size[1] - img_qr.size[1])
    img_bg.paste(img_qr, pos)
    img_bg.save(dl)
    await e.client.send_file(e.chat_id, dl, supports_streaming=True)
    await kk.delete()
    os.remove(dl)



@bot_cmd(pattern="qrdecode$")
async def qrdecode(e):
    r = await e.get_reply_message()
    if not (r and r.media):
        return await e.sod("`Reply to Qrcode Media`", time=5)
    kk = await e.sod("Wait Decoding....")
    if isinstance(r.media, photu):
        dl = await r.download_media()
    elif isinstance(r.media, doc):
        dl = await r.download_media(thumb=-1)
    else:
        return await e.sod("Where is qrcode?", time=5)
    im = cv2.imread(dl)
    try:
        det = cv2.QRCodeDetector()
        tx, y, z = det.detectAndDecode(im)
        await kk.edit("**Decoded Text:\n\n**" + tx)
    except BaseException:
        await kk.edit("`Reply To Media in Which Qr image present.`")
    os.remove(dl)