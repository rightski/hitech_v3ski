import warnings
warnings.filterwarnings("ignore", message="python-telegram-bot is using upstream urllib3")

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import Update
from alert_message import send_alert_message

# Replace with your bot token from BotFather
BOT_TOKEN = "7992394508:AAHd0bpcanTVErhre8hOw4TmqD5nIqvU-0w"
# Replace with your Telegram chat id (can be your user id for testing)
CHAT_ID = -1002405468364  # e.g., 123456789

# Dummy coin data for testing
coin_data_example = {
    "coin_name": "DummyCoin",
    "contract_address": "7LCi6CKiidt62SZJAJVQ4v4s62MR4yk1P2n9pVWVpump",
    "launch_time": "2025-02-19 14:05:23 UTC",
    "liquidity": "$7,500",
    "volume": "$5,500",
    "market_cap": "$22,000",
    "transactions": 25,
    "buys": 12,
    "sells": 11,
    "holders": 30,
    "top10": "28%",
    "top5": "8%, 7%, 6%, 4%, 3%",
    "dev_sold": "🟢",  # 🟢 indicates the dev has sold all tokens
    "dex_paid": "🟢",  # 🟢 indicates payment has been made
    "migration": "Pre-migration (Pump.fun → Raydium)",
    "social_presence": "Active"
}

def start(update: Update, context: CallbackContext):
    # When the /start command is issued, send the alert message.
    send_alert_message(context, CHAT_ID, coin_data_example)

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    # You can add logic here to process button presses.
    if query.data == "view_details":
        query.edit_message_text(text="You clicked View Details!")
    elif query.data == "ignore":
        query.edit_message_text(text="You clicked Ignore!")
    elif query.data == "take_action":
        query.edit_message_text(text="You clicked Take Action!")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handler for /start to trigger the alert
    dp.add_handler(CommandHandler("start", start))
    # Add callback query handler for inline buttons
    dp.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
