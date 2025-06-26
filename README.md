# livescorebot

This repository contains a minimal Telegram bot that monitors basketball games for lineup changes.
It periodically fetches configured game URLs, checks the published lineups and compares them with the
expected rosters. If players are missing, the bot sends an alert message.

## Configuration

Edit `config.json` and provide your Telegram bot token, target chat ID and the list of games to
monitor. Example:

```json
{
  "telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
  "telegram_chat_id": "YOUR_CHAT_ID",
  "scan_interval_minutes": 5,
  "games": [
    {
      "home_team": "Olympiacos",
      "away_team": "Panathinaikos",
      "start_time": "2025-06-30T20:30:00+03:00",
      "url": "http://example.com/game1",
      "rosters": {
        "home": ["Walkup", "PlayerB1", "PlayerB2"],
        "away": ["Sloukas", "PlayerC1", "PlayerC2"]
      }
    }
  ]
}
```

## Running the bot

Install the required dependencies (requests and beautifulsoup are not used so only the Python
standard library is required) and run:

```bash
python3 bot.py
```

## Testing

Run unit tests with:

```bash
pytest
```
