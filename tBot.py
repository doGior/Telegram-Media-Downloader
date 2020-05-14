import asyncio
from telethon import TelegramClient
from os import listdir, stat, mkdir, path
from re import sub
from settings import *

client = TelegramClient('anon', api_id, api_hash)

#Checking if download path exist
if(not path.isdir(download_folder)):
    mkdir(download_folder)


async def main():
    '''Download every media in a chat'''
    await client.connect()
    async for message in client.iter_messages(chat,
     reverse=True):

        #Excluding non media messages
        if (not message.media or
         not message.document or message.sticker):
            continue
        
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
            continue

        #Download the file
        print(file_name)
        await client.download_media(message,
            file=file, progress_callback=ProgressBar)


def ProgressBar (iteration, total):
    ''' Print a progress bar '''
    percent = round(iteration/total*100, 1)
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

    elif(mime_type == 'image/png'):
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



if __name__ == "__main__":
    with client:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            pass
