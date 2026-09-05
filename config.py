import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Bot token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Validate token
if not TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN not found!")
    print("Loading token from .env file...")
    import sys
    sys.exit(1)

print(f"✅ Token loaded: {TOKEN[:20]}...")
