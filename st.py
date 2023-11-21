from pyrogram import Client, filters
from pyrogram.errors import MessageNotModified
import os
from utils import get_new_file_name, download_file, upload_file, download_progress_callback, upload_progress_callback

API_KEY = "6517750473:AAFvsuuwixB_r_7ORYJxv6eBY8ZZ1v_pGe4"

app = Client("my_bot", api_id=28490129, api_hash="f244f8b975d989f818cefd27a38d771c", bot_token=API_KEY)
user_names = {}
user_thumbnails = {}
user_seasons = {}
progress_messages = {}


async def delete_progress_messages(progress_message):
    # Delete progress message
    if progress_message:
        await progress_message.delete()

@app.on_message(filters.command("start"))
async def start_command(_, message):
    await message.reply_text('✨ Hello!\n⚙️ Welcome To Auto Rename Bot.\n🔗 Heres All Command\n\n🛠️ /setname - <b>To Save Anime Names</b>\n🛠️ /setseason - <b>To Save Anime Season</b>')
@app.on_message(filters.command("setname"))
async def set_name_command(_, message):
    chat_id = message.chat.id
    await message.reply_text("Please send your name.")
    user_names[chat_id] = None 

@app.on_message(filters.command("setseason"))
async def set_season_command(_, message):
    chat_id = message.chat.id
    await message.reply_text("Please send your season.")
    user_seasons[chat_id] = None
    
@app.on_message(filters.create(lambda _, __, message: message.text and not message.text.startswith("/")))
async def handle_text(_, message):
    chat_id = message.chat.id
    text = message.text.strip()

    
    if chat_id in user_seasons and user_seasons[chat_id] is None:
        user_seasons[chat_id] = text.upper()
        await message.reply_text(f"Your season has been set to {text.upper()}.")
    elif chat_id in user_names and user_names[chat_id] is None:
        user_names[chat_id] = text
        await message.reply_text("Name has been set.")

@app.on_message(filters.private & filters.photo)
async def set_thumbnail_command(_, message):
    chat_id = message.chat.id
    thumbnail_file_id = message.photo.file_id

    user_thumbnails[chat_id] = thumbnail_file_id

    await message.reply_text("Your thumbnail has been saved.")

@app.on_message(filters.document)
async def file_handler(_, message):
    file_path = message.document.file_name
    storage_path = "./down/"
    downloaded_path = f'{storage_path}{file_path}'

    thumbnail_file_id = user_thumbnails.get(message.chat.id)


    download_progress_message = await message.reply_text("Download progress: 0.0%")

    if message.document:
        media = message.document

        await download_file(app, message, downloaded_path, download_progress_message, media)

        new_file_path = get_new_file_name(downloaded_path, message.chat.id, user_names, user_seasons)

        os.rename(downloaded_path, new_file_path)

        print(f"Processing file: {new_file_path}")

        upload_progress_message = await message.reply_text("Upload progress: 0.0%")

        uploaded_media = await upload_file(app, message.chat.id, new_file_path, upload_progress_message, thumbnail_file_id)


        await upload_progress_message.edit_text(f"Upload complete!")

        os.remove(new_file_path)

       
        await delete_progress_messages(download_progress_message)

if __name__ == "__main__":
    app.run()
