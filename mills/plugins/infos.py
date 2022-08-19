"""
≛ <b>Commands Available</b> ≛

- <code>/ip</code> ipAddress : Get info about that IP address.
──────────────────────
- <code>/phone <phonenumber></code>: Get phone number information with + and country code.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import inspect
import io
import json
import os
import time
import requests
from telethon import utils
# from telethon import Button
from telethon.tl.custom import Button



from mills.decorators import bot_cmd
from ._helpers.strings  import get_strings



@bot_cmd(cmd="ip")
async def ip(m):
    ip = m.pattern_match.group(1).strip()
    if ip:
        info = requests.get(f"http://ip-api.com/json/{ip}")
        info_json = info.json()
        if info_json['status'] != 'success':
            await m.reply("Invalid ip.")
            return
        else:
            text = "IP Info\n"
            for x in info_json:
                text += f"{x.title()}: {info_json[x]}\n"
            await m.sod(text)
    else:
        await m.sod("Give me IP address.", time = 5)
    return


@bot_cmd(cmd="phone")
async def phone(m):
    phone = m.pattern_match.group(1).strip()
    print(phone)
    if not phone or not phone.startswith('+') or len(phone) < 10:
        await m.sod("invalid Phone Number")
        return
    key = "fe65b94e78fc2e3234c1c6ed1b771abd"
    api = (
        "http://apilayer.net/api/validate?access_key="
        + key
        + "&number="
        + phone
        + "&country_code=&format=1"
    )
    output = requests.get(api)
    data = output.json()
    text = "Phone Number Information\n"
    for x in data:
        text += str(x.replace('_',' ').title()) + " : " + str(data[x]) + "\n"
    return await m.sod(text)



@bot_cmd(cmd="zip")
async def zip(m):
    zip = m.pattern_match.group(1).strip()
    if not zip or not zip.isdigit():
        await m.sod("invalid postal Code", time = 5)
        return
    output = requests.get('https://api.zippopotam.us/US/{}'.format(zip))
    if not output:
        await m.sod("invalid postal Code", time = 5)
    dic = output.json()
    new = "Zip Information\n"
    
    for a in dic:
        if isinstance(dic[a], dict):
            for x in dic[a]:
                new += f"{dd.title()}: {y[dd]}\n"
        elif isinstance(dic[a], list):        
            for y in dic[a]:
                if isinstance(y, dict):
                    for dd in y:
                        new += f"{dd.title()}: {y[dd]}\n"
                elif isinstance(y, list):
                    for z in y:
                        if isinstance(z, dict):
                            for dd in z:
                                new += f"{dd.title()}: {z[dd]}\n"
                        else:
                            new += f"{z}\n"
                else:
                    new += f"{y.title()}: {y.items()}\n"
        else:
            new += f"{a.title()}: {dic[a]}\n"
    return await m.sod(new)

