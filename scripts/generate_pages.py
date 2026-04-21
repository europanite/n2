import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PUBLIC_DIR = Path("frontend/app/public")
LATEST_PATH = PUBLIC_DIR / "latest.json"
FEED_DIR = PUBLIC_DIR / "feed"
SNAPSHOT_DIR = PUBLIC_DIR / "snapshot"


def utc_now_iso_z() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def local_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def local_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


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


def build_item(sentence: str) -> dict:
    now = utc_now_iso_z()
    return {
        "id": f"unko-{local_stamp()}",
        "date": local_date(),
        "text": sentence,
        "place": "N2",
        "kind": "unko",
        "avatar_image": "image/avatar/normal.png",
        "generated_at": now,
        "image": "image/avatar/normal.png",
        "links": [],
    }


def main() -> int:
    sentence = generate_sentence()
    item = build_item(sentence)

    latest = {
        "updated_at": utc_now_iso_z(),
        "place": "N2",
        "items": [item],
    }

    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    FEED_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    LATEST_PATH.write_text(
        json.dumps(latest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    (FEED_DIR / f"feed_{local_stamp()}.json").write_text(
        json.dumps(latest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    (SNAPSHOT_DIR / "latest_weather.json").write_text(
        json.dumps(
            {
                "ok": True,
                "source": "generate_pages.py",
                "generated_at": utc_now_iso_z(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(json.dumps(latest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())