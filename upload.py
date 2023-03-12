# Python script to upload files inside the encrypted_zips directory one by one to telegram individually using a loop
import os
import random
import string
import telegram
from telegram.ext import Updater, CommandHandler

# Define the token for your Telegram bot
TOKEN = 'your_bot_token_here'

# Define the ID of your Telegram user
USER_ID = 'your_user_id_here'

# Define the path to the directory containing the encrypted zip files
ZIP_DIR = os.path.join(os.getcwd(), 'encrypted_zips')

# Create a random string of uppercase letters and digits
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Create the Telegram bot object
bot = telegram.Bot(token=TOKEN)

# Create the channel and invite the user to it
def create_channel(update, context):
    chat_id = update.message.chat_id
    try:
        # Generate a random string and add it to the channel name
        random_string = generate_random_string()
        channel_name = f'backup_{random_string}'
        # Try to create the channel
        result = bot.create_chat(title=channel_name, type='channel', invite_link=True)
        invite_link = result.invite_link
        # Send the invite link to the user
        bot.send_message(chat_id=USER_ID, text=invite_link)
    except Exception as e:
        # Handle errors creating the channel
        bot.send_message(chat_id=chat_id, text=str(e))

# Define the function to upload the zip files
def upload_zip_files(update, context):
    chat_id = update.message.chat_id
    # Loop over the files in the zip directory
    for file_name in os.listdir(ZIP_DIR):
        file_path = os.path.join(ZIP_DIR, file_name)
        # Upload the file to the channel
        with open(file_path, 'rb') as f:
            try:
                bot.send_document(chat_id=channel_name, document=f)
            except Exception as e:
                # Handle errors uploading the file
                bot.send_message(chat_id=chat_id, text=str(e))

# Create the updater and add the handlers
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('create_channel', create_channel))
updater.dispatcher.add_handler(CommandHandler('upload_zips', upload_zip_files))

# Start the bot
updater.start_polling()
updater.idle()
