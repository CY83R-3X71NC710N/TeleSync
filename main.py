import os
import io
import zipfile
import tempfile
import schedule
import time
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext

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
    # Get the list of files in the local folder
    filenames = os.listdir(FOLDER_PATH)
    
    # Filter the files based on their extension
    filtered_filenames = [filename for filename in filenames if filename.endswith('.pdf') or filename.endswith('.jpg')]
    
    # Check if there are any files to sync
    if not filtered_filenames:
        update.message.reply_text('No files found to sync.')
        return
    
    # Create a temporary directory to store the compressed files
    with tempfile.TemporaryDirectory() as tempdir:
        # Compress the files into a ZIP archive
        archive_path = os.path.join(tempdir, 'archive.zip')
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for filename in filtered_filenames:
                filepath = os.path.join(FOLDER_PATH, filename)
                archive.write(filepath, filename)
                
        # Encrypt the ZIP archive with a password
        password = 'your_password_here'
        encrypted_archive_path = os.path.join(tempdir, 'archive.zip.enc')
        with open(archive_path, 'rb') as f_in, open(encrypted_archive_path, 'wb') as f_out:
            data = f_in.read()
            f_out.write(bytes([i ^ ord(password[i % len(password)]) for i in range(len(data))]))
        
        # Split the encrypted archive into chunks if it's too large to upload
        if os.path.getsize(encrypted_archive_path) > MAX_FILE_SIZE:
            with open(encrypted_archive_path, 'rb') as f:
                # Calculate the number of chunks needed to upload the file
                num_chunks = (os.path.getsize(encrypted_archive_path) + MAX_FILE_SIZE - 1) // MAX_FILE_SIZE
                
                # Upload each chunk as a separate file
                for i in range(num_chunks):
                    chunk = f.read(MAX_FILE_SIZE)
                    bot.send_document(chat_id=USERNAME, document=telegram.InputFile(io.BytesIO(chunk), filename=f'archive_{i+1}.zip.enc'))
        else:
            # Send the file to the Telegram chat
            with open(encrypted_archive_path, 'rb') as f:
                bot.send_document(chat_id=USERNAME, document=f)

    # Send a confirmation message
    update.message.reply_text('Sync complete!')

# Define a function to handle the /schedule_sync command
def schedule_sync(update, context):
    # Define the sync interval (in seconds)
    interval = 60 * 60 * 24 # 24 hours
    
    # Schedule the sync to run at the specified interval
    schedule.every(interval).seconds.do(sync, update=update, context=context)
    
    # Send a confirmation message
    update.message.reply_text('Sync unscheduled.')
# Define a function to handle errors
def error(update, context):
    """Log the error and send a message to the chat."""
    logger.warning(f'Update {update} caused error {context.error}')
    update.message.reply_text(f'An error occurred: {context.error}')

# Set up the Telegram bot handlers
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('sync', sync))
dispatcher.add_handler(CommandHandler('schedule_sync', schedule_sync))
dispatcher.add_handler(CommandHandler('unschedule_sync', unschedule_sync))
dispatcher.add_error_handler(error)

# Start the Telegram bot
updater.start_polling()
print('Telegram bot started.')

# Start the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)

