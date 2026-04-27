#!/usr/bin/env python3
import os
import random
import sys
import urllib.request
from pathlib import Path


def main() -> int:
    topic = os.environ.get("NTFY_TOPIC")
    if not topic:
        print("NTFY_TOPIC environment variable is required", file=sys.stderr)
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

    message = random.choice(lines)
    server = os.environ.get("NTFY_SERVER", "https://ntfy.sh").rstrip("/")
    url = f"{server}/{topic}"

    headers = {
        "Title": "Good morning",
        "Tags": "sunrise,sparkles",
        "Priority": "default",
        "Content-Type": "text/plain; charset=utf-8",
    }
    token = os.environ.get("NTFY_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(
        url,
        data=message.encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        if resp.status >= 300:
            print(f"ntfy returned status {resp.status}", file=sys.stderr)
            return 1

    print(f"Sent affirmation: {message}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
