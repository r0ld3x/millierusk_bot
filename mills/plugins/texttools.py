"""
≛ <b>Commands Available</b> ≛

──────────────────────
<code>/gtts</code> text : Get voice of the text.
──────────────────────
<code>/ytdl</code> url : Download YouTube videos.
──────────────────────
<code>/short</code> url : Get short link of long links..
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import asyncio
import inspect
import io
import json
import os
from random import shuffle
import aiohttp
import validators
import qrcode
import cv2
import numpy as np
import pytesseract
from numerize import numerize
from gtts import gTTS

from pytube import YouTube
from urllib.parse import urlparse
from PIL import Image
from telethon.tl.types import MessageMediaDocument as doc
from telethon.tl.types import MessageMediaPhoto as photu
from telethon import Button
from bs4 import BeautifulSoup
from selenium import webdriver

from mills.decorators import bot_cmd
from mills.func.tools import convert_size, download_file, isValidURL, web_search
from mills import client
from ._helpers.tools import Carbon1


@bot_cmd(cmd="gtts", text_only = True)
async def gtts(m):
    query = m.pattern_match.group(1)
    if not query:
        return m.sod("use this command with a text.")
    myobj = gTTS(text=query)
    myobj.save(f"downloads/{m.sender_id}_text.mp3")
    if os.path.exists(f"downloads/{m.sender_id}_text.mp3"):
        await m.sod(file = f"downloads/{m.sender_id}_text.mp3")
        os.unlink(f"downloads/{m.sender_id}_text.mp3")
    else:
        return await m.sod("Error While Converting.")




@bot_cmd(cmd="short", text_only = True)
async def short(m):
    link = m.pattern_match.group(1).strip()
    if not link or not isValidURL(link):
        return await m.sod("Give me a valid link.")
    header = {
        "Authorization": "Bearer ad39983fa42d0b19e4534f33671629a4940298dc",
        "Content-Type": "application/json",
    }
    payload = {"long_url": f"{link}"}
    payload = json.dumps(payload)
    data = None
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api-ssl.bitly.com/v4/shorten", headers=header, data=payload
        ) as resp:
            data = await resp.json()
    if data:
        msg = f"""
Original Url: [Click Here]({link})
Shortened Url: {data['link']}
    """
        return await m.sod(msg)
    else:
        return await m.sod("Give me a valid link.")