# Create code for a telegram script in python that grabs all files in a directory encrypts them and them uploads the files to telegram, however the files should be split into mutiple files if they are above 1.9GB and the script should ask questions such as if you would like to upload or decrypt a file. Decryption should take a file that was uploaded to telegram and decrypt it based on the file location. The script should sync every hour.

# Import the required modules including the module we will use to access telegram as a user and not a bot
import os
import time
import pyAesCrypt
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message

# Create a function that will encrypt the files
def encrypt_file(file, password):
    # Create a buffer size for the encryption
    bufferSize = 64 * 1024
    # Create a variable for the encrypted file
    encrypted_file = file + ".aes"
    # Encrypt the file
    pyAesCrypt.encryptFile(file, encrypted_file, password, bufferSize)
    # Delete the original file
    os.remove(file)

# Create a function that will decrypt the files
def decrypt_file(file, password):
    # Create a buffer size for the decryption
    bufferSize = 64 * 1024
    # Create a variable for the decrypted file
    decrypted_file = file.replace(".aes", "")
    # Decrypt the file
    pyAesCrypt.decryptFile(file, decrypted_file, password, bufferSize)
    # Delete the original file
    os.remove(file)

# Ask the user if they want to decrypt a file they encrypted or proceed with the rest of the script
decrypt = input("Would you like to decrypt a file you encrypted? (y/n): ")
if decrypt == "y":
    # Ask the user for the password they used to encrypt the file
    password = input("Please enter the password you used to encrypt the file: ")
    # Ask the user for the file they wish to decrypt
    file = input("Please enter the file you wish to decrypt: ")
    # Decrypt the file
    decrypt_file(file, password)
    # Exit the script
    exit()
if decrypt == "n":
    pass

# Ask the user for the password they wish to use
password = input("Please enter the password you wish to use: ")

# ENCRYPT THE ENTIRE DIRECTORY AND EVERY SINGLE FILE INSIDE IT
# Create a for loop that will loop through every file in the directory
for file in os.listdir():
    # Check if the file is a file and not a directory
    if os.path.isfile(file):
        # Check if the file is above 1.9GB
        if os.path.getsize(file) > 2000000000:
            # Create a variable for the file size
            file_size = os.path.getsize(file)
            # Create a variable for the number of parts the file will be split into
            number_of_parts = file_size / 2000000000
            # Create a variable for the size of each part
            part_size = file_size / number_of_parts
            # Create a variable for the current part
            current_part = 1
            # Create a variable for the current part size
            current_part_size = 0
            # Create a variable for the current part name
            current_part_name = file + ".part" + str(current_part)
            # Create a variable for the current part file
            current_part_file = open(current_part_name, "wb")
            # Create a variable for the current file
            current_file = open(file, "rb")
            # Create a variable for the current file data
            current_file_data = current_file.read(1024)
            # Create a while loop that will loop until the current part size is greater than the part size
            while current_part_size < part_size:
                # Write the current file data to the current part file
                current_part_file.write(current_file_data)
                # Add the current file data to the current part size
                current_part_size += len(current_file_data)
                # Read the next 1024 bytes of the current file
                current_file_data = current_file.read(1024)
                # Check if the current part size is greater than the part size
                if current_part_size > part_size:
                    # Close the current part file
                    current_part_file.close()
                    # Encrypt the current part file
                    encrypt_file(current_part_name, password)
                    # Increment the current part
                    current_part += 1
                    # Create a variable for the current part name
                    current_part_name = file + ".part" + str(current_part)
                    # Create a variable for the current part file
                    current_part_file = open(current_part_name, "wb")
                    # Create a variable for the current part size
                    current_part_size = 0
            # Close the current part file
            current_part_file.close()
            # Encrypt the current part file
            encrypt_file(current_part_name, password)
            # Close the current file
            current_file.close()
            # Delete the original file
            os.remove(file)
        # Check if the file is below 1.9GB
        else:
            # Encrypt the file
            encrypt_file(file, password)


