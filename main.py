import logging
from fastapi import FastAPI
from telethon.tl.functions.channels import InviteToChannelRequest, EditBannedRequest
import os
from telethon.sync import TelegramClient
from dotenv import load_dotenv
from telethon.tl.types import InputPeerChannel

app = FastAPI()
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
)
logger = logging.getLogger(__name__)


@app.get("/")
async def chat(action: str, name: str):
    api_id = int(os.environ['API_ID'])
    api_hash = os.environ['API_HASH']
    phone = os.environ['PHONE']
    client = TelegramClient(phone, api_id, api_hash)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            await client.sign_in(phone, input('Enter the code: '))
        logging.info("Successfully connected")
        channel_id = int(os.environ['CHANNEL_ID'])
        access_hash = int(os.environ['ACCESS_HASH'])
        target_group_entity = InputPeerChannel(channel_id, access_hash)
        user = await client.get_input_entity(name)
        if action == 'add':
            await client(InviteToChannelRequest(target_group_entity, [user]))
            logging.info("Successfully added to channel")
        elif action == 'delete':
            await client.edit_permissions(target_group_entity, user, view_messages=False)
            logging.info("Successfully removed from channel")
    except Exception as ex:
        logging.error(ex)
    finally:
        await client.disconnect()
