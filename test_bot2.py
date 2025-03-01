import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# Set up logging to see debug messages in the console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

# Your CoinMarketCap API key
CMC_API_KEY = "4a7ebddd-0919-40a1-bb7c-f74012583aa6"

def get_sol_price():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {"symbol": "SOL", "convert": "USD"}
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": CMC_API_KEY}
    try:
        response = requests.get(url, params=parameters, headers=headers)
        response.raise_for_status()
        data = response.json()
        sol_price = data['data']['SOL']['quote']['USD']['price']
        logging.debug("Fetched SOL price: %s", sol_price)
        return sol_price
    except Exception as e:
        logging.error("Error fetching SOL price: %s", e)
        return None

def adjust_market_cap_filters(current_sol_price, base_sol_price=169):
    base_market_cap_min = 65000
    base_market_cap_max = 75000
    new_market_cap_min = base_market_cap_min * (current_sol_price / base_sol_price)
    new_market_cap_max = base_market_cap_max * (current_sol_price / base_sol_price)
    return new_market_cap_min, new_market_cap_max

def send_confirmation_message(context: CallbackContext, chat_id: int):
    sol_price = get_sol_price()
    if sol_price is None:
        context.bot.send_message(chat_id=chat_id, text="Error fetching SOL price.")
        logging.debug("Error fetching SOL price.")
        return
    new_min, new_max = adjust_market_cap_filters(sol_price)
    message_text = (
        f"Current SOL Price: ${sol_price:.2f}\n"
        f"New Market Cap Thresholds:\n"
        f"Min: ${new_min:.2f}\n"
        f"Max: ${new_max:.2f}\n\n"
        "Do you want to apply these new thresholds?"
    )
    keyboard = [
        [InlineKeyboardButton("Confirm Adjustment", callback_data="confirm"),
         InlineKeyboardButton("Keep Current Settings", callback_data="decline")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=chat_id, text=message_text, reply_markup=reply_markup)
    logging.debug("Confirmation message sent to chat_id: %s", chat_id)

# Minimal adjust command to test handler functionality
def adjust_command(update: Update, context: CallbackContext):
    logging.debug("/adjust command received!")
    chat_id = update.effective_chat.id
    logging.debug("Chat ID: %s", chat_id)
    # For testing, first send a simple text message
    update.message.reply_text("Adjust command triggered!")
    # Uncomment the next line once this simple message works:
    send_confirmation_message(context, chat_id)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "confirm":
        query.edit_message_text(text="New thresholds applied.")
        logging.debug("User confirmed threshold adjustment.")
    elif query.data == "decline":
        query.edit_message_text(text="Keeping current thresholds.")
        logging.debug("User declined threshold adjustment.")

def main():
    # Replace with your actual bot token; ensure it does not have an extra character
    BOT_TOKEN = "7992394508:AAHd0bpcanTVErhre8hOw4TmqD5nIqvU-0w"
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("adjust", adjust_command))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    logging.debug("Bot started polling.")
    updater.idle()

if __name__ == '__main__':
    main()
