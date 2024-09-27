import telebot
import os
import zipfile
import shutil
from vars import admin_user_id
# Initialize variables
current_directory = os.getcwd()
zip_file_path = None

# Function to extract zip file and remove old data in the target directory
def extract_zip(file_path, target_dir):
    if os.path.exists(target_dir):
        # Remove all old data in the target directory
        for filename in os.listdir(target_dir):
            file_path = os.path.join(target_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        os.makedirs(target_dir)
        
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

# Function to register the bot commands
def register_plugin(bot):
    @bot.message_handler(commands=['upl'])
    def handle_upl(message):
        if message.from_user.id != admin_user_id:
            bot.reply_to(message, "You are not authorized to use this bot.")
            return
        if message.reply_to_message and message.reply_to_message.document:
            global zip_file_path
            file_info = bot.get_file(message.reply_to_message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = message.reply_to_message.document.file_name
            file_path = os.path.join(current_directory, file_name)

            # Check if the file already exists
            if os.path.exists(file_path):
                os.remove(file_path)
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            if file_name.endswith('.zip'):
                zip_file_path = file_path
                bot.reply_to(message, "Where do you want to extract this data?")
            else:
                bot.reply_to(message, f"Uploaded {file_name}")
        else:
            bot.reply_to(message, "Please tag a document to upload.")

    @bot.message_handler(commands=['ls'])
    def handle_ls(message):
        if message.from_user.id != admin_user_id:
            bot.reply_to(message, "You are not authorized to use this bot.")
            return

        files = os.listdir(current_directory)
        files_list = '\n'.join(files) if files else "No files in current directory."
        bot.reply_to(message, f"Current directory files:\n{files_list}")

    @bot.message_handler(commands=['cd'])
    def handle_cd(message):
        if message.from_user.id != admin_user_id:
            bot.reply_to(message, "You are not authorized to use this bot.")
            return

        global current_directory
        dir_name = message.text[4:].strip()
        if dir_name:
            new_directory = os.path.join(current_directory, dir_name)
            if os.path.isdir(new_directory):
                current_directory = new_directory
                bot.reply_to(message, f"Changed directory to {current_directory}")
            else:
                bot.reply_to(message, f"Directory {dir_name} does not exist.")
        else:
            bot.reply_to(message, "Please specify a directory name.")

    @bot.message_handler(func=lambda message: zip_file_path is not None)
    def handle_extract(message):
        global zip_file_path
        if message.from_user.id != admin_user_id:
            bot.reply_to(message, "You are not authorized to use this bot.")
            return

        target_dir = os.path.join(current_directory, message.text.strip())

        # Validate the directory path
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        try:
            extract_zip(zip_file_path, target_dir)
            os.remove(zip_file_path)
            zip_file_path = None
            bot.reply_to(message, f"Extracted data to {target_dir}")
        except Exception as e:
            bot.reply_to(message, f"Failed to extract zip file: {e}")
            zip_file_path = None
            