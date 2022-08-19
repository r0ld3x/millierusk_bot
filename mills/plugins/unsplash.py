"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/unsplash</code> : Get images from <code>unsplash.com</code>.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import asyncio
import inspect
import io
from random import shuffle
import re
import os
import bs4
from urllib.request import urlopen
import requests
from telethon import utils
# from telethon import Button
from telethon.tl.custom import Button
from ._helpers.tools import unsplashsearch



from mills.decorators import bot_cmd
from mills.func.tools import download_file, web_search




@bot_cmd(cmd="unsplash")
async def unsplash(m):
    query = m.pattern_match.group(1).strip().replace(" ", "+")
    if not query: return await m.sod("give me a text. Usage: `.unsplash image `")
    # input = re.findall(r"[0-9]+", query) or 1
    res = await unsplashsearch(query, limit=1)
    CL = [download_file(rp, f"images/{query}-{e}.png") for e, rp in enumerate(res)]
    imgs = [z for z in (await asyncio.gather(*CL)) if z]
    await m.client.send_file(
        m.chat_id, imgs, caption=f"Uploaded {len(imgs)} Images!"
    )
    [os.remove(img) for img in imgs]