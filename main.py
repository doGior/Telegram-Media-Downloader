from os import path, mkdir
from settings import *
from telethon import TelegramClient
import asyncio


if(not path.isdir(download_folder)):
    mkdir(download_folder)

if(not path.isfile("id_to_file.db")):
    from db_manager import create_connection, create_table

    db = create_connection("id_to_file.db")

    create_table(db, "CREATE TABLE stocks (date text,\
     trans text, symbol text, qty real, price real)")



'''
client = TelegramClient('anon', api_id, api_hash)

with client:
    try:
        loop = asyncio.get_event_loop()
        import download
        #import remove
        loop.run_until_complete(download._download(client))
    except KeyboardInterrupt:
        pass
'''