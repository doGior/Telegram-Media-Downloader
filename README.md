# Telegram-Media-Downloader
This is a bot that will download all the media from a given chat.<br/>
When a media is sent to the specified chat it will be downloaded and when that<br> message will be deleted from the chat the file will be deleted also from the pc <br>

**Note:** all the media have to be sent as document

## Installation
Run this on your shell
```
git clone "https://github.com/KalleHallden/ProjectInitializationAutomation.git"
cd ProjectInitializationAutomation
pip install -r requirements.txt
```
Then you have to edit the settings.py with your information and run main.py

## Commands
You can send text message on telegram for modifying the bot's beheavior<br/>
By default there are six commands:

* */downloadAll* --> Will download all the media from the selected chat
* */downloadToday* --> Will download all the media sen today from the selected chat
* */downloadImages* --> Will download all the Images from the selected chat
* */downloadVideo* --> Will download all the Videos from the selected chat
* */downloadMusic* --> Will download all the Audio file from the selected chat
* */downloadWhenArrive* --> Will download every media immediately when it arrive; it's True by default
* */stopDownloadWhenArrive* --> Will stop downloading every media immediately when it arrive
