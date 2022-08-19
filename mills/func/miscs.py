
import base64
from mills.utils.logger import log
import os
import random
import re
import string
from logging import WARNING
from random import choice, randrange, shuffle
from traceback import format_exc


try:
    from aiohttp import ContentTypeError
except ImportError:
    ContentTypeError = None

from telethon.tl import types
from telethon.utils import get_display_name, get_peer_id

from . import some_random_headers
from .tools import web_search, check_filename, json_parser

try:
    import aiofiles
    import aiohttp
except ImportError:
    aiohttp = None
    aiofiles = None


try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import cv2
except ImportError:
    cv2 = None
try:
    import numpy as np
except ImportError:
    np = None


from bs4 import BeautifulSoup



async def google_search(query):
    query = query.replace(" ", "+")
    _base = "https://google.com"
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "User-Agent": choice(some_random_headers),
    }
    con = await web_search(_base + "/search?q=" + query, headers=headers)
    soup = BeautifulSoup(con, "html.parser")
    result = []
    pdata = soup.find_all("a", href=re.compile("url="))
    for data in pdata:
        if not data.find("div"):
            continue
        try:
            result.append(
                {
                    "title": data.find("div").text,
                    "link": data["href"].split("&url=")[1].split("&ved=")[0],
                    "description": data.find_all("div")[-1].text,
                }
            )
        except BaseException as er:
            log.exception(er)
    return result

