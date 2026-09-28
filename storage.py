"""Persistent quest state using Upstash Redis on Vercel."""
import json
import os
from pathlib import Path
from typing import Set

import requests

STORAGE_FILE = Path(__file__).parent / "seen_items.json"
REDIS_URL = os.getenv("KV_REST_API_URL") or os.getenv("UPSTASH_REDIS_REST_URL")
REDIS_TOKEN = os.getenv("KV_REST_API_TOKEN") or os.getenv("UPSTASH_REDIS_REST_TOKEN")
STATE_KEY = os.getenv("ZEALY_STATE_KEY", "zealy-monitor:quests")


def _default_state() -> dict:
    return {"quests": [], "initialized": False}


def _normalize(data: dict) -> dict:
    return {
        "quests": [str(x) for x in data.get("quests", []) if x],
        "initialized": bool(data.get("initialized", False)),
    }


def _redis_command(command: list):
    if not (REDIS_URL and REDIS_TOKEN):
        return None
    response = requests.post(
        REDIS_URL,
        headers={"Authorization": f"Bearer {REDIS_TOKEN}"},
        json=command,
        timeout=10,
    )
    response.raise_for_status()
    return response.json().get("result")


def load_state() -> dict:
    if REDIS_URL and REDIS_TOKEN:
        raw = _redis_command(["GET", STATE_KEY])
        if raw:
            return _normalize(json.loads(raw))
        return _default_state()

    if not STORAGE_FILE.exists():
        return _default_state()
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        return _normalize(json.load(f))


def save_seen_quests(quests: Set[str], initialized: bool = True) -> None:
    data = {
        "quests": sorted(str(x) for x in quests if x),
        "initialized": initialized,
    }
    encoded = json.dumps(data, separators=(",", ":"))
    if REDIS_URL and REDIS_TOKEN:
        _redis_command(["SET", STATE_KEY, encoded])
        return
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_seen_quests() -> tuple[Set[str], bool]:
    data = load_state()
    return set(data["quests"]), data["initialized"]


def using_persistent_storage() -> bool:
    return bool(REDIS_URL and REDIS_TOKEN)
