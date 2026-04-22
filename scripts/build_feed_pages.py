#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def extract_items(path: Path) -> list[dict[str, Any]]:
    try:
        obj = load_json(path)
    except Exception:
        return []

    if isinstance(obj, dict):
        items = obj.get("items")
        if isinstance(items, list):
            return [it for it in items if isinstance(it, dict)]
        return [obj]

    if isinstance(obj, list):
        return [it for it in obj if isinstance(it, dict)]

    return []


def sort_key(it: dict[str, Any]) -> tuple[str, str]:
    primary = str(
        it.get("created_at")
        or it.get("generated_at")
        or it.get("published_at")
        or it.get("date")
        or ""
    )
    return (primary, str(it.get("id") or ""))


def normalize_permalink(item: dict[str, Any], base_url: str) -> None:
    pid = str(item.get("id") or "").strip()
    if not pid:
        return
    base = base_url.rstrip("/")
    if base == ".":
        item["permalink"] = f"./posts/{pid}/index.html"
    else:
        item["permalink"] = f"{base}/posts/{pid}/index.html"


def render_post_html(item: dict[str, Any]) -> str:
    title = html.escape(str(item.get("kind") or "post"))
    text = html.escape(str(item.get("text") or item.get("tweet") or ""))
    image = str(item.get("image") or "").strip()
    image_html = (
        f'<p><img src="../../{html.escape(image)}" alt="" style="max-width:100%;height:auto;" /></p>'
        if image
        else ""
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{title}</title>
</head>
<body>
  <main style="max-width:720px;margin:40px auto;padding:0 16px;font-family:sans-serif;line-height:1.6;">
    <p><a href="../../index.html">← Back</a></p>
    <h1>{title}</h1>
    {image_html}
    <p>{text}</p>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-dir", default="frontend/app/public")
    parser.add_argument("--base-url", default=".")
    args = parser.parse_args()

    public_dir = Path(args.public_dir)
    feed_dir = public_dir / "feed"
    latest_path = public_dir / "latest.json"
    posts_dir = public_dir / "posts"

    feed_dir.mkdir(parents=True, exist_ok=True)
    posts_dir.mkdir(parents=True, exist_ok=True)

    all_items: list[dict[str, Any]] = []
    for path in sorted(feed_dir.glob("feed_*.json")):
        all_items.extend(extract_items(path))

    for item in all_items:
        normalize_permalink(item, args.base_url)

    all_items.sort(key=sort_key, reverse=True)

    write_json(
        feed_dir / "index.json",
        {
            "updated_at": all_items[0].get("created_at", "") if all_items else "",
            "items": all_items,
        },
    )

    write_json(latest_path, all_items[0] if all_items else {})

    for item in all_items:
        pid = str(item.get("id") or "").strip()
        if not pid:
            continue
        out = posts_dir / pid / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_post_html(item), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())