# TeleSync
Unlimited storage utilizing telegram with folder sync and file splitting. Fast CLI Interface.

# Why create this?
To clarify, many other solutions for backups are not "set and forget," which can be problematic because backups need to be consistently run on a schedule. That's why I created Telesync, which combines AES encrypted files, file splitting, folder sync, and scheduled runs into a single that combines all of the features together for a more efficient and reliable backup system.

# Platforms?:
Currently this is windows only but if it gains enough traction I will bring it over to GNU/Linux and MacOS.

# Goal:
Create code for a telegram script in python that grabs all files in a directory encrypts them and them uploads the files to telegram, however the files should be split into mutiple files if they are above 1.9GB and the script should ask questions such as if you would like to upload or decrypt a file. Decryption should take a file that was uploaded to telegram and decrypt it based on the file location. The script should sync every hour using a batch script.

# How to get started?

Update all the variable values in the script with your values and then run the 24h-run-sync.cmd file for the first time you should answer the first-time-run questios and then it should become automatic every 24h as long as the .cmd script is open. You are able to run this script on a server if needed. The more you add to the sync folder the more that gets encrypted and then uploaded every 24 hours.

# Where to put this folder?
Preferably git clone this repo on the C drive top layer root "/"

# Warning:

Please for back up your keys, if you do not your storage will be for naught do not back them up on telegram back them up on an external private cloud solution. You do not need much storage to back your keys up.

# What is the channel name format?:
```
The format of the date in the file name "backup-20230312_132606" is YYYYMMDD_HHMMSS, where:

YYYY: Represents the year with four digits (e.g., 2023).
MM: Represents the month with two digits (e.g., 03 for March).
DD: Represents the day with two digits (e.g., 12).
HH: Represents the hour with two digits in 24-hour format (e.g., 13 for 1 PM).
MM: Represents the minute with two digits (e.g., 26).
SS: Represents the second with two digits (e.g., 06).
Therefore, the date and time in the file name "backup-20230312_132606" represents March 12, 2023, at 1:26:06 PM.
```

# What does TSA stand for?

TSA stands for TeleSync Archive and is in the preview of the files you upload.

# How to download?:

Running a powershell window in the folder simply run python download.ps1

# Resources: 
```
https://7-zip.org/download.html (Install on windows before running script this is used for the file operations)
https://github.com/Nekmo/telegram-upload pip3 install -U telegram-upload
https://my.telegram.org/apps (ID Values)
https://docs.telethon.dev/en/stable/ (Telethon) pip3 install telethon
https://www.python.org/ (Install python to windows path)
```
