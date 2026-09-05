import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import json

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

# Flask app
app = Flask(__name__)
application = None

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

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """Handle webhook updates."""
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        
        # Process update
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(application.process_update(update))
        loop.close()
        
        return 'ok', 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return 'error', 500

# Health check
@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

@app.route('/', methods=['GET'])
def root():
    return 'Bot Running!', 200

# Setup
def setup_bot():
    """Initialize bot."""
    global application
    
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))
    
    logger.info("✅ Bot initialized")

# Main
if __name__ == '__main__':
    if not TOKEN or not WEBHOOK_URL:
        logger.error("❌ Missing TOKEN or WEBHOOK_URL")
        exit(1)
    
    setup_bot()
    
    # Set webhook
    import asyncio
    async def set_webhook():
        await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
        logger.info(f"✅ Webhook set: {WEBHOOK_URL}/webhook")
    
    try:
        asyncio.run(set_webhook())
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    
    logger.info(f"🤖 Starting on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False)
