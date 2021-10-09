from pyrogram import filters
from pyrogram.types import Message

from bot import app, dispatcher
from telegram.ext import CommandHandler



@app.on_message(filters.command("webss"))
async def take_ss(_, message: Message):
    try:
        if len(message.command) != 2:
            return await message.reply_text("Give A Url To Fetch Screenshot.")
        url = message.text.split(None, 1)[1]
        m = await message.reply_text("**Mengambil Screenshot**")
        await m.edit("**Mengupload**")
        try:
            await message.reply_photo(
                photo=f"https://webshot.amanoteam.com/print?q={url}",
                quote=False,
            )
        except TypeError:
            return await m.edit("No Such Website.")
        await m.delete()
    except Exception as e:
        await message.reply_text(str(e))


WEBSS_HANDLER = CommandHandler("webss", take_ss)

dispatcher.add_handler(WEBSS_HANDLER)
