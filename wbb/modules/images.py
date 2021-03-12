import urllib.request
import json
import asyncio
from random import randint
from pyrogram import filters
from pyrogram.types import Message
from wbb.utils import cust_filter
from wbb import app, ARQ
from wbb.utils.errors import capture_err
from wbb.utils.fetch import fetch


__MODULE__ = "Images"
__HELP__ = '''/cat  - Get Cute Cats Images
/wall - Get Wallpapers'''


async def delete_message_with_delay(delay, message: Message):
    await asyncio.sleep(delay)
    await message.delete()


@app.on_message(filters.command("cat") & ~filters.edited)
@capture_err
async def cat(_, message):
    with urllib.request.urlopen(
            "https://api.thecatapi.com/v1/images/search"
    ) as url:
        data = json.loads(url.read().decode())
    cat_url = (data[0]['url'])
    await message.reply_photo(cat_url)


@app.on_message(filters.command("wall") & ~filters.edited)
@capture_err
async def wall(_, message):
    if len(message.command) < 2:
        await message.reply_text("/wall needs an argument")
        return
    initial_term = message.text.split(None, 1)[1]
    m = await message.reply_text("Searching!")
    term = initial_term.replace(' ', '%20')
    json_rep = await fetch(f"{ARQ}wall?query={term}")
    if not json_rep.get("success"):
        await m.edit("Something happened! Shit.")
    else:
        wallpapers = json_rep.get("wallpapers")
        if not wallpapers:
            await m.edit("Found literally nothing!,"
                         + "You should work on your English.")
            return
        if len(wallpapers) > 10:
            selection = 10
        else:
            selection = len(wallpapers)
        index = randint(0, selection - 1)
        wallpaper = wallpapers[index]
        wallpaper = wallpaper.get("url_image")
        wallpaper = wallpaper.replace("\\", "")
        await message.reply_document(wallpaper)
        await m.delete()
