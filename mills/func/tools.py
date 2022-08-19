import asyncio
import json
import math
import re
import time
import aiofiles
import aiohttp
from telegraph import Telegraph
import urllib3

from mills import client, db
from mills.utils.logger import log


async def web_search(
    link:str = None,
    data: str = None,
    json: dict = None,
    params: dict = None,
    headers: dict = None,
    post:bool =  False,
    r_json: bool = False,
    r_content: bool = False,
    r_real: bool = False,
    **kwargs
):
    """
    Search for a link on web
    """
    if not headers:
        headers = {}

    if json:
        headers.update({"Content-Type": "application/json"})
    if data:
        headers.update({"Content-Type": "application/x-www-form-urlencoded"})
    async with aiohttp.ClientSession(headers = headers) as session:
        if post or data or json:
            async with session.post(link, data=data, json=json,**kwargs) as resp:
                if r_json:
                    return await resp.json()
                if r_content:
                    return await resp.read()
                if r_real:
                    return resp
                return await resp.text()
        else:
            async with session.get(link, params=params, **kwargs) as resp:
                if r_json:
                    return await resp.json()
                if r_content:
                    return await resp.read()
                if r_real:
                    return resp
                return await resp.text()

async def download_file(link, name):
    """for files, without progress callback with aiohttp"""
    if not aiohttp:
        urllib3.request.urlretrieve(link, name)
        return name
    async with aiohttp.ClientSession() as ses:
        async with ses.get(link) as re_ses:
            file = await aiofiles.open(name, "wb")
            await file.write(await re_ses.read())
            await file.close()
    return name

def cmd_regex_replace(cmd):
    cmd = str(cmd)
    return (
        cmd.replace("$", "")
        .replace("?(.*)", "")
        .replace("(.*)", "")
        .replace("(?: |)", "")
        .replace("| ", "")
        .replace("( |)", "")
        .replace("?((.|//)*)", "")
        .replace("?P<shortname>\\w+", "")
        .replace("(", "")
        .replace(")", "")
        .replace("?(\\d+)", "")
        .replace("|@roldexeversepybot|$", "")
        .replace("|@roldexeversepybot|", "")
        .replace(" - Admins Only", "").strip()
    )


import re
 
# Function to validate URL
# using regular expression
def isValidURL(str):

    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
    p = re.compile(regex)

    if (str == None):
        return False
    
    if(re.search(p, str)):
        return True
    else:
        return False



def convert_size(size_bytes):
    if size_bytes == 0:
       return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])



def time_formatter(milliseconds):
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s") if seconds else "")
    )
    if not tmp:
        return "0 s"

    if tmp.endswith(":"):
        return tmp[:-1]
    return tmp



def create_telegraph():
    key = db.get_key("TELEGRAPH_KEY") or None
    if key:
        telegraph_client = Telegraph(key)
        return telegraph_client
    full_name = client.name
    short_name = full_name[:20]
    profile_url = f"https://t.me/{client.me.username}"
    try:
        telegraph_client = Telegraph()
        telegraph_client.create_account(short_name = short_name,  author_url = profile_url, author_name = full_name)
    except Exception as er:
        if "SHORT_NAME_TOO_LONG" in str(er):
            telegraph_client.create_account(short_name = "Millie",  author_url = profile_url, author_name = full_name)
        else:
            log.exception(er)
            return
        return telegraph_client
    else:
        db.set_key("TELEGRAPH_KEY", telegraph_client.get_access_token())
        return telegraph_client
    



def json_parser(data, indent=None):
    parsed = {}
    try:
        if isinstance(data, str):
            parsed = json.loads(str(data))
            if indent:
                parsed = json.dumps(json.loads(str(data)), indent=indent)
        elif isinstance(data, dict):
            parsed = data
            if indent:
                parsed = json.dumps(data, indent=indent)
    except json.JSONDecodeError:
        parsed = eval(data)
    return parsed





def humanbytes(size):
    if not size:
        return "0 B"
    for unit in ["", "K", "M", "G", "T"]:
        if size < 1024:
            break
        size /= 1024
    if isinstance(size, int):
        size = f"{size}{unit}B"
    elif isinstance(size, float):
        size = f"{size:.2f}{unit}B"
    return size


def humanbytes(size):
    if not size:
        return "0 B"
    for unit in ["", "K", "M", "G", "T"]:
        if size < 1024:
            break
        size /= 1024
    if isinstance(size, int):
        size = f"{size}{unit}B"
    elif isinstance(size, float):
        size = f"{size:.2f}{unit}B"
    return size



def numerize(number):
    if not number:
        return None
    for unit in ["", "K", "M", "B", "T"]:
        if number < 1000:
            break
        number /= 1000
    if isinstance(number, int):
        number = f"{number}{unit}"
    elif isinstance(number, float):
        number = f"{number:.2f}{unit}"
    return number
