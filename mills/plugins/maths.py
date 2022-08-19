"""
≛ <b>Commands Available</b> ≛
- <code>/simplify</code>- Math /math 2^2+2(2)
──────────────────────
- <code>/factor</code>- Factor /factor x^2 + 2x
──────────────────────
- <code>/derive</code>- Derive /derive x^2+2x
──────────────────────
- <code>/integrate</code>- Integrate /integrate x^2+2x
──────────────────────
- <code>/zeroes</code>- Find 0's /zeroes x^2+2x
──────────────────────
- <code>/tangent</code>- Find Tangent /tangent 2lx^
──────────────────────
- <code>/area</code>: Area Under Curve <code>/area 2:4lx^3<code>
──────────────────────
- <code>/cos</code>: Cosine /cos pi
──────────────────────
- <code>/sin</code>: Sine /sin 0
──────────────────────
- <code>/tan</code>: Tangent /tan 0
──────────────────────
- <code>/arccos</code>: Inverse Cosine /arccos 1
──────────────────────
- <code>/arcsin</code>: Inverse Sine /arcsin 0
──────────────────────
- <code>/arctan</code>: Inverse Tangent /arctan 0
──────────────────────
- <code>/abs</code>: Absolute Value /abs -1
──────────────────────
- <code>/log</code>: Logarithm /log 2l8
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import asyncio
import inspect
import io
import os
from random import shuffle
import requests
import validators
import qrcode
import cv2
import numpy as np
import pytesseract
from numerize import numerize
import math

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




@bot_cmd(cmd="simplify", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/simplify/{query}")
    obj = response.json()
    j = obj["result"]
    await m.sod(j)



@bot_cmd(cmd="factor", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/factor/{query}")
    obj = response.json()
    j = obj["result"]
    await m.sod(j)


@bot_cmd(cmd="factorize", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/factor/{query}")
    obj = response.json()
    j = obj["result"]
    await m.sod(j)




@bot_cmd(cmd="derive", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/derive/{query}")
    obj = response.json()
    j = obj["result"]
    await m.sod(j)



@bot_cmd(cmd="zeroes", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/zeroes/{query}")
    obj = response.json()
    j = obj["result"]
    await m.sod(j)



@bot_cmd(cmd="tangent", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/tangent/{query}")
    obj = response.json()
    j = obj["result"]
    await m.sod(j)


@bot_cmd(cmd="area", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/area/{query}")
    obj = response.json()
    j = obj["result"]
    await m.sod(j)


@bot_cmd(cmd="cos", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    await m.sod(str(math.cos(int(query))))


@bot_cmd(cmd="sin", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    await m.sod(str(math.sin(int(query))))

@bot_cmd(cmd="tan", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    await m.sod(str(math.tan(int(query))))

@bot_cmd(cmd="arccos", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    await m.sod(str(math.arccos(int(query))))

@bot_cmd(cmd="arcsin", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    await m.sod(str(math.arcsin(int(query))))

@bot_cmd(cmd="abs", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    await m.sod(str(math.abs(int(query))))

@bot_cmd(cmd="log", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    await m.sod(str(math.log(int(query))))

@bot_cmd(cmd="log", text_only = True)
async def webss(m):
    query = m.pattern_match.group(1)
    await m.sod(str(math.log(int(query))))
