from io import BytesIO
from random import shuffle
import aiohttp
import bs4
import markdown
from telethon import Button
from mills import client, db
from mills.func.tools import cmd_regex_replace, web_search
from mills.utils.logger import log
from telegraph import Telegraph
import urllib.parse

from .. import LIST, MOD_HELP, Telegraph_client


def find_between( data, first, last ):
    try:
        start = data.index( first ) + len( first )
        end = data.index( last, start )
        return data[start:end]
    except ValueError:
        return None





async def make_cmds(m):
    text = ""
    for l in LIST.keys():
        text += f"Plugin Name: {l.title()}\n\n<br>"
        for zz in LIST[l]:
            _ = cmd_regex_replace(zz).strip()
            md = markdown.markdown('/' + _)
            text += "\n" + md + "\n"
        text += "\n\n"
    t = Telegraph_client.create_page(html_content = text, title = 'Commands Of Millie')
    await m.sod(f"All Millie Cmds: [Click Here]({t['url']})")



def short_list(list, index):
    sorted_list = []
    while list:
        sorted_list.extend([list[:index]])
        list = list[index:]
    return sorted_list


def make_buttons(index, key):
    loaded = MOD_HELP.get(key, [])
    cmds = [
        Button.inline(x, data = f"{key}_{x}_{index}")
        for x in sorted(loaded)
    ]
    
    rows = short_list(cmds, 3)
    cols = short_list(rows, 4)
    try:
        buttons = cols[int(index)]
        index = int(index)
    except:
        buttons = cols[0] if cols else []
        index = 0
    if index == 0  and len(cols) == 1:
        if key in ["plugins", "checkers"]:
            data = f"make_cmd_again_{key}"
        else:
            data = f"cmds_{key}_{index}"
        buttons.append(
            [
                Button.inline("☒", data="close"),
                Button.inline('Back', data)
            ]
            )
        # buttons.append([Button.inline("« Bᴀᴄᴋ »", data="open")])
    else:
        buttons.append(
            [
                Button.inline(
                    "❮",
                    data=f"help_{key}_{index-1}",
                ),
                Button.inline("☒", data="close"),
                Button.inline(
                    "❯",
                    data=f"help_{key}_{index+1}",
                ),
            ]
        )
    return buttons


def make_buttons_checkers():
    butt = [
            Button.inline(" Auth ", data = f"auth"),
            Button.inline(" Charge ", data = f"charge"),
            Button.inline(" Others ", data = f"other"),
            Button.inline(" Mass ", data = f"mass"),
            Button.inline(" Tools ", data = f"tools"),
        ]
    rows = short_list(butt, 3)
    cols = short_list(rows, 4)
    buttons =  cols[0] if cols else []
    buttons.append([Button.inline("« Back", data="main")])
    return buttons



def count_keys(dict_, counter=0):
    for each_key in dict_:
        if isinstance(dict_[each_key], dict):
            counter = count_keys(dict_[each_key], counter + 1)
        else:
            counter += 1
    return counter




def mediainfo(media):
    xx = str((str(media)).split("(", maxsplit=1)[0])
    m = ""
    if xx == "MessageMediaDocument":
        mim = media.document.mime_type
        if mim == "application/x-tgsticker":
            m = "sticker animated"
        elif "image" in mim:
            if mim == "image/webp":
                m = "sticker"
            elif mim == "image/gif":
                m = "gif as doc"
            else:
                m = "pic as doc"
        elif "video" in mim:
            if "DocumentAttributeAnimated" in str(media):
                m = "gif"
            elif "DocumentAttributeVideo" in str(media):
                i = str(media.document.attributes[0])
                if "supports_streaming=True" in i:
                    m = "video"
                m = "video as doc"
            else:
                m = "video"
        elif "audio" in mim:
            m = "audio"
        else:
            m = "document"
    elif xx == "MessageMediaPhoto":
        m = "pic"
    elif xx == "MessageMediaWebPage":
        m = "web"
    return m




async def Carbon1(code: str = None, bgcolour: str = 'rgba(120, 19, 254, 100)'):
    async with aiohttp.ClientSession() as client:
        url = f'https://carbonara-42.herokuapp.com/api/cook'
        code = urllib.parse.quote(code)
        params = {
'code': code,
'theme': 'nord',
# 'backgroundColor': bgcolour,
'dropShadow':True,
'dropShadowBlurRadius': '50px',
'dropShadowOffsetY': '25px',
'fontFamily': 'hack',
'widthAdjustment':True,
'windowControls':False,
'windowTheme': "none",
        }

        _ = await client.post(url, json = params)
        data =  await _.read()
        with open('images/Mille_Rusk.jpg', 'wb') as wr:
            wr.write(data)
        return 'images/Mille_Rusk.jpg'





async def unsplashsearch(query, limit=None, shuf=True):
    query = query.replace(" ", "-")
    link = "https://unsplash.com/s/photos/" + query
    extra = await web_search(link, r_content=True)
    if not extra: return 
    res = bs4.BeautifulSoup(extra, "html.parser", from_encoding="utf-8")
    all_ = res.find_all("img", "YVj9w")
    if len(all_) == 0: return
    if shuf:
        shuffle(all_)
    all_ = all_[:limit]
    return [image["src"] for image in all_]
