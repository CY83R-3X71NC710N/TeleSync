# python script to upload files inside the encrypted_zips directory one by one to telegram individually using a loop when running for the first time it will ask you to give your tokens
import subprocess

with open("channel_invite_link.txt", "r") as f:
    invite_link = f.readline().strip()

command = f"telegram-upload .\\encrypted_zips\\** --to {invite_link} --large-files=split --print-file-id --thumbnail-file=.\\preview.png"
subprocess.run(command, shell=True)
