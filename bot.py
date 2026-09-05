import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = int(os.getenv('PORT', 10000))

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app for webhook
app = Flask(__name__)

# Global application variable
application = None

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! 🧮\n\n"
        "I'm a calculator bot. Send me math expressions and I'll solve them!\n\n"
        "Examples:\n"
        "• 2 + 2\n"
        "• 10 * 5\n"
        "• 100 / 4\n"
        "• 2 ** 3 (power)\n\n"
        "Use /help for more commands."
    )

# Help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
    📋 Available Commands:
    /start - Start the bot
    /help - Show this help message
    
    💡 Just send any math expression and I'll calculate it!
    """
    await update.message.reply_text(help_text)

# Message handler for calculations
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Calculate the expression sent by the user."""
    try:
        expression = update.message.text.strip()
        
        # Simple validation - only allow numbers and basic operators
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            await update.message.reply_text("❌ Invalid characters. Use only: 0-9, +, -, *, /, (), .")
            return
        
        # Evaluate the expression
        result = eval(expression)
        await update.message.reply_text(f"✅ {expression} = {result}")
    
    except ZeroDivisionError:
        await update.message.reply_text("❌ Error: Division by zero!")
    except SyntaxError:
        await update.message.reply_text("❌ Error: Invalid expression syntax!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

# Webhook route for Telegram updates
@app.route('/webhook', methods=['POST'])
async def webhook():
    """Handle incoming Telegram updates via webhook."""
    try:
        json_data = request.get_json(force=True)
        update = Update.de_json(json_data, application.bot)
        await application.process_update(update)
        return 'ok', 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return 'error', 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Render."""
    return 'OK', 200

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    """Root endpoint."""
    return 'Telegram Calculator Bot is running!', 200

async def main():
    """Start the bot."""
    global application
    
    # Create application
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))

    logger.info("✅ Bot handlers registered")
    
    # Set webhook
    try:
        webhook_url = f"{WEBHOOK_URL}/webhook"
        await application.bot.set_webhook(webhook_url)
        logger.info(f"✅ Webhook set to {webhook_url}")
    except Exception as e:
        logger.error(f"❌ Webhook setup error: {e}")

# Main entry point
if __name__ == '__main__':
    if not TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN not found in environment variables")
        exit(1)
    
    if not WEBHOOK_URL:
        logger.error("❌ WEBHOOK_URL not found in environment variables")
        exit(1)
    
    # Setup bot
    asyncio.run(main())
    
    logger.info(f"🤖 Bot server starting on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
