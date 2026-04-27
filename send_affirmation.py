#!/usr/bin/env python3
import json
import os
import random
import sys
import urllib.request
from html import escape
from pathlib import Path


def main() -> int:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print(
            "TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required",
            file=sys.stderr,
        )
        return 1

    affirmations_path = Path(__file__).resolve().parent / "affirmations.txt"
    lines = [
        line.strip()
        for line in affirmations_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not lines:
        print("No affirmations found in affirmations.txt", file=sys.stderr)
        return 1

    line = random.choice(lines)
    if " — " in line:
        quote, _, author = line.partition(" — ")
        text = f"<i>{escape(quote)}</i>\n\n— <b>{escape(author)}</b>"
    else:
        text = escape(line)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps(
        {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode("utf-8")
        if resp.status >= 300:
            print(
                f"Telegram returned status {resp.status}: {body}",
                file=sys.stderr,
            )
            return 1

    print(f"Sent: {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
