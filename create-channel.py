from datetime import datetime
from telethon import TelegramClient, functions

api_id = YOUR_API_ID_HERE
api_hash = 'YOUR_API_HASH_HERE'
phone = 'YOUR_PHONE_NUMBER_HERE'

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Login to Telegram
    await client.start(phone)

    # Create the channel name
    channel_name = f"backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Create the channel
    result = await client(functions.channels.CreateChannelRequest(
        title=channel_name,
        about="Backup channel",
        megagroup=False
    ))

    # Get the invite link to the channel
    invite_link = await client(functions.messages.ExportChatInviteRequest(result.chats[0].id))

    # Store the invite link in a text file
    with open("channel_invite_link.txt", "w") as f:
        f.write(f"{invite_link}\n")

    # Print the result
    print(f"Channel '{result.chats[0].title}' (id: {result.chats[0].id}) created successfully.")
    print(f"Invite link: {invite_link.link}")

    # Logout
    await client.disconnect()

with client:
    client.loop.run_until_complete(main())
