# TeleSync
Unlimited storage utilizing telegram with folder sync and file splitting. Fast CLI Interface.

# Why create this?
To clarify, many other solutions for backups are not "set and forget," which can be problematic because backups need to be consistently run on a schedule. That's why I created Telesync, which combines AES encrypted files, file splitting, folder sync, and scheduled runs into a single Python script for a more efficient and reliable backup system.

# Goal:
Create code for a telegram script in python that grabs all files in a directory encrypts them and them uploads the files to telegram, however the files should be split into mutiple files if they are above 1.9GB and the script should ask questions such as if you would like to upload or decrypt a file. Decryption should take a file that was uploaded to telegram and decrypt it based on the file location. The script should sync every hour using a batch script.

# Resources: 
```
https://t.me/get_id_bot (Get Chat ID)
https://telegram.me/BotFather (Get Bot Token)
https://pypi.org/project/python-telegram-bot/ pip install python-telegram-bot==13.7 (This specific version is used in the project)
```
