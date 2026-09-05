import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Bot token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Validate token
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN not found in environment variables!")

print(f"✅ Bot token loaded successfully")
