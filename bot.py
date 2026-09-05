import os
import sys
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

print(f"DEBUG: TOKEN = {TOKEN}")
print(f"DEBUG: TOKEN type = {type(TOKEN)}")
print(f"DEBUG: TOKEN length = {len(TOKEN) if TOKEN else 0}")

if not TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN not found!")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the bot."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! 🧮\n\n"
        "I'm a calculator bot. Send me math expressions!\n\n"
        "Examples: 2+2, 10*5, 100/4, 2**3"
    )

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command."""
    help_text = "📋 Commands:\n/start - Start bot\n/help - This message"
    await update.message.reply_text(help_text)

# Calculate messages
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Calculate math expression."""
    try:
        expr = update.message.text.strip()
        result = eval(expr)
        await update.message.reply_text(f"✅ Result: {result}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# Main function
async def main():
    """Start the bot using polling."""
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))
        
        logger.info("✅ Bot started!")
        await application.run_polling()
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
