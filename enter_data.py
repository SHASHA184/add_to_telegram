from telethon.tl.types import InputPeerChannel
import os
from dotenv import load_dotenv
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.sync import TelegramClient

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

api_id = int(input("Enter api_id: "))
api_hash = input("Enter api_hash: ")
phone = input("Enter phone: ")
client = TelegramClient(phone, api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))



chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup:
            groups.append(chat)
    except:
        continue
print('Choose a group to add members: ')
i = 0
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1
g_index = input("Enter a Number: ")
target_group = groups[int(g_index)]
channel_id = target_group.id
access_hash = target_group.access_hash
my_file = open(".env", "w")
my_file.write(f"API_ID={api_id}\n")
my_file.write(f"API_HASH={api_hash}\n")
my_file.write(f"PHONE={phone}\n")
my_file.write(f"CHANNEL_ID={channel_id}\n")
my_file.write(f"ACCESS_HASH={access_hash}\n")
my_file.close()