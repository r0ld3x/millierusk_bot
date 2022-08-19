"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/carbon</code>: Carbinize the text and gives you a image.
──────────────────────
- <code>/ytdl</code> url : Download YouTube videos.
──────────────────────
- <code>/shorturl</code> url : Download YouTube videos.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import asyncio
import inspect
import io
import os
from random import shuffle
import validators
from mills.func.funcs import progress
import qrcode
import cv2
import numpy as np
import pytesseract
from numerize import numerize


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



@bot_cmd(cmd="webss", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1).strip()
    if not query or not isValidURL(query):
        return await m.sod("Give me a valid link.")
    try:
        await client.send_file(m.chat,f"https://webshot.deam.io/{query}/?delay=2000")
    except:
        return await m.sod("Invalid link.")



@bot_cmd(cmd="ytdl", text_only = True)
async def ytdl(m):
    link = m.pattern_match.group(1).strip()
    if not link or not isValidURL(link):
        return await m.sod("Give me a valid link.")
    try:
        yt = YouTube(link)
    except:
        return await m.sod("Invalid link.")
    xx =await m.sod("Wait extracting information...")
    text = f"""
<b>Title</b>: {yt.title}
<b>Views</b>: {numerize.numerize(yt.views)}
<b>Length</b>: {yt.length}
<b>Author</b>: {yt.author}
<b>Channel Link</b>: <a href="{yt.channel_url}">{yt.author}</a>
    """
    url = yt.thumbnail_url
    buttons = []
    webname = urlparse(link).netloc.split('.')[-1]
    vid_path = link.split(webname)[1]
    fil = yt.streams.filter(progressive=True)
    for x in fil.itag_index:
        get = yt.streams.get_by_itag(x)
        buttons.append([
            Button.inline(f"{str(get.resolution)} {convert_size(get.filesize)}", "yt_down_" +  vid_path + "_"+ str(x))
        ])
    fil = yt.streams.filter(only_audio=True).first()
    buttons.append([
        Button.inline(f"Audio {convert_size(fil.filesize)}", "yt_down_" +  vid_path + "_mp3"
    )])
    await xx.edit(text, file = url, buttons = buttons)
    # print(x, get.resolution, convert_size(get.filesize_approx))