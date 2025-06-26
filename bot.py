import time
from datetime import datetime, timedelta
from typing import Dict, List

from utils import (
    fetch_html,
    parse_lineups,
    find_missing_players,
    send_telegram_message,
    load_config,
)


def process_game(game: Dict[str, any], token: str, chat_id: str) -> None:
    start_time = datetime.fromisoformat(game["start_time"])
    now = datetime.now(start_time.tzinfo)
    if now > start_time:
        return
    if start_time - now > timedelta(minutes=90):
        return

    try:
        html = fetch_html(game["url"])
    except Exception as exc:
        print(f"Failed to fetch {game['url']}: {exc}")
        return

    lineups = parse_lineups(html)
    home_roster = game["rosters"]["home"]
    away_roster = game["rosters"]["away"]

    missing_home = find_missing_players(home_roster, lineups.get("home", []))
    missing_away = find_missing_players(away_roster, lineups.get("away", []))

    if missing_home or missing_away:
        msg_lines = [
            "\ud83d\udea8 Missing Players Alert",
            f"Game: {game['home_team']} vs {game['away_team']}",
            f"Time: {start_time.strftime('%H:%M %Z')}",
        ]
        if missing_home:
            msg_lines.append(
                f"Missing {game['home_team']}: " + ", ".join(missing_home)
            )
        if missing_away:
            msg_lines.append(
                f"Missing {game['away_team']}: " + ", ".join(missing_away)
            )
        message = "\n".join(msg_lines)
        try:
            send_telegram_message(token, chat_id, message)
        except Exception as exc:
            print(f"Failed to send message: {exc}")


def main():
    cfg = load_config("config.json")
    token = cfg["telegram_bot_token"]
    chat_id = cfg["telegram_chat_id"]
    interval = cfg.get("scan_interval_minutes", 5)
    games = cfg.get("games", [])

    while True:
        for game in games:
            process_game(game, token, chat_id)
        time.sleep(interval * 60)


if __name__ == "__main__":
    main()
