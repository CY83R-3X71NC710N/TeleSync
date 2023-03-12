# Python script to upload files inside the encrypted_zips directory one by one to telegram individually using a loop
import os
import random
import string
import telegram
from telegram.ext import Updater, CommandHandler

# Define the token for your Telegram bot
TOKEN = 'YOUR_BOT_TOKEN'

# Define the ID of your Telegram user
USER_ID = 'YOUR_USER_ID'

# Define the path to the directory containing the files to upload
FILES_DIR = os.path.join(os.getcwd(), 'files_to_upload')

# Create a random string of uppercase letters and digits
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Create the Telegram bot object
bot = telegram.Bot(token=TOKEN)

# Create the function to upload the files
def upload_files(update, context):
    chat_id = update.message.chat_id
    # Loop over the files in the files directory
    for file_name in os.listdir(FILES_DIR):
        file_path = os.path.join(FILES_DIR, file_name)
        # Upload the file to the user via direct message
        with open(file_path, 'rb') as f:
            try:
                # Send a message indicating the file is being uploaded
                bot.send_message(chat_id=USER_ID, text=f'Uploading file: {file_name}...')
                bot.send_document(chat_id=USER_ID, document=f)
            except Exception as e:
                # Handle errors uploading the file
                bot.send_message(chat_id=chat_id, text=str(e))
    # Generate a random ID for the uploaded files
    upload_id = generate_random_string()
    # Send a message with the upload ID
    bot.send_message(chat_id=USER_ID, text=f'All files have been uploaded. Your upload ID is {upload_id}.')
    # Store the upload ID and list of files in a text file
    with open(f'{upload_id}.txt', 'w') as f:
        for file_name in os.listdir(FILES_DIR):
            f.write(f'{file_name}\n')

# Create the updater and add the handler
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('upload_files', upload_files))

# Start the bot
updater.start_polling()
updater.idle()
# The script now generates a random ID using the generate_random_string() function and sends it to the user as a message after all files have been uploaded. It also creates a new text file with the upload ID as the filename and writes the list of uploaded file names to it. This file can be used by a downloader script to download all of the files associated with the upload ID.
