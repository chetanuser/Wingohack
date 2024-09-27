import telebot
import re
import json
from telebot import types
import requests
import time
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from functions import insertUser, track_exists, addBalance, cutBalance, getData, addRefCount, isExists, setReferredStatus
import os
import importlib.util
from vars import*

bot = telebot.TeleBot(bot_token)

# Load plugins dynamically from the plugins folder
plugin_folder = 'plugins'
for filename in os.listdir(plugin_folder):
    if filename.endswith('.py'):
        plugin_name = filename[:-3]
        spec = importlib.util.spec_from_file_location(plugin_name, os.path.join(plugin_folder, filename))
        plugin_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin_module)
        if hasattr(plugin_module, 'register_plugin'):
            plugin_module.register_plugin(bot)

try:
    with open("user_ids.json", "r") as f:
        user_ids = set(json.load(f))
except FileNotFoundError:
    user_ids = set()

successful_messages = 0
failed_messages = 0

# Temporary storage for user states
user_states = {}

# Function to check if the user is a member of all required channels
def is_member_of_channel(user_id):
    for channel in required_channels:
        status = bot.get_chat_member(channel, user_id).status
        if status not in ['member', 'administrator', 'creator']:
            return False
    return True

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    first_name = message.from_user.first_name
    global user_ids
    user_ids.add(message.chat.id)
    with open("user_ids.json", "w") as f:
        json.dump(list(user_ids), f)
    ref_by = message.text.split()[1] if len(
        message.text.split()) > 1 and message.text.split()[1].isdigit() else None

    if ref_by and int(ref_by) != int(user_id) and track_exists(ref_by):
        if not isExists(user_id):
            initial_data = {
                "user_id": user_id,
                "balance": 0.00,
                "ref_by": ref_by,
                "referred": 0,
                "total_refs": 0,
            }
            insertUser(user_id, initial_data)
            addRefCount(ref_by)

    if not isExists(user_id):
        initial_data = {
            "user_id": user_id,
            "balance": 0.00,
            "ref_by": "none",
            "referred": 0,
            "total_refs": 0,
        }
        insertUser(user_id, initial_data)

    if not is_member_of_channel(user_id):
        markup = types.InlineKeyboardMarkup()
        join = types.InlineKeyboardButton("✨ join ✨", url=f"https://t.me/WingoGiftCodess")
        join2 = types.InlineKeyboardButton("✨ join ✨", url=f"https://t.me/BlackScripter")
        join3 = types.InlineKeyboardButton("✨ join ✨", url=f"https://telegram.me/+1faadLPHlOpjNGY1")
        markup.add(join, join2)
        markup.add(join3)

        bot.send_photo(
            user_id, logo_url,
            caption="You need to join the following channels before continuing:\n\nafter joining channels, send /start again",
            parse_mode='HTML',
            reply_markup=markup  # Pass the markup to the reply
        )
        return

    userData = getData(user_id)
    refby = userData['ref_by']
    referred = userData['referred']
    if refby != "none" and referred == 0:
        bot.send_message(refby, f"You referred {first_name} +{ref_bonus} coins")
        addBalance(refby, ref_bonus)
        setReferredStatus(user_id)

    # Main menu buttons using InlineKeyboard
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("🛒 Recharge hack", callback_data='order')
    button2 = InlineKeyboardButton("👤 My Account", callback_data='my_account')
    button3 = InlineKeyboardButton("💻 wingo hack", callback_data='buy_coins')
    button4 = InlineKeyboardButton("🗣 Refer", callback_data='refer')

    markup.add(button1)
    markup.add(button4, button3)
    markup.add(button2)
    bot.send_photo(user_id, logo_url, caption="""Hi, welcome to wingo hack 💓✋. 

👇🏻 To continue, choose an item""", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    message_id = call.message.message_id
    bot_username = bot.get_me().username
    first_name = call.from_user.first_name

    # Main menu buttons using InlineKeyboard
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("🛒 Recharge hack", callback_data='order')
    button2 = InlineKeyboardButton("👤 My Account", callback_data='my_account')
    button3 = InlineKeyboardButton("💻 wingo hack", callback_data='buy_coins')
    button4 = InlineKeyboardButton("🗣 Refer", callback_data='refer')

    markup.add(button1)
    markup.add(button4, button3)
    markup.add(button2)

    if call.data == "my_account":
        referral_link = f"https://t.me/{bot_username}?start={user_id}"
        data = getData(user_id)
        total_refs = data['total_refs']
        balance = data['balance']

        msg = f"""<b><u>My Account</u></b>
🆔 User ID: {user_id}
👤 Username: @{call.from_user.username}
🗣 Invited Users: {total_refs}
🔗 Referral Link: {referral_link}

👁‍🗨 Balance: <code>{balance}</code> coins
"""
        bot.edit_message_caption(chat_id=user_id, message_id=message_id, caption=msg, parse_mode='html', reply_markup=markup)

    elif call.data == "refer":
        bot_username = bot.get_me().username  # Get the bot's username
        referral_link = f"https://t.me/{bot_username}?start={user_id}"
        data = getData(user_id)
        total_refs = data['total_refs']
        msg = f"<b>Referral Link:</b> {referral_link}\n\n<b><u>Share it with friends and get {ref_bonus} coins for each referral</u></b>"
        bot.edit_message_caption(chat_id=user_id, message_id=message_id, caption=msg, parse_mode='html', reply_markup=markup)

    elif call.data == 'order':
        # Send message "Select app" with buttons "App1" and "App2"
        app_markup = InlineKeyboardMarkup()
        app1_button = InlineKeyboardButton("App1", callback_data='select_app1')
        app2_button = InlineKeyboardButton("App2", callback_data='select_app2')
        app_markup.add(app1_button, app2_button)
        bot.send_message(user_id, f"Please select an app:", reply_markup=app_markup)

    elif call.data == 'select_app1':
        # Send message to user with link to make id for app1, and ask user to send their userid
        bot.send_message(user_id, f"Please create an account using this link:\n\n {reflink}\n\n\nAfter creating an account, please send me your user ID.", parse_mode='Markdown')
        bot.register_next_step_handler_by_chat_id(user_id, process_userid, 'App1')

    elif call.data == 'select_app2':
        bot.send_message(user_id, f"Please create an account using this link: \n\n{reflink}\n\n\nAfter creating an account, please send me your user ID.", parse_mode='Markdown')
        bot.register_next_step_handler_by_chat_id(user_id, process_userid, 'App2')

    elif call.data.startswith('amount_'):
        amount = call.data.split('_')[1]  # '500', '1000', etc.
        user_state = user_states.get(user_id)
        if user_state:
            app_name = user_state['app_name']
            user_app_userid = user_state['userid']
            # Now process the submission
            # For example, save to database, or send notification to admin
            # Send message to user
            bot.send_message(user_id, "Success! Submitted. Your balance will be added in 24h")
            # Optionally, send message to admin with the details
            admin_user_id = admin_user_id  # Replace with actual admin user id or fetch from vars
            bot.send_message(admin_user_id, f"User {user_id} requested recharge hack.\nApp: {app_name}\nUserID: {user_app_userid}\nAmount: {amount}")
            # Clear the user state
            del user_states[user_id]
        else:
            bot.send_message(user_id, "An error occurred. Please start over.")
            # Clear the user state just in case
            if user_id in user_states:
                del user_states[user_id]

    elif call.data == "buy_coins":
        # When the user clicks on "💻 wingo hack", forward the message without forward tag
        from_chat_id = '@thanosseen'
        message_id_to_forward = 219  # The message ID in the channel
        try:
            bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=message_id_to_forward)
        except Exception as e:
            bot.send_message(user_id, "Sorry, an error occurred while processing your request.")
            print(f"Error forwarding message: {e}")

def process_userid(message, app_name):
    user_id = message.from_user.id
    user_input = message.text
    # Store the app name and user ID in user_states
    user_states[user_id] = {'app_name': app_name, 'userid': user_input}
    # Ask the user to select amount
    amount_markup = InlineKeyboardMarkup()
    amount_buttons = [
        InlineKeyboardButton("500", callback_data='amount_500'),
        InlineKeyboardButton("1000", callback_data='amount_1000'),
        InlineKeyboardButton("1500", callback_data='amount_1500'),
        InlineKeyboardButton("2000", callback_data='amount_2000')
    ]
    amount_markup.add(*amount_buttons)
    bot.send_message(user_id, "Please select an amount:", reply_markup=amount_markup)

print("Bot is running")
bot.polling()
