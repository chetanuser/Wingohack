import telebot
import os
import zipfile
from vars import admin_user_id

ACCOUNT_FOLDER_PATH = 'Account'
USER_IDS_FILE_PATH = 'user_ids.json'
autoview = 'auto.json'
ZIP_FILE_NAME = 'Account.zip'

# Function to create a zip file of the Account folder
def create_zip():
    with zipfile.ZipFile(ZIP_FILE_NAME, 'w') as zipf:
        for root, dirs, files in os.walk(ACCOUNT_FOLDER_PATH):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), ACCOUNT_FOLDER_PATH))
                
                
# Function to register the bot commands
def register_plugin(bot):
	@bot.message_handler(commands=['upload'])
	def handle_upload(message):
	    if message.from_user.id == admin_user_id:
	        try:
	            # Create a zip file of the Account folder
	            create_zip()
	            # Send the zip file
	            bot.send_document(message.chat.id, open(ZIP_FILE_NAME, 'rb'))
	            # Send the user_ids.json file
	            bot.send_document(message.chat.id, open(USER_IDS_FILE_PATH, 'rb'))
	            # Send the user_ids.json file
	            bot.send_document(message.chat.id, open(autoview, 'rb'))	
	            # Delete the zip file after sending
	            os.remove(ZIP_FILE_NAME)
	        except Exception as e:
	            print(f"Error uploading files: {e}")
	            bot.reply_to(message, "Error uploading files.")
	    else:
	        bot.reply_to(message, "This command is restricted to the bot owner.")
	
	        
	        