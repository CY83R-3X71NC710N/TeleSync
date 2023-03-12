import os
import subprocess

# Check if telegram_downloads directory exists, if not create it
if not os.path.exists('telegram_downloads'):
    os.mkdir('telegram_downloads')

# Switch to telegram_downloads directory
os.chdir('telegram_downloads')

# Run the telegram-download --interactive command
subprocess.run(['telegram-download', '--interactive'])
