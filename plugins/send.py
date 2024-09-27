import telebot

def register_plugin(bot):

    @bot.message_handler(commands=['send'])
    def send_message_to_user(message):
        try:
            # Split the command and arguments
            parts = message.text.split(maxsplit=2)
            if len(parts) < 3:
                bot.reply_to(message, "Usage: /send <user_id> <message>")
                return

            user_id = int(parts[1])
            user_message = parts[2]

            # Send the message to the specified user
            bot.send_message(user_id, user_message)
            bot.reply_to(message, f"Message sent to user {user_id}")
        except ValueError:
            bot.reply_to(message, "Invalid user ID. Please enter a valid user ID.")
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")

# Example usage
