import os
import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

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
        "Examples: 2+2, 10*5, 100/4, 2**3\n\n"
        "Use /help for commands."
    )

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command."""
    help_text = "📋 Commands:\n/start - Start bot\n/help - This message\n\n💡 Send any math expression!"
    await update.message.reply_text(help_text)

# Calculate messages
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Calculate math expression."""
    try:
        expr = update.message.text.strip()
        allowed = set('0123456789+-*/.() ')
        
        if not all(c in allowed for c in expr):
            await update.message.reply_text("❌ Invalid! Use: 0-9, +, -, *, /, (), .")
            return
        
        result = eval(expr)
        await update.message.reply_text(f"✅ {expr} = {result}")
    except ZeroDivisionError:
        await update.message.reply_text("❌ Division by zero!")
    except SyntaxError:
        await update.message.reply_text("❌ Invalid syntax!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# Main function
async def main():
    """Start the bot using polling."""
    
    if not TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN not found in environment variables!")
        logger.error("Please set TELEGRAM_BOT_TOKEN in your .env file")
        return
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))
    
    logger.info("✅ Bot handlers registered")
    logger.info("🤖 Bot starting with polling mode...")
    logger.info("🔄 Polling updates from Telegram...")
    
    # Start polling
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

# Entry point
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
