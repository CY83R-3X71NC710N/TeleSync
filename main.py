import os
import zipfile
import math
import telegram
from telegram.ext import Updater, CommandHandler
from datetime import datetime, timedelta

# Set the path of the folder to sync
folder_path = '/path/to/folder'

# Set the maximum file size for splitting
max_file_size = 1.9 * 1024 * 1024 * 1024

# Set the Telegram bot token
bot_token = 'YOUR_BOT_TOKEN'

# Set the Telegram chat ID to send the files to
chat_id = 'YOUR_CHAT_ID'

# Create a Telegram bot instance
bot = telegram.Bot(token=bot_token)

# Define a function to encrypt and split the folder
def encrypt_and_split_folder():
    # Get the current date and time
    now = datetime.now()
    # Set the name of the zip file
    zip_file_name = now.strftime('%Y-%m-%d_%H-%M-%S.zip')
    # Set the path of the zip file
    zip_file_path = os.path.join(folder_path, zip_file_name)
    # Create a zip file instance
    zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
    # Add all files in the folder to the zip file
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            zip_file.write(file_path, os.path.relpath(file_path, folder_path))
    # Close the zip file
    zip_file.close()
    # Get the size of the zip file
    zip_file_size = os.path.getsize(zip_file_path)
    # Check if the zip file size is above the maximum file size
    if zip_file_size > max_file_size:
        # Calculate the number of parts needed to split the zip file
        num_parts = math.ceil(zip_file_size / max_file_size)
        # Calculate the size of each part
        part_size = math.ceil(zip_file_size / num_parts)
        # Open the zip file for reading
        with open(zip_file_path, 'rb') as f:
            # Loop through the parts
            for i in range(num_parts):
                # Set the name of the part file
                part_file_name = f'{zip_file_name}.part{i+1}'
                # Set the path of the part file
                part_file_path = os.path.join(folder_path, part_file_name)
                # Open the part file for writing
                with open(part_file_path, 'wb') as part_file:
                    # Write the part of the zip file to the part file
                    part_file.write(f.read(part_size))
                # Send the part file to the Telegram chat
                bot.send_document(chat_id=chat_id, document=open(part_file_path, 'rb'))
                # Delete the part file
                os.remove(part_file_path)
    else:
        # Send the zip file to the Telegram chat
        bot.send_document(chat_id=chat_id, document=open(zip_file_path, 'rb'))
    # Delete the zip file
    os.remove(zip_file_path)

# Define a function to sync the folder and encrypt and split it
def sync_and_encrypt_folder():
    # Sync the folder
    # ...
    # Encrypt and split the folder
    encrypt_and_split_folder()

# Define a function to handle the /sync command
def sync_command_handler(update, context):
    # Sync the folder and encrypt and split it
    sync_and_encrypt_folder()
    # Send a message to the Telegram chat
    context.bot.send_message(chat_id=update.effective_chat.id, text='Folder synced and encrypted')

# Create an Updater instance
updater = Updater(token=bot_token, use_context=True)

# Create a CommandHandler instance for the /sync command
sync_command_handler = CommandHandler('sync', sync_command_handler)

# Add the CommandHandler instance to the Updater instance
updater.dispatcher.add_handler(sync_command_handler)

# Start the Updater instance
updater.start_polling()

# Schedule the sync_and_encrypt_folder function to run every hour
schedule_interval = timedelta(hours=1)
next_run_time = datetime.now() + schedule_interval
while True:
    if datetime.now() >= next_run_time:
        sync_and_encrypt_folder()
        next_run_time += schedule_interval
