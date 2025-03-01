from telegram import Bot

# Replace with your actual bot token
BOT_TOKEN = "7992394508:AAHd0bpcanTVErhre8hOw4TmqD5nIqvU-0w"

# Initialize the bot
bot = Bot(BOT_TOKEN)

# Clear the webhook
result = bot.delete_webhook()
if result:
    print("Webhook cleared successfully!")
else:
    print("Failed to clear the webhook. It might already be cleared.")
