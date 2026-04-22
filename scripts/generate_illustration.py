import argparse
import base64
import os
from pathlib import Path

import requests


def build_prompt(sentence: str) -> str:
    return (
        "Create a clean, friendly illustration that matches this Japanese text exactly. "
        "No letters, no captions, no watermark. "
        "Bright background, simple composition, cute character design. "
        f"Text meaning: {sentence}"
    )


def generate_image(prompt: str, output_path: Path) -> None:
    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required")

    model = (os.getenv("OPENAI_IMAGE_MODEL") or "gpt-image-1").strip()
    size = (os.getenv("OPENAI_IMAGE_SIZE") or "1024x1024").strip()

    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "prompt": prompt,
            "size": size,
        },
        timeout=180,
    )
    response.raise_for_status()
    payload = response.json()
    data = payload.get("data") or []
    if not data:
        raise SystemExit("image API returned no data")

    image_base64 = data[0].get("b64_json")
    if not image_base64:
        raise SystemExit("image API did not return b64_json")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(base64.b64decode(image_base64))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("sentence")
    parser.add_argument("output_path")
    args = parser.parse_args()

    prompt = build_prompt(args.sentence)
    generate_image(prompt, Path(args.output_path))
    print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
