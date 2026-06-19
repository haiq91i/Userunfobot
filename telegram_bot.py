
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n\nMain aapki madad kar sakta hoon Telegram user IDs se public information nikalne mein. Bas `/userinfo <user_id>` command ka upyog karein."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Aap `/userinfo <user_id>` command ka upyog karke kisi bhi user ki public jaankari prapt kar sakte hain. Jaise: `/userinfo 123456789`"
    )

async def get_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetches and displays public information about a user by their ID."""
    if not context.args:
        await update.message.reply_text("Kripya user ID pradaan karein. Upyog: `/userinfo <user_id>`")
        return

    user_id_str = context.args[0]
    try:
        user_id = int(user_id_str)
    except ValueError:
        await update.message.reply_text("Invalid user ID. Kripya ek sankhyatmak user ID pradaan karein.")
        return

    try:
        # get_chat can be used to get information about a user, group, or channel
        # For a user, it returns a Chat object which contains user information
        chat = await context.bot.get_chat(user_id)

        info_message = f"*User Information for ID: {user_id}*\n\n"
        info_message += f"*First Name:* {chat.first_name or 'N/A'}\n"
        if chat.last_name:
            info_message += f"*Last Name:* {chat.last_name}\n"
        if chat.username:
            info_message += f"*Username:* @{chat.username}\n"
        if chat.bio:
            info_message += f"*Bio:* {chat.bio}\n"
        
        # Note: Phone number is NOT accessible via Bot API for privacy reasons.
        # Profile pictures can be fetched but require more complex handling (file downloads).
        # For simplicity, we are not including profile picture download in this basic example.

        await update.message.reply_text(info_message, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Error fetching user info for {user_id}: {e}")
        await update.message.reply_text(
            f"User ID {user_id} ke liye jaankari prapt karne mein asamarth. Sambhav hai ki user ID galat hai, ya bot ko is user tak pahunchne ki anumati nahi hai, ya user ne bot ko block kar diya hai. Error: {e}"
        )

def main() -> None:
    """Start the bot."""
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
    # It's recommended to use environment variables for sensitive information
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set. Please set it.")
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set. Please set it.")
        return

    application = Application.builder().token(token).build()

    # On different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("userinfo", get_user_info))

    # Run the bot until the user presses Ctrl-C
    print("Bot started. Press Ctrl-C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
  
