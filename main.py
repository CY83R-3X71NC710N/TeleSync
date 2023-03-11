import os
import telegram
from telegram.ext import Updater, CommandHandler

# Replace with your own Telegram bot token
TOKEN = 'your_token_here'

# Replace with the username of the Telegram user you want to sync with
USERNAME = 'your_username_here'

# Replace with the path of the local folder you want to sync
FOLDER_PATH = 'your_folder_path_here'

# Define the maximum file size (in bytes) that can be uploaded to Telegram
MAX_FILE_SIZE = 50 * 1024 * 1024

# Create a Telegram bot instance
bot = telegram.Bot(token=TOKEN)

# Define a function to handle the /sync command
def sync(update, context):
    for filename in os.listdir(FOLDER_PATH):
        # Build the full path of the file
        filepath = os.path.join(FOLDER_PATH, filename)
        
        # Split the file into chunks if it's too large to upload
        if os.path.getsize(filepath) > MAX_FILE_SIZE:
            with open(filepath, 'rb') as f:
                # Calculate the number of chunks needed to upload the file
                num_chunks = (os.path.getsize(filepath) + MAX_FILE_SIZE - 1) // MAX_FILE_SIZE
                
                # Upload each chunk as a separate file
                for i in range(num_chunks):
                    chunk = f.read(MAX_FILE_SIZE)
                    bot.send_document(chat_id=USERNAME, document=telegram.InputFile(io.BytesIO(chunk), filename=f'{filename}_{i+1}'))
        else:
            # Send the file to the Telegram chat
            with open(filepath, 'rb') as f:
                bot.send_document(chat_id=USERNAME, document=f)

    # Send a confirmation message
    update.message.reply_text('Sync complete!')

# Create an updater instance and attach the command handler
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('sync', sync))

# Start the bot
updater.start_polling()
updater.idle()
