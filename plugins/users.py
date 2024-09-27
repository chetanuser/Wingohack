import telebot
import os
from functions import insertUser, track_exists, addBalance, cutBalance, getData, addRefCount, isExists, setWelcomeStaus, setReferredStatus
import json
from vars import admin_user_id


# Function to register the bot commands
def register_plugin(bot):
	@bot.message_handler(commands=['users'])
	def count_users(message):
	    if message.from_user.id != admin_user_id:
	        bot.reply_to(message, "You are not authorized to use this command.")
	        return
	        
	    try:
	        with open("user_ids.json", "r") as file:
	            user_ids = json.load(file)
	            total_users = len(user_ids)
	            bot.reply_to(message, f"Total users using the bot: {total_users}")
	    except FileNotFoundError:
	        bot.reply_to(message, "No users found.")
	
	
	
	@bot.message_handler(commands=['check'])
	def check_user_data(message):
	    if message.from_user.id != admin_user_id:
	        bot.reply_to(message, "You are not authorized to use this command.")
	        return
	   
	    try:
	        user_id = message.text.split()[1]
	    except IndexError:
	        bot.reply_to(message, "Please provide a user ID to check.")
	        return
	    user_data = getData(user_id)
	    if user_data:
	        username = bot.get_chat(user_id).username if bot.get_chat(user_id).username else "N/A"
	        bot.reply_to(message, f"User ID: {user_id}\nUsername: @{username}\nBalance: {user_data.get('balance', 'N/A')} coins")
	    else:
	        bot.reply_to(message, "User not found.")
	
	        