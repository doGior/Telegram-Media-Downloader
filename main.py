from os import path, mkdir, remove
from settings import *
from telethon import TelegramClient, events
from datetime import date
import db_manager as dbm
import asyncio
import download


if(not path.isdir(download_folder)):
    mkdir(download_folder)


conn = dbm.create_connection("messages.db")


#Checking if the table exist
c = conn.cursor()

#get the count of tables with the name
c.execute(''' SELECT count(name) FROM sqlite_master
 WHERE type='table' AND name='id_to_file' ''')


#if the count is 1, then table exists
if c.fetchone()[0]==0 : {
    dbm.create_table(conn, '''CREATE TABLE id_to_file
     (Message_Id, File_Path)''')
}

conn.commit()


client = TelegramClient('anon', api_id, api_hash)
actions = {cmds[0]: download._downloadAll(client, conn),
            cmds[1]: download._downloadAll(client, conn, start_date=date.today()),
            cmds[2]: download._downloadAll(client, conn, media_type='image/png'),
            cmds[3]: download._downloadAll(client, conn, media_type='video/mp4'),
            cmds[4]:download._downloadAll(client, conn, media_type='audio/mpeg',)}


instant_download = True

@client.on(events.NewMessage(chats=chat))
async def DownloadHandler(event):

    global instant_download

    message = event.message
    text = message.message
    
    if (text == cmds[5]):
        instant_download = True
    elif (text == cmds[6]):
        instant_download = False

    #print(instant_download)
    if (message.media and instant_download
     and not message.sticker):
        await download._download(client, message, conn)
    elif text in cmds:
        await actions[text]


@client.on(events.MessageDeleted(chats=chat))
async def RemoveHandler(event):
    for msg_id in event.deleted_ids:
        file = dbm.delete_message(conn, msg_id)
        print(file)
        remove(file)



with client:
    client.run_until_disconnected()
    
