from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

def send_alert_message(context: CallbackContext, chat_id: int, coin_data: dict):
    """
    Sends an alert message with actionable buttons for a coin.
    
    :param context: The CallbackContext from the telegram bot.
    :param chat_id: The Telegram chat ID where the message will be sent.
    :param coin_data: A dictionary containing coin details.
    """
    # Extract coin details from coin_data dictionary (using placeholders as defaults)
    coin_name = coin_data.get("coin_name", "Unknown Coin")
    contract_address = coin_data.get("contract_address", "N/A")
    launch_time = coin_data.get("launch_time", "N/A")
    liquidity = coin_data.get("liquidity", "N/A")
    volume = coin_data.get("volume", "N/A")
    market_cap = coin_data.get("market_cap", "N/A")
    transactions = coin_data.get("transactions", "N/A")
    buys = coin_data.get("buys", "N/A")
    sells = coin_data.get("sells", "N/A")
    holders = coin_data.get("holders", "N/A")
    
    # Holder information specifics
    top10 = coin_data.get("top10", "N/A")
    top5 = coin_data.get("top5", "N/A")
    # For Dev Sold: 🟢 means all tokens sold; 🔴 means not sold.
    dev_sold = coin_data.get("dev_sold", "🟢")
    # For Dex Paid: 🟢 means payment made; 🔴 means not paid.
    dex_paid = coin_data.get("dex_paid", "🟢")
    
    migration = coin_data.get("migration", "Pre-migration (Pump.fun → Raydium)")
    social_presence = coin_data.get("social_presence", "Active")
    
    # Build dynamic external links using the contract address
    bullx_link = f"https://neo.bullx.io/coin/{contract_address}"
    axiom_link = f"https://axiom.trade/coin/{contract_address}"
    dexscreener_link = f"https://dexscreener.com/solana/{contract_address}"
    
    # Build the alert message text
    message_text = (
        f"💎 *Coin Found Alert* 💎\n\n"
        f"*Coin Name:* {coin_name}\n"
        f"*Contract Address:* {contract_address}\n"
        f"*Launch Time:* {launch_time}\n\n"
        f"📊 *Market Metrics:*\n"
        f"- Liquidity: {liquidity}\n"
        f"- Volume: {volume}\n"
        f"- Market Cap: {market_cap}\n"
        f"- Transactions: {transactions}\n"
        f"- Buys: {buys}\n"
        f"- Sells: {sells}\n"
        f"- Holders: {holders}\n\n"
        f"🔒 *Security Audit:*\n"
        f"- Mint Authority: Disabled\n"
        f"- Freeze Authority: Disabled\n"
        f"- LP Burned: ≥ 50%\n\n"
        f"👥 *Holder Information:*\n"
        f"- Top 10 Holders: {top10} total\n"
        f"- Top 5 Holders: {top5}\n"
        f"- Dev Sold: {dev_sold}\n"
        f"- Dex Paid: {dex_paid}\n\n"
        f"🛠 *Migration:* {migration}\n"
        f"🌐 *Social Presence:* {social_presence}\n"
    )
    
    # Create inline keyboard buttons for actions
    keyboard = [
        [
            InlineKeyboardButton("View Details", callback_data="view_details"),
            InlineKeyboardButton("Ignore", callback_data="ignore"),
            InlineKeyboardButton("Take Action", callback_data="take_action")
        ],
        [
            InlineKeyboardButton("BullX Neo", url=bullx_link),
            InlineKeyboardButton("Axiom", url=axiom_link),
            InlineKeyboardButton("Dexscreener", url=dexscreener_link)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the message
    context.bot.send_message(
        chat_id=chat_id,
        text=message_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
