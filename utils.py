import json
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import List, Dict

class LineupParser(HTMLParser):
    """Simple HTML parser to extract home and away lineups."""
    def __init__(self):
        super().__init__()
        self.current_team = None
        self.players = {"home": [], "away": []}

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            attrs_dict = dict(attrs)
            class_attr = attrs_dict.get("class", "")
            if "team home" in class_attr:
                self.current_team = "home"
            elif "team away" in class_attr:
                self.current_team = "away"

    def handle_endtag(self, tag):
        if tag == "div" and self.current_team is not None:
            self.current_team = None

    def handle_data(self, data):
        if self.current_team:
            text = data.strip()
            if text:
                self.players[self.current_team].append(text)


def parse_lineups(html: str) -> Dict[str, List[str]]:
    parser = LineupParser()
    parser.feed(html)
    return parser.players


def find_missing_players(roster: List[str], lineup: List[str]) -> List[str]:
    """Return players from roster who are not present in lineup."""
    return [p for p in roster if p not in lineup]


def fetch_html(url: str) -> str:
    with urllib.request.urlopen(url) as resp:
        return resp.read().decode("utf-8")


def send_telegram_message(token: str, chat_id: str, text: str) -> None:
    message_url = (
        f"https://api.telegram.org/bot{token}/sendMessage"
        f"?chat_id={chat_id}&text=" + urllib.parse.quote(text)
    )
    with urllib.request.urlopen(message_url) as resp:
        resp.read()


def load_config(path: str) -> dict:
    with open(path) as f:
        return json.load(f)
