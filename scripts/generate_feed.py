import json
import subprocess
from datetime import datetime
from pathlib import Path


PUBLIC_DIR = Path("frontend/app/public")
LATEST_JSON = PUBLIC_DIR / "latest.json"
INDEX_HTML = PUBLIC_DIR / "index.html"
NOJEKYLL = PUBLIC_DIR / ".nojekyll"


def generate_sentence():
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


def main():
    sentence = generate_sentence()

    payload = {
        "title": "Unko Sentence",
        "body": sentence,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "image": "/image/avatar/normal.png",
    }

    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    INDEX_HTML.write_text(
        f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>UNKO N2</title>
  <style>
    body {{
      font-family: sans-serif;
      margin: 0;
      background: #f5f7fb;
      color: #1f2937;
    }}
    .wrap {{
      max-width: 720px;
      margin: 40px auto;
      padding: 24px;
    }}
    .card {{
      background: white;
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    }}
    .row {{
      display: flex;
      gap: 16px;
      align-items: center;
    }}
    img {{
      width: 96px;
      height: 96px;
      object-fit: contain;
      border-radius: 12px;
      background: #fff;
    }}
    .title {{
      font-size: 28px;
      font-weight: 700;
      margin-bottom: 16px;
    }}
    .body {{
      font-size: 20px;
      line-height: 1.7;
      margin-top: 16px;
      white-space: pre-wrap;
    }}
    .meta {{
      color: #6b7280;
      font-size: 14px;
      margin-top: 12px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="title">UNKO N2</div>
    <div class="card">
      <div class="row">
        <img src="./image/avatar/normal.png" alt="avatar">
        <div>
          <div><strong>{payload["title"]}</strong></div>
          <div class="meta">{payload["created_at"]}</div>
        </div>
      </div>
      <div class="body">{payload["body"]}</div>
    </div>
  </div>
</body>
</html>
""",
        encoding="utf-8",
    )

    NOJEKYLL.write_text("", encoding="utf-8")


if __name__ == "__main__":
    main()