import telebot
import os
from vars import admin_user_id


# Function to register the bot commands
def register_plugin(bot):
	@bot.message_handler(commands=['owner'])
	def owner_commands(message):
	    if message.from_user.id != admin_user_id:
	        bot.reply_to(message, "You are not authorized to use this command.")
	        return
	
	    owner_command_list = [
	        "/add userid amount - Add coins to a user's balance",
	        "/cut userid amount - Deduct coins from a user's balance",
	        "/users - Display a list of registered users",
	        "/check - Show users data",
	        "/broadcast message - Send message to all bot user",
	        "/upload - upload users data",
	    ]
	
	    examples = "\n\nExamples:\n"
	    examples += "/add 123456 500\n"
	    examples += "/cut 123456 200\n"
	    examples += "/check 123456\n"
	    examples += "/broadcast hello\n"
	    bot.reply_to(message, "Owner commands:\n" + "\n".join(owner_command_list) + examples)