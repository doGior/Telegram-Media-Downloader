import asyncio
from os import listdir, stat, mkdir, path
from re import sub
from settings import *
import db_manager as dbm

async def _download(client, message, db_conn):
    message_id = message.id
    message = message.document
    file_name = message.attributes[-1].file_name

    #Delete tags in file name if there are
    file_name = sub('^\.*@[A-Za-z0-9]+ ', '', file_name) 

    #Path to file
    file = SortingFolder(message.mime_type, download_folder)
    file += file_name

    #Skip file already downloaded
    if(file_name in listdir(download_folder) and
        stat(file).st_size == message.size):
        print("File already downloaded")
        return None

    #Download the file
    print(file_name)
    await client.download_media(message,
        file=file, progress_callback=ProgressBar)

    #Writing Database    
    with db_conn:
        add_file = (message_id, file)
        dbm.insert_message(db_conn, add_file)

    return file


async def _downloadAll(client, db_conn, start_date = None, media_type = None):
    '''Download every media in a chat'''
    #await client.connect()
    async for message in client.iter_messages(chat, reverse=True,
    offset_date=start_date):

        #Excluding non media messages
        if (not message.media or
         message.sticker):
            continue

        if(message.document.mime_type != media_type):
            if media_type:
                continue
        
        message_id = message.id

        #Make variariabile easier to access
        message = message.document
        file_name = message.attributes[-1].file_name

        #Delete tags in file name if there are
        file_name = sub('^\.*@[A-Za-z0-9]+ ', '', file_name) 

        #Path to file
        file = SortingFolder(message.mime_type, download_folder)
        file += file_name

        #Skip file already downloaded
        if(file_name in listdir(download_folder) and
         stat(file).st_size == message.size):
            print("File already downloaded")
            continue

        #Download the file
        print(file_name)
        await client.download_media(message,
            file=file, progress_callback=ProgressBar)
        
        #Writing Database    
        with db_conn:
            add_file = (message_id, file)
            dbm.insert_message(db_conn, add_file)


def ProgressBar (iteration, total):
    ''' Print a progress bar '''
    percent = round(iteration / total * 100, 1)
    filledLength = 100 * iteration // total
    bar = "#" * filledLength + '-' * (100 - filledLength)
    print('\r%s |%s| %s%% %s' % ('', bar, percent, ''), end = "\r")
    # Print New Line on Complete
    if (iteration == total): 
        print("\n")


def SortingFolder(mime_type, download_path):
    ''' Sort every file by type putting it in a folder '''
    if(mime_type == 'video/mp4'):
        new_path = path.join(download_path,"Video/")
        if ("Video" not in listdir(download_path)):
            mkdir((new_path))

    elif(mime_type == 'image/png' or
    mime_type == 'image/jpeg'):
        new_path = path.join(download_path,"Pictures/")
        if ("Pictures" not in listdir(download_path)):
            mkdir((new_path))

    elif(mime_type == 'audio/mpeg'):
        new_path = path.join(download_path,"Music/")
        if ("Music" not in listdir(download_path)):
            mkdir((new_path))
    
    else:
        new_path = path.join(download_path,"Documents/")
        if ("Documents" not in listdir(download_path)):
            mkdir((new_path))

    return new_path
