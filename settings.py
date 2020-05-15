# Use your own values from my.telegram.org
api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'

#Chat from where tou want to download the files
chat = "chat link or username or id ord contact"

#Folder in which files will be stored
download_folder = "Downloads/"

#Data from which messages will be downloaded
import datetime
#It has to be a date object or
#None to download all the media from the chat
start_date = datetime.date.today()
