import json
import subprocess
from datetime import datetime

def generate_sentence():
    try:
        result = subprocess.run(
            ["python", "scripts/generate_sentence.py"],
            capture_output=True,
            text=True,
            timeout=30
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
        "image": "/image/avatar/unko.png"
    }

    print(json.dumps(payload, ensure_ascii=False))

if __name__ == "__main__":
    main()