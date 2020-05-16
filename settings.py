# Use your own values from my.telegram.org
api_id = 01234567
api_hash = '0123456789abcdef0123456789abcdef'

# Chat from where tou want to download the files
chat = "https://t.me/joinchat/AAAAAE0pUzvX057hFf8vdA"

# Folder in which files will be stored
download_folder = "Downloads/"



# DANGER
# Commands are linked to the functions by position,
# so if you want to change the command for download all the
# media from a chat you must be sure that the new command is
# in the exact previous command's position in this list
cmds = ["/downloadAll", "/downloadToday",
        "/downloadImages", "/downloadVideo","/downloadMusic",
        "/downloadWhenArrive", "/stopDownloadWhenArrive"]