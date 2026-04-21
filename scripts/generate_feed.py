import json
import subprocess
from datetime import datetime
from pathlib import Path

PUBLIC_DIR = Path("frontend/app/public")
LATEST_JSON = PUBLIC_DIR / "latest.json"


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


def main() -> None:
    sentence = generate_sentence()
    payload = {
        "kind": "unko",
        "text": sentence,
        "title": "UNKO N2",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "avatar_image": "image/avatar/normal.png",
        "fixed_image": "",
        "links": [],
    }

    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
