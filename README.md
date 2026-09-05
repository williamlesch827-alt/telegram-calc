# 🧮 Telegram Calculator Bot - Render Deployment

A simple yet powerful Telegram bot that performs mathematical calculations in real-time, deployed on Render using webhooks.

## Features

- ✅ Basic arithmetic operations (+, -, *, /)
- ✅ Power operations (**)
- ✅ Parentheses support for complex expressions
- ✅ Error handling for invalid inputs
- ✅ Webhook-based deployment (no polling)
- ✅ Render-ready configuration

## Prerequisites

- Python 3.8 or higher
- Render account (free tier works!)
- Telegram Bot Token

## Local Installation & Testing

1. **Clone the repository**
```bash
git clone https://github.com/williamlesch827-alt/telegram-calc.git
cd telegram-calc
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create `.env` file** (for local testing only)
```bash
TELEGRAM_BOT_TOKEN=your_token_here
WEBHOOK_URL=http://localhost:5000
```

4. **Run locally**
```bash
python bot.py
```

## Deployment to Render

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create Render Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Fill in the details:
   - **Name**: `telegram-calc` (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Plan**: Free (recommended for testing)

### Step 3: Set Environment Variables

In Render Dashboard, go to your service → "Environment":

Add these variables:
```
TELEGRAM_BOT_TOKEN = your_bot_token_here
WEBHOOK_URL = https://your-app-name.onrender.com
PORT = 10000
```

⚠️ **Important**: Replace `your-app-name` with your actual Render app name!

### Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically deploy your bot
3. Wait for the build to complete (shows "Live" when ready)
4. Your bot is now running! 🎉

## Usage

### In Telegram
- Find your bot (search by token or bot name)
- Send `/start` to begin
- Send any math expression (e.g., `2 + 2`, `10 * 5`, `100 / 4`)
- The bot will calculate and return the result

### Examples

- `2 + 2` → `4`
- `10 * 5` → `50`
- `100 / 4` → `25`
- `2 ** 3` → `8` (2 to the power of 3)
- `(10 + 5) * 2` → `30`
- `sqrt(16)` → Error (use: 16 ** 0.5)

## Commands

- `/start` - Start the bot and see welcome message
- `/help` - Display help information

## How It Works

### Polling vs Webhook

This bot uses **webhook mode** (better for Render):
- ✅ Uses Flask to receive updates from Telegram
- ✅ No continuous polling (saves resources)
- ✅ Scales well on Render's free tier
- ✅ Instant message processing

## Security Notes

⚠️ **Important**:
- Never commit `.env` with real tokens to public repos (already in `.gitignore`)
- Use Render's Environment Variables for sensitive data
- Keep your bot token private!

## Monitoring

### View Logs in Render
1. Go to your service dashboard
2. Click "Logs" tab
3. See real-time bot activity

### Health Check
The bot has a health endpoint: `https://your-app-name.onrender.com/health`

## Troubleshooting

### Bot not responding?
1. Check if Render service is "Live"
2. Verify `WEBHOOK_URL` matches your Render app URL
3. Check logs in Render dashboard

### Build fails?
- Ensure `requirements.txt` is correct
- Check Python version is 3.8+

### Webhook errors?
- Make sure `WEBHOOK_URL` is set correctly in environment variables
- Restart the service in Render dashboard

## Development

To add more features:

1. Edit `bot.py`
2. Add new handlers
3. Commit and push to GitHub
4. Render auto-deploys on push!

## License

This project is open source and available under the MIT License.

## Support

For issues or feature requests, open an issue on GitHub.

---

**Happy Calculating! 🧮✨**
