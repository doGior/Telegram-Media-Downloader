from datetime import date
from os import path, mkdir, remove

from telethon import TelegramClient, events

import db_manager as dbm
import download
from settings import *

# Initializing the Telegram client
client = TelegramClient('anon', api_id, api_hash)

async def hello():
    await client.send_message(chat, "**Bot Activated!**😀\n" +
                              "I will download every media sent in this chat\n\n" +
                              "Here are the avaible commands:\n" +
                              "**/downloadAll** --> Will download all the media from the selected chat\n" +
                              "**/downloadToday** --> Will download all the media sent today from the selected chat\n" +
                              "**/downloadImages** --> Will download all the Images from the selected chat\n" +
                              "**/downloadVideo** --> Will download all the Videos from the selected chat\n" +
                              "**/downloadMusic** --> Will download all the Audio file from the selected chat\n" +
                              "**/downloadWhenArrive** --> Will download every media immediately when it arrive;"
                              " it's True by default\n" + "**/stopDownloadWhenArrive** --> Will stop downloading"
                                                          " every media immediately when it arrive")
    print("Message sent")


@client.on(events.NewMessage(chats=chat))
async def download_handler(event):
    # Referencing to the global variable
    global instant_download

    # Making data easier to access
    message = event.message
    text = message.message

    # Checking if we have to download
    # the media immediately when it arrive or not
    if text == cmds[5]:
        instant_download = True
    elif text == cmds[6]:
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
async def remove_handler(event):
    # Deleting every file which correspond
    #  to a deleted Telegram's message
    for msg_id in event.deleted_ids:
        file = dbm.delete_message(conn, msg_id)
        remove(file)


if __name__ == "__main__":
    # Creating the download folder if it doesn't exist
    if not path.isdir(download_folder):
        mkdir(download_folder)

    # Connecting to the database (if the file doesn't
    #  exist it will be created)
    conn = dbm.create_connection("messages.db")

    # Checking if the table exist
    c = conn.cursor()

    c.execute(''' SELECT count(name) FROM sqlite_master
     WHERE type='table' AND name='id_to_file' ''')

    if c.fetchone()[0] == 0:
        # Create the table if it doesn't exist
        dbm.create_table(conn, '''CREATE TABLE id_to_file
         (Message_Id, File_Path)''')

    conn.commit()

    # Binding every command from settings.py with a function
    actions = {cmds[0]: download.download_all(client, conn),
               cmds[1]: download.download_all(client, conn, start_date=date.today()),
               cmds[2]: download.download_all(client, conn, media_type='image/png'),
               cmds[3]: download.download_all(client, conn, media_type='video/mp4'),
               cmds[4]: download.download_all(client, conn, media_type='audio/mpeg', )}

    # Initializing the download immediately when a message arrive
    instant_download = True

    # Running the program
    with client:
        client.loop.run_until_complete(hello())
        client.run_until_disconnected()
