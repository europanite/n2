import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PUBLIC_DIR = Path("frontend/app/public")
LATEST_PATH = PUBLIC_DIR / "latest.json"


def generate_sentence() -> str:
    try:
        result = subprocess.run(
            ["python", "scripts/generate_sentence.py"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        text = result.stdout.strip()
        if text:
            return text
    except Exception:
        pass

    return "今日はとても立派なうんこを生成した。"


def main() -> int:
    sentence = generate_sentence()
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    payload = {
        "kind": "unko",
        "text": sentence,
        "tweet": sentence,
        "created_at": now,
        "updated_at": now,
        "avatar_image": "image/avatar/normal.png",
        "image": "image/avatar/normal.png",
        "links": [],
    }

    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
