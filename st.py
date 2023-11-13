import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Your Telegram bot token
TOKEN = "6594858799:AAH2Y3sa-7vbQaIYUM5WASndSosEc6qyutw"

# Set up the Updater
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define the start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me a file, and I will download it to my storage.')

# Define the file handler
def file_handler(update: Update, context: CallbackContext) -> None:
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    file.download('your_storage_path/' + update.message.document.file_name)
    update.message.reply_text('File downloaded successfully!')

# Add the handlers to the dispatcher
start_handler = CommandHandler('start', start)
file_handler = MessageHandler(Filters.document, file_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(file_handler)

# Start the Bot
updater.start_polling()
updater.idle()
          
