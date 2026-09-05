# 🧮 Telegram Calculator Bot

A simple yet powerful Telegram bot that performs mathematical calculations in real-time.

## Features

- ✅ Basic arithmetic operations (+, -, *, /)
- ✅ Power operations (**)
- ✅ Parentheses support for complex expressions
- ✅ Error handling for invalid inputs
- ✅ User-friendly command interface

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/williamlesch827-alt/telegram-calc.git
cd telegram-calc
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure the bot token**

The `.env` file already contains your bot token. Make sure it's properly configured:
```
TELEGRAM_BOT_TOKEN=your_token_here
```

## Usage

1. **Start the bot**
```bash
python bot.py
```

2. **In Telegram**
   - Find your bot and send `/start`
   - Send any math expression (e.g., `2 + 2`, `10 * 5`, `100 / 4`)
   - The bot will calculate and return the result

## Examples

- `2 + 2` → `4`
- `10 * 5` → `50`
- `100 / 4` → `25`
- `2 ** 3` → `8` (2 to the power of 3)
- `(10 + 5) * 2` → `30`

## Commands

- `/start` - Start the bot and see welcome message
- `/help` - Display help information

## Security Note

⚠️ **Important**: Never commit the `.env` file with your bot token to a public repository!
- Add `.env` to `.gitignore` before pushing to GitHub
- Always use environment variables for sensitive data

## Development

To extend the bot with more features:

1. Edit `bot.py`
2. Add new handlers or modify existing ones
3. Test locally before deploying

## License

This project is open source and available under the MIT License.

## Support

For issues or feature requests, please open an issue on GitHub.
