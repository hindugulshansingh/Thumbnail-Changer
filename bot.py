import os
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN

os.makedirs("downloads", exist_ok=True)

app = Client("thumb-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("👋 Welcome! Send a photo to set thumbnail.\nUse /setthumb, /getthumb, /delthumb.")

@app.on_message(filters.command("setthumb") & filters.photo)
async def set_thumb(client, message: Message):
    user_id = str(message.from_user.id)
    path = f"downloads/{user_id}.jpg"
    await message.download(path)
    await message.reply("✅ Thumbnail saved!")

@app.on_message(filters.command("getthumb"))
async def get_thumb(client, message: Message):
    user_id = str(message.from_user.id)
    path = f"downloads/{user_id}.jpg"
    if os.path.exists(path):
        await message.reply_photo(path)
    else:
        await message.reply("❌ No thumbnail found.")

@app.on_message(filters.command("delthumb"))
async def del_thumb(client, message: Message):
    user_id = str(message.from_user.id)
    path = f"downloads/{user_id}.jpg"
    if os.path.exists(path):
        os.remove(path)
        await message.reply("🗑️ Thumbnail deleted.")
    else:
        await message.reply("❌ No thumbnail to delete.")

@app.on_message(filters.video | filters.document)
async def process_media(client, message: Message):
    user_id = str(message.from_user.id)
    thumb_path = f"downloads/{user_id}.jpg"
    if os.path.exists(thumb_path):
        await message.reply_document(
            document=message.document or message.video,
            thumb=thumb_path,
            caption="✅ Sent with custom thumbnail"
        )
    else:
        await message.reply("⚠️ No custom thumbnail set. Use /setthumb with a photo.")

app.run()
