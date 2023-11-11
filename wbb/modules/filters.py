"""
MIT License

Copyright (c) 2023 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import re

from pyrogram import filters

from wbb import app
from wbb.core.decorators.errors import capture_err
from wbb.core.decorators.permissions import adminsOnly
from wbb.core.keyboard import ikb
from wbb.utils.dbfunctions import (
    delete_filter,
    get_filter,
    get_filters_names,
    save_filter,
)
from wbb.utils.filter_groups import chat_filters_group
from wbb.utils.functions import extract_text_and_keyb
from wbb.modules.notes import extract_urls

__MODULE__ = "Filters"
__HELP__ = """/filters To Get All The Filters In The Chat.
/filter [FILTER_NAME] To Save A Filter(reply to a message).

Supported filter types are Text, Animation, Photo, Document, Video, video notes, Audio, Voice

To use more words in a filter use.
`/filter Hey_there` To filter "Hey there"

/stop [FILTER_NAME] To Stop A Filter.


You can use markdown or html to save text too.

Checkout /markdownhelp to know more about formattings and other syntax.
"""


@app.on_message(filters.command("filter") & ~filters.private)
@adminsOnly("can_change_info")
async def save_filters(_, message):
    if len(message.command) < 2 or not message.reply_to_message:
        return await message.reply_text(
            "**Usage:**\nReply to a message with /filter [FILTER_NAME] To set a new filter."
        )    
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text("**Usage:**\n__/filter [FILTER_NAME]__")    
    chat_id = message.chat.id
    replied_message = message.reply_to_message
    text = name.split(" ", 1)    
    if len(text) > 1:
        name = text[0]
        data = text[1].strip()
        if replied_message.sticker or replied_message.video_note:
            data = None
    else:
        if replied_message.sticker or replied_message.video_note:
            data = None
        elif not replied_message.text and not replied_message.caption:
            data = None
        else:
            data = replied_message.text.markdown if replied_message.text else replied_message.caption.markdown
    if replied_message.text:
        _type = "text"
        file_id = None
    if replied_message.sticker:
        _type = "sticker"
        file_id = replied_message.sticker.file_id
    if replied_message.animation:
        _type = "animation"
        file_id = replied_message.animation.file_id
    if replied_message.photo:
        _type = "photo"
        file_id = replied_message.photo.file_id
    if replied_message.document:
        _type = "document"
        file_id = replied_message.document.file_id
    if replied_message.video:
        _type = "video"
        file_id = replied_message.video.file_id
    if replied_message.video_note:
        _type = "video_note"
        file_id = replied_message.video_note.file_id
    if replied_message.audio:
        _type = "audio"
        file_id = replied_message.audio.file_id
    if replied_message.voice:
        _type = "voice"
        file_id = replied_message.voice.file_id    
    if replied_message.reply_markup and not "~" in data:
        urls = extract_urls(replied_message.reply_markup)
        if urls:
            response = "\n".join([f"{name}=[{text}, {url}]" for name, text, url in urls])
            data = data + response
    name = name.replace("_", " ")
    _filter = {
        "type": _type,
        "data": data,
        "file_id": file_id,
    }
    await save_filter(chat_id, name, _filter)
    return await message.reply_text(f"__**Saved filter {name}.**__")


@app.on_message(filters.command("filters") & ~filters.private)
@capture_err
async def get_filterss(_, message):
    _filters = await get_filters_names(message.chat.id)
    if not _filters:
        return await message.reply_text("**No filters in this chat.**")
    _filters.sort()
    msg = f"List of filters in {message.chat.title} :\n"
    for _filter in _filters:
        msg += f"**-** `{_filter}`\n"
    await message.reply_text(msg)


@app.on_message(filters.command("stop") & ~filters.private)
@adminsOnly("can_change_info")
async def del_filter(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Usage:**\n__/stop [FILTER_NAME]__")
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text("**Usage:**\n__/stop [FILTER_NAME]__")
    chat_id = message.chat.id
    deleted = await delete_filter(chat_id, name)
    if deleted:
        await message.reply_text(f"**Deleted filter {name}.**")
    else:
        await message.reply_text("**No such filter.**")


@app.on_message(
    filters.text & ~filters.private & ~filters.via_bot & ~filters.forwarded,
    group=chat_filters_group,
)
@capture_err
async def filters_re(_, message):
    text = message.text.lower().strip()
    if not text:
        return
    chat_id = message.chat.id
    list_of_filters = await get_filters_names(chat_id)
    for word in list_of_filters:
        pattern = r"( |^|[^\w])" + re.escape(word) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            _filter = await get_filter(chat_id, word)
            data_type = _filter["type"]
            data = _filter["data"]
            file_id = _filter["file_id"]
            keyb = None
            if data:
                if re.findall(r"\[.+\,.+\]", data):
                    keyboard = extract_text_and_keyb(ikb, data)
                    if keyboard:
                        data, keyb = keyboard
            replied_message = message.reply_to_message
            if replied_message:
                if text.startswith("~"):
                    await message.delete()
                if replied_message.from_user.id != message.from_user.id:
                    message = replied_message

            if data_type == "text":
                await message.reply_text(
                    text=data,
                    reply_markup=keyb,
                    disable_web_page_preview=True,
                )
            if data_type == "sticker":
                await message.reply_sticker(
                    sticker=file_id,
                )
            if data_type == "animation":
                await message.reply_animation(
                    animation=file_id,
                    caption=data,
                    reply_markup=keyb,
                )
            if data_type == "photo":
                await message.reply_photo(
                    photo=file_id,
                    caption=data,
                    reply_markup=keyb,
                )
            if data_type == "document":
                await message.reply_document(
                    document=file_id,
                    caption=data,
                    reply_markup=keyb,
                )
            if data_type == "video":
                await message.reply_video(
                    video=file_id,
                    caption=data,
                    reply_markup=keyb,
                )
            if data_type == "video_note":
                await message.reply_video_note(
                    video_note=file_id,
                )
            if data_type == "audio":
                await message.reply_audio(
                    audio=file_id,
                    caption=data,
                    reply_markup=keyb,
                )
            if data_type == "voice":
                await message.reply_voice(
                    voice=file_id,
                    caption=data,
                    reply_markup=keyb,
                )
