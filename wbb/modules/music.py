from __future__ import unicode_literals
from urllib.parse import urlparse
import os
import youtube_dl
import aiohttp
import aiofiles
import os
from random import randint
from pyrogram import filters
from pyrogram.types import Message
from wbb import app, OWNER_ID, SUDO_USER_ID, 
from wbb.utils.fetch import fetch
from wbb.utils.errors import capture_err


SUDOERS = [OWNER_ID, SUDO_USER_ID]

__MODULE__ = "Music"
__HELP__ = "/ytmusic [link] To Download Music From Various Websites Including Youtube"

ydl_opts = {
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }]
}


# Ytmusic

@app.on_message(filters.command("ytmusic") & ~filters.edited & filters.user(SUDOERS))
@capture_err
async def music(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text("`/music` needs a link as argument")
        return
    link = message.text.split(None, 1)[1]
    m = await message.reply_text(f"Downloading {link}",
                                 disable_web_page_preview=True)
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
            # .webm -> .weba
            basename = audio_file.rsplit(".", 1)[-2]
            thumbnail_url = info_dict['thumbnail']
            thumbnail_file = basename + "." + get_file_extension_from_url(thumbnail_url)
            audio_file = basename + ".mp3"
    except Exception as e:
        await m.edit(str(e))
        return
        # info
    title = info_dict['title']
    webpage_url = info_dict['webpage_url']
    performer = info_dict['uploader']
    duration = int(float(info_dict['duration']))
    caption = f"[{title}]({webpage_url})"
    await m.delete()
    await message.reply_chat_action("upload_document")
    await message.reply_audio(audio_file, caption=caption,
                              duration=duration, performer=performer,
                              title=title, thumb=thumbnail_file)
    os.remove(audio_file)
    os.remove(thumbnail_file)


def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


# Funtion To Download Song
@capture_err
async def download_song(url):
    song_name = f"{randint(6969, 6999)}.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(song_name, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return song_name


# Jiosaavn Music


@app.on_message(filters.command("song"))
@capture_err
async def jssong(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text("/song requires an argument.")
        return
    text = message.text.split(None, 1)[1]
    query = text.replace(" ", "%20")
    m = await message.reply_text("Searching...")
    try:
        r = await fetch(f"{JSMAPI}{query}")
    except Exception as e:
        await m.edit(str(e))
        return
    sname = r.json()[0]['song']
    slink = r.json()[0]['media_url']
    ssingers = r.json()[0]['singers']
    song = await download_song(slink)
    await message.reply_audio(audio=ffile, title=sname,
                              performer=ssingers)
    os.remove(song)
    await m.delete()
