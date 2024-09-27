import telebot
import json
import logging
import time
from telebot import types
from functions import insertUser, track_exists, addBalance, cutBalance, getData, addRefCount, isExists, setWelcomeStaus, setReferredStatus
from vars import admin_user_id

# Configure logging

try:
    with open("user_ids.json", "r") as f:
        user_ids = set(json.load(f))
except FileNotFoundError:
    user_ids = set()

successful_broadcasts = 0
failed_broadcasts = 0

def chunk_list(lst, chunk_size):
    """Divide the list into chunks of the specified size."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def register_plugin(bot):
    @bot.message_handler(commands=['broadcast'])
    def handle_broadcast(message):
        global successful_broadcasts, failed_broadcasts

        if message.chat.id == admin_user_id and message.chat.type == 'private':
            if message.reply_to_message:
                broadcast_message = message.reply_to_message
            else:
                broadcast_message = ' '.join(message.text.split()[1:])
                if not broadcast_message:
                    bot.reply_to(message, "Please specify the message you want to broadcast or reply to a message to forward.")
                    return

            user_chunks = list(chunk_list(list(user_ids), 100))
            for chunk in user_chunks:
                for user_id in chunk:
                    try:
                        if message.reply_to_message:
                            bot.forward_message(user_id, message.reply_to_message.chat.id, message.reply_to_message.message_id)
                        else:
                            bot.send_message(user_id, broadcast_message)
                        successful_broadcasts += 1
                    except Exception as e:
                        logging.error(f"Failed to send message to user {user_id}: {e}")
                        failed_broadcasts += 1

                # Wait between chunks to avoid hitting rate limits
                time.sleep(10)

            bot.reply_to(message, f"Broadcast completed!\n\n"
                                  f"Successful broadcasts: {successful_broadcasts}\n"
                                  f"Failed broadcasts: {failed_broadcasts}")
            logging.info(f"Broadcast completed! Successful: {successful_broadcasts}, Failed: {failed_broadcasts}")
            successful_broadcasts = 0
            failed_broadcasts = 0
        else:
            bot.reply_to(message, "This command is restricted to the bot owner and should be sent in a private chat.")

# Example usage