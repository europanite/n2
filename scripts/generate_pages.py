from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIR = ROOT / "frontend" / "app" / "public"
LATEST_PATH = PUBLIC_DIR / "latest.json"
INDEX_PATH = PUBLIC_DIR / "index.html"
NOJEKYLL_PATH = PUBLIC_DIR / ".nojekyll"
AVATAR_PATH = "image/avatar/normal.png"


def generate_sentence() -> str:
    script = ROOT / "scripts" / "generate_sentence.py"
    if script.exists():
        try:
            proc = subprocess.run(
                ["python", str(script)],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=ROOT,
                check=False,
            )
            text = (proc.stdout or "").strip()
            if text:
                return text.splitlines()[0].strip()
        except Exception:
            pass
    return "今日はとても立派なうんこを生成した。"


def build_payload(text: str) -> dict:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    return {
        "kind": "unko",
        "text": text,
        "avatar_image": AVATAR_PATH,
        "fixed_image": "",
        "links": [],
        "place": "Unko",
        "published_at": now.isoformat().replace("+00:00", "Z"),
    }


def write_index(payload: dict) -> None:
    text = escape(payload["text"])
    published_at = escape(payload["published_at"])
    avatar = escape(payload["avatar_image"])
    html = f"""<!doctype html>
<html lang=\"ja\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Unko Feed</title>
    <style>
      body {{ font-family: sans-serif; margin: 0; background: #f7f3ee; color: #2b2118; }}
      main {{ max-width: 720px; margin: 0 auto; padding: 24px 16px 48px; }}
      .card {{ background: #fff; border-radius: 16px; padding: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.08); }}
      .header {{ display: flex; gap: 12px; align-items: center; margin-bottom: 16px; }}
      .avatar {{ width: 72px; height: 72px; object-fit: cover; border-radius: 999px; background: #f0e4d6; }}
      .title {{ font-size: 24px; font-weight: 700; margin: 0; }}
      .meta {{ margin: 4px 0 0; color: #6b5a4b; font-size: 14px; }}
      .text {{ font-size: 28px; line-height: 1.6; margin: 16px 0 0; word-break: break-word; }}
      .footer {{ margin-top: 24px; font-size: 14px; color: #6b5a4b; }}
      a {{ color: inherit; }}
    </style>
  </head>
  <body>
    <main>
      <div class=\"card\">
        <div class=\"header\">
          <img class=\"avatar\" src=\"{avatar}\" alt=\"avatar\" />
          <div>
            <h1 class=\"title\">Unko Feed</h1>
            <p class=\"meta\">{published_at}</p>
          </div>
        </div>
        <p class=\"text\">{text}</p>
        <p class=\"footer\"><a href=\"./latest.json\">latest.json</a></p>
      </div>
    </main>
  </body>
</html>
"""
    INDEX_PATH.write_text(html, encoding="utf-8")


def main() -> None:
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    text = generate_sentence()
    payload = build_payload(text)
    LATEST_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_index(payload)
    NOJEKYLL_PATH.write_text("\n", encoding="utf-8")


if __name__ == "__main__":
    main()
