import os
import io
import zipfile
from Crypto.Cipher import AES

# Define the encryption key
password = 'your_password_here'
password_encoded = password.encode('utf-8')

# Define the path to the encrypted file
encrypted_file_path = 'path_to_encrypted_file.enc'

# Define the path where the decrypted file will be saved
decrypted_file_path = 'path_to_decrypted_file'

# Open the encrypted file in binary mode
with open(encrypted_file_path, 'rb') as f_in:
    # Read the contents of the encrypted file
    encrypted_data = f_in.read()

    # Decrypt the file contents using AES
    cipher = AES.new(password_encoded, AES.MODE_EAX)
    decrypted_data = cipher.decrypt(encrypted_data)

    # Write the decrypted data to a new file
    with open(decrypted_file_path, 'wb') as f_out:
        f_out.write(decrypted_data)
