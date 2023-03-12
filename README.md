# TeleSync
Unlimited storage utilizing telegram with folder sync and file splitting. Fast CLI Interface.

# Why create this?
To clarify, many other solutions for backups are not "set and forget," which can be problematic because backups need to be consistently run on a schedule. That's why I created Telesync, which combines AES encrypted files, file splitting, folder sync, and scheduled runs into a single Python script for a more efficient and reliable backup system.

# Platforms?:
Currently this is windows only but if it gains enough traction I will bring it over to GNU/Linux and MacOS.

# Goal:
Create code for a telegram script in python that grabs all files in a directory encrypts them and them uploads the files to telegram, however the files should be split into mutiple files if they are above 1.9GB and the script should ask questions such as if you would like to upload or decrypt a file. Decryption should take a file that was uploaded to telegram and decrypt it based on the file location. The script should sync every hour using a batch script.

# How to get started?

Update all the variable values in the script with your values and then run the 24h-run-sync.cmd file for the first time you should answer the first-time-run questios and then it should become automatic every 24h as long as the .cmd script is open. You are able to run this script on a server if needed.

# Warning:

Please for back up your keys, if you do not your storage will be for naught do not back them up on telegram back them up on an external private cloud solution. You do not need much storage to back your keys up.

# Resources: 
```
https://7-zip.org/download.html
https://github.com/Nekmo/telegram-upload pip3 install -U telegram-upload
https://my.telegram.org/apps (ID Values)

```
