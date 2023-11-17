import os
import re
from pyrogram.errors import MessageNotModified

def get_new_file_name(old_file_path, chat_id, user_names, user_seasons):
    user_name = user_names.get(chat_id, "Unknown")
    season = user_seasons.get(chat_id, "S1")

    file_name = os.path.basename(old_file_path)
    episode_match = re.search(r"(\d{2})", file_name)
    quality_match = re.search(r"(360p|480p|720p|1080p)", file_name)

    episode_number = episode_match.group(1) if episode_match else "00"
    quality = quality_match.group(1).replace('360p', '480p') if quality_match else "Unknown"

    new_file_name = f"[TAL] [{season}-EP{episode_number}] {user_name} [{quality}]{os.path.splitext(file_name)[-1]}"
    return os.path.join(os.path.dirname(old_file_path), new_file_name)

async def download_file(client, message, downloaded_path, progress_message, media):
    if media:
        await client.download_media(message, file_name=downloaded_path, progress=download_progress_callback(progress_message))

async def upload_file(client, chat_id, new_file_path, progress_message, thumbnail_file_id=None):
    try:
        file_name = os.path.basename(new_file_path)

        if thumbnail_file_id:
            thumbnail_path = await client.download_media(thumbnail_file_id)
            media = await client.send_document(
                chat_id,
                new_file_path,
                caption=file_name,
                progress=upload_progress_callback(progress_message),
                thumb=thumbnail_path
            )
            os.remove(thumbnail_path)
        else:
            media = await client.send_document(
                chat_id,
                new_file_path,
                caption=file_name,
                progress=upload_progress_callback(progress_message),
            )

        return media
    except MessageNotModified:
        return None

def download_progress_callback(progress_message):
    async def callback(current, total):
        await progress_message.edit_text(f"Download progress: {current * 100 / total:.1f}%")
    return callback

def upload_progress_callback(progress_message):
    async def callback(current, total):
        await progress_message.edit_text(f"Upload progress: {current * 100 / total:.1f}%")
    return callback
