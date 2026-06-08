#!/usr/bin/env python3
"""Extract and save full-resolution photos from a saved realtor.com listing HTML page."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
    re.S,
)
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def extract_photo_urls(html: str) -> list[str]:
    match = NEXT_DATA_RE.search(html)
    if not match:
        raise RuntimeError("Could not find __NEXT_DATA__ on the page.")

    payload = json.loads(match.group(1))
    details = (
        payload.get("props", {})
        .get("pageProps", {})
        .get("initialReduxState", {})
        .get("propertyDetails", {})
    )
    if not details:
        raise RuntimeError("Could not find propertyDetails in page data.")

    urls: list[str] = []
    for photo in details.get("photos") or []:
        href = photo.get("href")
        if href:
            urls.append(href)

    home_photos = (details.get("home_photos") or {}).get("collection") or []
    for photo in home_photos:
        href = photo.get("href")
        if href:
            urls.append(href)

    seen: set[str] = set()
    unique: list[str] = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique.append(url)

    if not unique:
        raise RuntimeError("No photos found for this listing.")
    return unique


def full_size_url(url: str) -> str:
    url = url.replace("http://", "https://")
    if "rd-w" in url or url.endswith("s.jpg"):
        return re.sub(r"s\.jpg$", "rd-w2048_h1536.jpg", url)
    return url


def download_photo(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        destination.write_bytes(response.read())


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read a saved realtor.com listing HTML page and download "
            "full-resolution photos to a folder."
        )
    )
    parser.add_argument("html", type=Path, help="Saved listing HTML file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output directory for photos (default: photos/)",
    )
    parser.add_argument(
        "--thumb",
        action="store_true",
        help="Download thumbnail URLs instead of 2048px images",
    )
    args = parser.parse_args()

    if not args.html.is_file():
        print(f"File not found: {args.html}", file=sys.stderr)
        return 1

    html = args.html.read_text(encoding="utf-8", errors="replace")

    try:
        photo_urls = extract_photo_urls(html)
    except (RuntimeError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 1

    out_dir = args.output or Path("photos")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Found {len(photo_urls)} photos. Saving to {out_dir}/")

    for index, url in enumerate(photo_urls, start=1):
        download_url = url if args.thumb else full_size_url(url)
        ext = Path(download_url.split("?", 1)[0]).suffix or ".jpg"
        destination = out_dir / f"{index:03d}{ext}"

        try:
            download_photo(download_url, destination)
        except urllib.error.HTTPError:
            if download_url != url:
                download_photo(url, destination)
            else:
                print(f"  [{index}/{len(photo_urls)}] failed: {url}", file=sys.stderr)
                return 1
        except urllib.error.URLError as exc:
            print(f"  [{index}/{len(photo_urls)}] network error: {exc.reason}", file=sys.stderr)
            return 1

        print(f"  [{index}/{len(photo_urls)}] {destination.name}")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
