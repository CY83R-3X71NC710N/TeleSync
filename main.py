import os
import telegram
from telegram.ext import Updater, CommandHandler
import zipfile
from cryptography.fernet import Fernet
import random
import shutil
import string
from datetime import datetime, timedelta

# Check if the key file exists
if os.path.isfile('key.txt'):
    use_existing_key = input("Do you want to use the existing key in key.txt? (y/n): ")
    if use_existing_key.lower() == 'y':
        # Read the key from file
        with open('key.txt', 'rb') as f:
            key = f.read()
    else:
        # Generate a new key
        key = Fernet.generate_key()
        # Create a backup of the key
        backup_name = 'key_backup_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        shutil.copyfile('key.txt', backup_name)
        # Save the key to file
        with open('key.txt', 'wb') as f:
            f.write(key)
else:
    # Generate a new key
    key = Fernet.generate_key()
    # Save the key to file
    with open('key.txt', 'wb') as f:
        f.write(key)
        
print(f"Using key: {key}")

def encrypt(file_data):
    # Create a Fernet instance with the key
    f = Fernet(key)
    # Encrypt the data with Fernet
    encrypted_data = f.encrypt(file_data)
    return encrypted_data

def decrypt_data(encrypted_data):
    # Create a Fernet instance with the key
    f = Fernet(key)
    # Decrypt the data with Fernet
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data

def encrypt_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Check if the file is not a directory
            if not os.path.isdir(file_path):
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                encrypted_data = encrypt(file_data)
                with open(file_path, 'wb') as f:
                    f.write(encrypted_data)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            encrypt_folder(dir_path)

def decrypt_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.enc'):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                decrypted_data = decrypt_data(file_data)
                with open(os.path.splitext(file_path)[0], 'wb') as f:
                    f.write(decrypted_data)
                os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            decrypt_folder(dir_path)

# Create the encrypted_zips directory if it doesn't exist
encrypted_zips_path = os.path.join(os.getcwd(), 'encrypted_zips')
if not os.path.exists(encrypted_zips_path):
    os.makedirs(encrypted_zips_path)

# Set the path of the folder to sync
folder_path = os.path.join(os.getcwd(), 'sync')
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Set the maximum file size for splitting
max_file_size = 1.9 * 1024 * 1024 * 1024

# Set the Telegram bot token
bot_token = ''

# Set the Telegram chat ID to send the files to
chat_id = ''

decrypt = input("Do you want to decrypt a folder? (Y/N): ")
if decrypt.lower() == 'y':
    path = input("Please enter the path to the folder you want to decrypt: ")
    decrypt_folder(path)
else:
    print("Okay, no files will be decrypted.")

# Create a Telegram bot instance
bot = telegram.Bot(token=bot_token)
def encrypt_and_split_folder():
    # Get the current date and time
    now = datetime.now()
    # Set the name of the zip file
    zip_file_name = f'backup_{now.strftime("%Y-%m-%d_%H-%M-%S")}.zip'
    # Set the path of the zip file
    zip_file_path = os.path.join(encrypted_zips_path, zip_file_name)
    # Create a ZipFile object to write the encrypted archive
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the directory tree and add each file to the archive
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    # Generate the name of the encrypted file
                    encrypted_file_name = f'{os.path.relpath(file_path, folder_path)}.enc'
                    # Encrypt the file data
                    encrypted_data = encrypt(f.read())
                    # Write the encrypted file to the archive
                    zipf.writestr(encrypted_file_name, encrypted_data)
    # Get the size of the zip file
    zip_file_size = os.path.getsize(zip_file_path)
    # Check if the zip file size is above the maximum file size
    if zip_file_size > max_file_size:
        # Calculate the number of parts needed to split the zip file
        num_parts = -(-zip_file_size // max_file_size)
        # Split the encrypted zip file
        with open(zip_file_path, 'rb') as f:
            # Read the data from the zip file
            zip_data = f.read()
            # Split the data into parts
            part_size = max_file_size
            for i in range(num_parts):
                # Generate the name of the part file
                part_file_name = f'{zip_file_name}.part{i+1}'
                part_file_path = os.path.join(encrypted_zips_path, part_file_name)
                # Write the part data to a file
                with open(part_file_path, 'wb') as part_file:
                    part_file.write(zip_data[:part_size])
                # Send the part file to the Telegram chat
                bot.send_document(chat_id=chat_id, document=open(part_file_path, 'rb'))
                # Delete the part file
                os.remove(part_file_path)
                # Remove the written data from the zip_data
                zip_data = zip_data[part_size:]
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

# Sync and encrypt folder once for the start of the script
sync_and_encrypt_folder()
