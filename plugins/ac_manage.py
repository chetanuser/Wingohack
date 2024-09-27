import telebot
import re
import json
from telebot import types
import requests
import time
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from functions import insertUser, track_exists, addBalance, cutBalance, getData, addRefCount, isExists, setWelcomeStaus, setReferredStatus
import telebot
import os
import importlib.util
from vars import admin_user_id



# Function to register the bot commands
def register_plugin(bot):
	@bot.message_handler(commands=['cut'])
	def cut_coins(message):
	    if message.from_user.id != admin_user_id:
	        bot.reply_to(message, "You are not authorized to use this command.")
	        return
	    try:
	        command_parts = message.text.split()
	        if len(command_parts) != 3:
	            raise ValueError("Invalid command format. Use /cut userid amount")
	        user_id = command_parts[1]
	        amount = float(command_parts[2])
	        # Check if the user exists
	        if not isExists(user_id):
	            bot.reply_to(message, "User does not exist.")
	            return
	            
	        # Cut balanc
	        if amount > 0:
	            cutBalance(user_id, amount)
	            bot.reply_to(message, f"{amount} coins deducted from user {user_id}'s balance.")
	            bot.send_message(user_id, f"{amount} coins have been deducted from your balance.")
	        else:
	            bot.reply_to(message, "Amount should be a positive value.")
	    except ValueError as ve:
	        bot.reply_to(message, str(ve))
	
	       
	
	@bot.message_handler(commands=['add'])
	def add_coins(message):
	    if message.from_user.id != admin_user_id:
	        bot.reply_to(message, "You are not authorized to use this command.")
	        return
	    try:
	        command_parts = message.text.split()
	        if len(command_parts) != 3:
	            raise ValueError("Invalid command format. Use /add userid amount")    
	
	        user_id = command_parts[1]
	        amount = float(command_parts[2])
	        # Check if the user exists
	        if not isExists(user_id):
	            bot.reply_to(message, "User does not exist.")
	            return
	        # Add or cut balance
	        if amount > 0:
	            addBalance(user_id, amount)
	            bot.reply_to(message, f"{amount} coins added to user {user_id}'s balance.")
	            bot.send_message(user_id, f"{amount} coins have been added to your balance.")
	        elif amount < 0:
	            current_balance = getData(user_id)['balance']
	            if current_balance + amount < 0:
	                bot.reply_to(message, f"The user's balance cannot go negative.")
	                return
	            cutBalance(user_id, abs(amount))
	            bot.reply_to(message, f"{abs(amount)} coins deducted from user {user_id}'s balance.")
	            bot.send_message(user_id, f"{abs(amount)} coins have been deducted from your balance.")
	        else:
	            bot.reply_to(message, "Amount should be a non-zero value.")
	    except ValueError as ve:
	        bot.reply_to(message, str(ve))
	        