import os
import time
from Crypto.Cipher import AES
from telethon import TelegramClient, events

# Telegram API credentials
api_id = 'your_api_id'
api_hash = 'your_api_hash'
phone_number = 'your_phone_number'

# Encryption key and initialization vector
key = b'your_encryption_key'
iv = b'your_initialization_vector'

# Maximum file size in bytes
max_file_size = 1900000000

# Folder path to upload files from
folder_path = 'path_to_folder'

# Telegram client initialization
client = TelegramClient('session_name', api_id, api_hash)

# Encryption function
def encrypt_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = data + b'\0' * (AES.block_size - len(data) % AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

# Decryption function
def decrypt_file(file_path):
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    with open(file_path, 'wb') as f:
        f.write(decrypted_data.rstrip(b'\0'))

# File splitting function
def split_file(file_path):
    file_size = os.path.getsize(file_path)
    if file_size <= max_file_size:
        return [file_path]
    else:
        parts = []
        with open(file_path, 'rb') as f:
            index = 0
            while True:
                part_path = f'{file_path}.part{index + 1}'
                part_size = min(max_file_size, file_size - index * max_file_size)
                if part_size == 0:
                    break
                with open(part_path, 'wb') as part:
                    part.write(f.read(part_size))
                parts.append(part_path)
                index += 1
        return parts

# Telegram file upload function
async def upload_file(file_path):
    async with client:
        async with client.conversation('user_username') as conv:
            await conv.send_file(file_path)

# Main function
async def main():
    while True:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                encrypt_file(file_path)
                file_parts = split_file(file_path)
                sorted_file_parts = sorted(file_parts)  # sort the list of file parts
                for part_path in sorted_file_parts:
                    encrypt_file(file_path)  # encrypt the file before uploading
                    await upload_file(part_path)
                    os.remove(part_path)
                decrypt_file(file_path)
        time.sleep(3600)

# Start the script
client.start(phone_number)
client.loop.run_until_complete(main())
