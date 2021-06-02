from os import listdir, stat, mkdir, path
from re import sub
from settings import *
from queue import Queue
import db_manager as dbm


async def download(client, queue: Queue, db_conn):
    """ (TelegramClient object, Message object, Connection object) --> None
    Download the media from the message provided

    client:  TelegramClient object [telethon]
    message: Message object [telethon]
    db_conn: Connection object [sqlite3]
    return: None
    """
    # Checking if the queue is empty
    if queue.is_empty():
        return

    message = queue.dequeue()
    # Making data easier to access
    message_id = message.id
    message = message.document
    file_name = message.attributes[-1].file_name

    # Delete tags in file name if there are
    file_name = sub('^\.*@[A-Za-z0-9]+ ', '', file_name)

    # Path to file
    file = sort_folder(message.mime_type, download_folder)
    file += file_name

    # Skip file already downloaded
    if (file_name in listdir(download_folder) and
            stat(file).st_size == message.size):
        print("File already downloaded")
        return None

    # Download the file
    print(file_name)

    await client.download_media(message,
                                file=file, progress_callback=progress_bar)

    # Writing Database    
    with db_conn:
        add_file = (message_id, file)
        dbm.insert_message(db_conn, add_file)

    # Downloading all the files in queue
    if not queue.is_empty():
        await download(client, queue, db_conn)


async def download_all(client, db_conn, start_date=None, media_type=None):
    """ (TelegramClient object, Connection object, Date object, string) --> string
    Download every media in a chat

    client:  TelegramClient object [telethon]
    db_conn: Connection object [sqlite3]
    start_date: date since when to start downloading files,
     it has to be a Date object [datetime]
    media_type: filter for dowload only one type of media
    return: None
    """
    async for message in client.iter_messages(chat, reverse=True,
                                              offset_date=start_date):

        # Excluding non media messages
        if (not message.media or
                message.sticker):
            continue

        # Skipping media not wanted
        if (message.document.mime_type != media_type):
            if media_type:
                continue

        # Making data easier to access
        message_id = message.id
        message = message.document
        file_name = message.attributes[-1].file_name

        # Delete tags in file name if there are
        file_name = sub('^\.*@[A-Za-z0-9]+ ', '', file_name)

        # Path to file
        file = sort_folder(message.mime_type, download_folder)
        file += file_name

        # Skip file already downloaded
        if (file_name in listdir(download_folder) and
                stat(file).st_size == message.size):
            print("File already downloaded")
            continue

        # Download the file
        print(file_name)
        await client.download_media(message,
                                    file=file, progress_callback=progress_bar)

        # Writing Database    
        with db_conn:
            add_file = (message_id, file)
            dbm.insert_message(db_conn, add_file)


def progress_bar(iteration, total):
    """ (int, int) --> None
    Print a progress bar on the console

    iteration: the size of the downloaded part
    total: the size of the total file """
    percent = round(iteration / total * 100, 1)
    filledLength = 100 * iteration // total
    bar = "#" * filledLength + '-' * (100 - filledLength)
    print('\r%s |%s| %s%% %s' % ('', bar, percent, ''), end="\r")
    # Print a blank line on complete
    if (iteration == total):
        print("\n")


def sort_folder(mime_type, download_path):
    """ (string, string) --> string
    Sort every file by type putting it in a folder

    mime_type: mime_type attribute of the Message object [telethon]
    download_path: path to the main download folder
    return: complete path to the file """
    if (mime_type == 'video/mp4'):
        new_path = path.join(download_path, "Video/")
        if ("Video" not in listdir(download_path)):
            mkdir((new_path))

    elif (mime_type == 'image/png' or
          mime_type == 'image/jpeg'):
        new_path = path.join(download_path, "Pictures/")
        if ("Pictures" not in listdir(download_path)):
            mkdir((new_path))

    elif (mime_type == 'audio/mpeg'):
        new_path = path.join(download_path, "Music/")
        if ("Music" not in listdir(download_path)):
            mkdir((new_path))

    else:
        new_path = path.join(download_path, "Documents/")
        if ("Documents" not in listdir(download_path)):
            mkdir((new_path))

    return new_path
