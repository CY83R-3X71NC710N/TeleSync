# Python script to download files uploaded to telegram if in parts or indvidually. (We could do this by creating a channel specifically for the upload and then in this script downloading everything in that channel)
import os
import telegram
from telegram.ext import Updater, CommandHandler

# Prompt the user to enter the bot token, channel ID, and download directory
TOKEN = input('Enter your bot token: ')
CHANNEL_ID = input('Enter the channel ID: ')
DOWNLOAD_DIR = input('Enter the download directory: ')

# Create the Telegram bot object
bot = telegram.Bot(token=TOKEN)

# Define the function to download the files
def download_files(update, context):
    chat_id = update.message.chat_id
    # Get a list of all the files in the channel
    file_list = bot.get_chat_history(chat_id=CHANNEL_ID, limit=999999, filter='document')
    # Loop over the files in the list and download each one
    for file_obj in file_list:
        file_id = file_obj.document.file_id
        file_name = file_obj.document.file_name
        file_path = os.path.join(DOWNLOAD_DIR, file_name)
        try:
            # Download the file
            bot.get_file(file_id).download(custom_path=file_path)
        except Exception as e:
            # Handle errors downloading the file
            bot.send_message(chat_id=chat_id, text=str(e))
    # Send a message when all files have been downloaded
    bot.send_message(chat_id=chat_id, text='All files downloaded!')

# Create the updater and add the handler
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('download_files', download_files))

# Start the bot
updater.start_polling()
updater.idle()
