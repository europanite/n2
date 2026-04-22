from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROMPT_PATH = PROJECT_ROOT / "local" / "prompt.txt"


def load_settings() -> dict[str, str | int]:
    load_dotenv(PROJECT_ROOT / ".env")
    return {
        "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "ollama_model": os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
        "prompt_path": os.getenv("PROMPT_PATH", str(DEFAULT_PROMPT_PATH)),
        "max_retries": int(os.getenv("MAX_RETRIES", "3")),
        "request_timeout": int(os.getenv("REQUEST_TIMEOUT", "120")),
    }


def load_prompt(prompt_path: str) -> str:
    path = Path(prompt_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.read_text(encoding="utf-8").strip()


def generate_once(base_url: str, model: str, prompt: str, timeout: int) -> str:
    response = requests.post(
        f"{base_url.rstrip('/')}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
            },
        },
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    return str(data.get("response", "")).strip()


def normalize_output(text: str) -> str:
    text = text.strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " ".join(lines)


def is_valid_sentence(text: str) -> bool:
    if not text:
        return False
    if "うんこ" not in text:
        return False
    if len(text) < 12:
        return False

    forbidden_prefixes = (
        "例文",
        "説明",
        "解説",
        "出力",
        "以下",
    )
    if text.startswith(forbidden_prefixes):
        return False

    sentence_endings = "。！？"
    ending_count = sum(text.count(mark) for mark in sentence_endings)
    if ending_count == 0:
        return False
    if ending_count > 1:
        return False

    banned_fragments = (
        "箇条書き",
        "説明します",
        "次の文",
        "この例文",
    )
    if any(fragment in text for fragment in banned_fragments):
        return False

    return True


def extract_json_payload(raw: str) -> dict[str, str]:
    normalized = normalize_output(raw)

    try:
        data = json.loads(normalized)
    except json.JSONDecodeError as exc:
        raise ValueError(f"output is not valid JSON: {normalized}") from exc

    if not isinstance(data, dict):
        raise ValueError("output JSON must be an object")

    text = str(data.get("text", "")).strip()
    study_point = str(data.get("study_point", "")).strip()
    translation_en = str(data.get("translation_en", "")).strip()

    if not is_valid_sentence(text):
        raise ValueError(f"invalid text field: {text}")

    if not study_point:
        raise ValueError("study_point is empty")

    if not translation_en:
        raise ValueError("translation_en is empty")

    return {
        "text": text,
        "study_point": study_point,
        "translation_en": translation_en,
    }


def main() -> int:
    settings = load_settings()
    prompt = load_prompt(str(settings["prompt_path"]))

    last_output = ""
    for attempt in range(1, int(settings["max_retries"]) + 1):
        try:
            raw = generate_once(
                base_url=str(settings["ollama_base_url"]),
                model=str(settings["ollama_model"]),
                prompt=prompt,
                timeout=int(settings["request_timeout"]),
            )
            last_output = normalize_output(raw)
            payload = extract_json_payload(raw)
            print(json.dumps(payload, ensure_ascii=False))
            return 0

        except (requests.RequestException, ValueError) as exc:
            print(f"[retry {attempt}] invalid output: {last_output or exc}", file=sys.stderr)

    print("Failed to generate a valid sentence JSON.", file=sys.stderr)
    if last_output:
        print(f"Last output: {last_output}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
