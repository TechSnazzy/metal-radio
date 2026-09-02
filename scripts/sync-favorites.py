#!/usr/bin/env python3
"""Regenerate the STATIONS list in index.html from cliamp's radio favorites.

cliamp stores favorited stations in ~/.config/cliamp/radio_favorites.toml.
Run this after favoriting/unfavoriting stations in cliamp to keep the web app
in sync, then commit and push.

Usage: scripts/sync-favorites.py [path/to/radio_favorites.toml]
"""
import pathlib
import re
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
DEFAULT_FAV = pathlib.Path.home() / ".config" / "cliamp" / "radio_favorites.toml"

# Prefer an HTTPS endpoint when a station offers one; the app is served over
# HTTPS and browsers block mixed (http) media. Keys are matched as substrings
# of the station name.
HTTPS_OVERRIDES = {
    "181.FM":            "https://listen.181fm.com/181-hairband_128k.mp3",
    "Big R Radio":       "https://bigrradio.cdnstream1.com/5186_128",
    "Hard Rock Heaven":  "https://ais-sa2.cdnstream1.com/1521_128",
}


def country_code(name: str) -> str:
    return {
        "United States": "USA", "Germany": "Germany", "Russia": "Russia",
        "United Kingdom": "UK", "Canada": "Canada",
    }.get(name, name)


def main() -> int:
    fav_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FAV
    if not fav_path.exists():
        print(f"not found: {fav_path}", file=sys.stderr)
        return 1

    data = tomllib.loads(fav_path.read_text())
    stations = data.get("station", [])
    if not stations:
        print("no stations in favorites file", file=sys.stderr)
        return 1

    rows = []
    for s in stations:
        name = s["name"].replace(" - ", " — ")
        url = s["url"]
        for key, better in HTTPS_OVERRIDES.items():
            if key in s["name"]:
                url = better
        genre = s.get("codec", "")
        tag = f'{s.get("country", "")}'.strip() or genre
        tag = f'{_genre_hint(s["name"])} · {country_code(s.get("country", ""))}'.strip(" ·")
        rows.append(f'    {{ name: {js(name)}, tag: {js(tag)}, url: {js(url)} }},')

    block = "  const STATIONS = [\n" + "\n".join(rows) + "\n  ];"
    html = INDEX.read_text()
    new = re.sub(r"  const STATIONS = \[.*?\n  \];", block, html, count=1, flags=re.S)
    if new == html:
        print("could not locate STATIONS block in index.html", file=sys.stderr)
        return 1
    INDEX.write_text(new)
    print(f"synced {len(rows)} stations into {INDEX.relative_to(ROOT)}")
    return 0


def _genre_hint(name: str) -> str:
    n = name.lower()
    if "glam" in n:
        return "Glam Metal"
    if "hairband" in n or "hair band" in n:
        return "Hair Band"
    if "hair" in n:
        return "Hair Metal"
    if "hard rock" in n:
        return "Hard Rock"
    if "80s" in n or "80's" in n:
        return "80s Metal"
    return "Metal"


def js(v: str) -> str:
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'


if __name__ == "__main__":
    raise SystemExit(main())
