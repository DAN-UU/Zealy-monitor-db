import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(message: str) -> bool:
    """Send a message via Telegram Bot API."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️  Telegram credentials missing. Message would be:")
        print(message)
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")
        return False


def notify_new_sprint(sprint: dict, subdomain: str) -> bool:
    name = sprint.get("name") or "Unnamed Sprint"
    sprint_id = sprint.get("id", "")
    starting = sprint.get("startingAt", "N/A")
    ending = sprint.get("endingAt", "N/A")

    message = (
        f"🚀 <b>New Sprint Started!</b>\n\n"
        f"<b>{name}</b>\n"
        f"ID: <code>{sprint_id}</code>\n"
        f"Starts: {starting}\n"
        f"Ends: {ending}\n\n"
        f"👉 <a href='https://zealy.io/cw/{subdomain}'>Open Community</a>"
    )
    return send_telegram(message)


def notify_new_quest(quest: dict, subdomain: str) -> bool:
    name = quest.get("name") or "Unnamed Quest"
    quest_id = quest.get("id", "")
    published = quest.get("published", False)

    message = (
        f"🎯 <b>New Quest Published!</b>\n\n"
        f"<b>{name}</b>\n"
        f"ID: <code>{quest_id}</code>\n"
        f"Published: {published}\n\n"
        f"👉 <a href='https://zealy.io/cw/{subdomain}'>Open Community</a>"
    )
    return send_telegram(message)
