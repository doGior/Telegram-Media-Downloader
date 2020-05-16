from os import path, mkdir, remove
from settings import *
from telethon import TelegramClient, events
from datetime import date
import asyncio
import download
import db_manager as dbm

# Creating the download folder if it doesn't exist
if(not path.isdir(download_folder)):
    mkdir(download_folder)

# Connecting to the database (if the file doesn't
#  exist it will be created)
conn = dbm.create_connection("messages.db")


# Checking if the table exist
c = conn.cursor()

c.execute(''' SELECT count(name) FROM sqlite_master
 WHERE type='table' AND name='id_to_file' ''')

if c.fetchone()[0]==0 : {
    # Create the table if it doesn't exist
    dbm.create_table(conn, '''CREATE TABLE id_to_file
     (Message_Id, File_Path)''')
}

conn.commit()

# Inizializing the Telegram client
client = TelegramClient('anon', api_id, api_hash)

# Binding every command from settings.py with a function
actions = {cmds[0]: download.downloadAll(client, conn),
            cmds[1]: download.downloadAll(client, conn, start_date=date.today()),
            cmds[2]: download.downloadAll(client, conn, media_type='image/png'),
            cmds[3]: download.downloadAll(client, conn, media_type='video/mp4'),
            cmds[4]:download.downloadAll(client, conn, media_type='audio/mpeg',)}

# Inizializing the download immediately when a message arrive
instant_download = True

@client.on(events.NewMessage(chats=chat))
async def DownloadHandler(event):

    # Referencing to the global variable
    global instant_download

    # Making data easier to access
    message = event.message
    text = message.message
    
    # Checking if we have to download 
    # the media immediately when it arrive or not
    if (text == cmds[5]):
        instant_download = True
    elif (text == cmds[6]):
        instant_download = False

    # Checking if the message is a media and,
    #  if we can, downloading it immediately
    if (instant_download and message.media
     and not message.sticker):
        await download.download(client, message, conn)
    # If the message is a text checking
    #  if it is a command and executing it 
    elif text in cmds:
        await actions[text]


@client.on(events.MessageDeleted(chats=chat))
async def RemoveHandler(event):
    # Deleting every file which correspond
    #  to a deleted Telegram's message
    for msg_id in event.deleted_ids:
        file = dbm.delete_message(conn, msg_id)
        remove(file)


#Running the program
with client:
    client.run_until_disconnected()