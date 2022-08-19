"""
≛ <b>Commands Available</b> ≛
──────────────────────
- <code>/carbon</code>: Carbinize the text and gives you a image.
──────────────────────
- <code>/uploadimg</code>: Upload a image to Telegraph server.
──────────────────────
- <code>/gblur</code>: Gaussian blur the image.
──────────────────────
- <code>/mblur</code>: Median blur the image.
──────────────────────
- <code>/detectedge</code>: Detect Edges of the image.
──────────────────────
- <code>/centroid</code>: Centroid (Center of blob) detection of the image.**
──────────────────────
- <code>/blackandwhite</code>: Convert image to grayscale (Black & White).
──────────────────────
- <code>/imagetotext</code>: Extracting text from Image.
──────────────────────
- <code>/rednoise</code>: Reduce noise from Image.
──────────────────────
- <code>/rmbg</code>: Remove Background from Image.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""
import asyncio
import inspect
import io
import os
from random import shuffle

import numpy as np

import pytesseract
from ._helpers.tools import Carbon1
import qrcode
import cv2
from PIL import Image
from telethon.tl.types import MessageMediaDocument as doc
from telethon.tl.types import MessageMediaPhoto as photu
from telegraph import upload_file

from mills.decorators import bot_cmd
from mills.func.tools import download_file, web_search
from mills import client


@bot_cmd(cmd="carbon", text_only = True)
async def carbon(m):
    query = m.text.split(maxsplit=1)
    if query and len(query) == 1 or not query: return await m.sod("give me a text. \n Usage:  <code>/carbon print('Millie Rusk')</code")
    res = await Carbon1(query[1])
    await m.reply(file = res, supports_streaming=True)
    if os.path.exists(res):
        os.remove(res)



@bot_cmd(cmd="uploadimg")
async def uploadimg(m):
    r = await m.get_reply_message()
    if not (r and r.media):
        return await m.sod("`Reply to Image`", time=5)
    if isinstance(r.media, photu):
        dl = await r.download_media()
    elif isinstance(r.media, doc):
        dl = await r.download_media(thumb=-1)
    else:
        return await m.sod("Where is Image?", time=5)
    try:
        link = upload_file(dl)
    except:
        return await m.sod("error while doing this. make sure you give a image file.")
    if not link:
        return await m.sod("error while doing this. make sure you give a image file.")
    await m.sod("Your image online link: {}".format('https://telegra.ph/' + link[0]))
    os.unlink(dl)
    


@bot_cmd(cmd="gblur")
async def gblur(m):
    r = await m.get_reply_message()
    if not (r and r.media):
        return await m.sod("`Reply to Media`", time=5)
    if isinstance(r.media, photu):
        dl = await r.download_media()
    elif isinstance(r.media, doc):
        dl = await r.download_media(thumb=-1)
    else:
        return await m.sod("Where is Image?", time=5)
    img = cv2.imread(dl)
    blur_image = cv2.GaussianBlur(img, (7,7), 0)
    cv2.imwrite(f'images/gblur_{str(m.sender_id)}.jpg', blur_image)
    if os.path.exists(f'images/gblur_{str(m.sender_id)}.jpg'):
        await m.sod(file = f'images/gblur_{str(m.sender_id)}.jpg', supports_streaming = True)
        os.remove(f'images/gblur_{str(m.sender_id)}.jpg')
        os.remove(dl)
    else:
        await m.sod("Sorry i have some issues. i cant blur this image", time=5)
        return



@bot_cmd(cmd="mblur")
async def mblur(m):
    r = await m.get_reply_message()
    if not (r and r.media):
        return await m.sod("`Reply to Media`", time=5)
    if isinstance(r.media, photu):
        dl = await r.download_media()
    elif isinstance(r.media, doc):
        dl = await r.download_media(thumb=-1)
    else:
        return await m.sod("Where is Image?", time=5)
    img = cv2.imread(dl)
    blur_image = cv2.medianBlur(img, 5)
    cv2.imwrite(f'images/mblur_{str(m.sender_id)}.jpg', blur_image)
    if os.path.exists(f'images/mblur_{str(m.sender_id)}.jpg'):
        await m.sod(file = f'images/mblur_{str(m.sender_id)}.jpg', supports_streaming = True)
        os.remove(f'images/mblur_{str(m.sender_id)}.jpg')
        os.remove(dl)
    else:
        await m.sod("Sorry i have some issues. i cant blur this image", time=5)
        return


@bot_cmd(cmd="detectedge")
async def detectedge(m):
    r = await m.get_reply_message()
    if not (r and r.media):
        return await m.sod("`Reply to Media`", time=5)
    if isinstance(r.media, photu):
        dl = await r.download_media()
    elif isinstance(r.media, doc):
        dl = await r.download_media(thumb=-1)
    else:
        return await m.sod("Where is Image?", time=5)
    img = cv2.imread(dl)
    blur_image = cv2.Canny(img, 100,200)
    cv2.imwrite(f'images/detected_{str(m.sender_id)}.jpg', blur_image)
    if os.path.exists(f'images/detected_{str(m.sender_id)}.jpg'):
        await m.sod(file = f'images/detected_{str(m.sender_id)}.jpg', supports_streaming = True)
        os.remove(f'images/detected_{str(m.sender_id)}.jpg')
        os.remove(dl)
    else:
        await m.sod("Sorry i have some issues. i cant blur this image", time=5)
        return




@bot_cmd(cmd="blackandwhite")
async def blackandwhite(m):
    r = await m.get_reply_message()
    if not (r and r.media):
        return await m.sod("`Reply to Media`", time=5)
    if isinstance(r.media, photu):
        dl = await r.download_media()
    elif isinstance(r.media, doc):
        dl = await r.download_media(thumb=-1)
    else:
        return await m.sod("Where is Image?", time=5)
    img = cv2.imread(dl)
    blur_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(f'images/gray_{str(m.sender_id)}.jpg', blur_image)
    if os.path.exists(f'images/gray_{str(m.sender_id)}.jpg'):
        await m.sod(file = f'images/gray_{str(m.sender_id)}.jpg', supports_streaming = True)
        os.remove(f'images/gray_{str(m.sender_id)}.jpg')
        os.remove(dl)
    else:
        await m.sod("Sorry i have some issues. i cant blur this image", time=5)


@bot_cmd(cmd="centroid")
async def centroid(m):
    r = await m.get_reply_message()
    if not (r and r.media):
        return await m.sod("`Reply to Media`", time=5)
    if isinstance(r.media, photu):
        dl = await r.download_media()
    elif isinstance(r.media, doc):
        dl = await r.download_media(thumb=-1)
    else:
        return await m.sod("Where is Image?", time=5)
    img = cv2.imread(dl)
    blur_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    moment = cv2.moments(blur_image)
    X = int(moment ["m10"] / moment["m00"])
    Y = int(moment ["m01"] / moment["m00"])
    cv2.circle(img, (X, Y), 15, (205, 114, 101), 1)
    cv2.imwrite(f'images/centroid{str(m.sender_id)}.jpg', blur_image)
    if os.path.exists(f'images/centroid{str(m.sender_id)}.jpg'):
        await m.sod(file = f'images/centroid{str(m.sender_id)}.jpg', supports_streaming = True)
        os.remove(f'images/centroid{str(m.sender_id)}.jpg')
        os.remove(dl)
    else:
        await m.sod("Sorry i have some issues. i cant blur this image", time=5)


@bot_cmd(cmd="rednoise")
async def rednoise(m):
    r = await m.get_reply_message()
    if not (r and r.media):
        return await m.sod("`Reply to Media`", time=5)
    if isinstance(r.media, photu):
        dl = await r.download_media()
    elif isinstance(r.media, doc):
        dl = await r.download_media(thumb=-1)
    else:
        return await m.sod("Where is Image?", time=5)
    img = cv2.imread(dl)
    result = cv2.fastNlMeansDenoisingColored(img,None,20,10,7,21)
    cv2.imwrite(f'images/reduced_noice_{str(m.sender_id)}.jpg', result)
    if os.path.exists(f'images/reduced_noice_{str(m.sender_id)}.jpg'):
        await m.sod(file = f'images/reduced_noice_{str(m.sender_id)}.jpg', supports_streaming = True)
        os.remove(f'images/reduced_noice_{str(m.sender_id)}.jpg')
        os.remove(dl)
    else:
        await m.sod("Sorry i have some issues. i cant blur this image", time=5)




@bot_cmd(cmd="rmbg")
async def rmbg(m):
    r = await m.get_reply_message()
    if not (r and r.media):
        return await m.sod("`Reply to Media`", time=5)
    if isinstance(r.media, photu):
        dl = await r.download_media()
    elif isinstance(r.media, doc):
        dl = await r.download_media(thumb=-1)
    else:
        return await m.sod("Where is Image?", time=5)
    img = cv2.imread(dl)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    img_contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    img_contours = sorted(img_contours, key=cv2.contourArea)
    for i in img_contours:
        if cv2.contourArea(i) > 100:
            break
    mask = np.zeros(img.shape[:2], np.uint8)
    cv2.drawContours(mask, [i],-1, 255, -1)
    new_img = cv2.bitwise_and(img, img, mask=mask)
    cv2.imwrite(f'images/rmbg_{str(m.sender_id)}.jpg', new_img)
    if os.path.exists(f'images/rmbg_{str(m.sender_id)}.jpg'):
        await m.sod(file = f'images/rmbg_{str(m.sender_id)}.jpg', supports_streaming = True)
        os.remove(f'images/rmbg_{str(m.sender_id)}.jpg')
        os.remove(dl)
    else:
        await m.sod("Sorry i have some issues. i cant blur this image", time=5)




@bot_cmd(cmd="imagetotext")
async def imagetotext(m):
    r = await m.get_reply_message()
    if not (r and r.media):
        return await m.sod("`Reply to Media`", time=5)
    if isinstance(r.media, photu):
        dl = await r.download_media()
    elif isinstance(r.media, doc):
        dl = await r.download_media(thumb=-1)
    else:
        return await m.sod("Where is Image?", time=5)
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    x = pytesseract.image_to_string(dl)
    if len(x) == ' ':
        return await m.sod("No text found in image", time=5)
    await m.sod(x)
    if os.path.exists(dl):
        os.remove(dl)
    else:
        await m.sod("Sorry i have some issues. i cant blur this image", time=5)


