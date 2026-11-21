"""Merge the CMU Web projects' galleries into _data/gallery.json.

Each project lists the sites built with it in its docs/gallery.json (the
format is in the Web Kilt's tools/gallery.mjs). This fetches each one, makes
its image addresses absolute against the project's docs site, gives each
pill its classes and tooltip, and writes the merged list, sorted by name, for
gallery.html. A project whose file can't be read is skipped with a warning,
so one missing file never empties the gallery.

    python3 tools/gallery.py              fetch from GitHub
    python3 tools/gallery.py --local ..   read sibling checkouts instead
"""

import json
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

# Label, repository, branch, and the docs site its image paths are relative to
SOURCES = [
    ("Web Kilt", "cmu-web-kilt", "0.x", "https://webkilt.andrew.cmu.edu/0/"),
    (
        "Jekyll & Plaid",
        "cmu-web-jekyll-and-plaid",
        "0.x",
        "https://themes.andrew.cmu.edu/jekyll-and-plaid/0/",
    ),
    (
        "Forbes & Moreword",
        "cmu-web-forbes-and-moreword",
        "0.x",
        "https://themes.andrew.cmu.edu/forbes-and-moreword/0/",
    ),
]
# Every pill a card can have, with its classes and tooltip. Mirrors PILLS in
# the Web Kilt's tools/gallery.mjs, which checks each project's file.
PILLS = {
    "CMS": ("cmu-pill cmu-pill--blue", "A content site"),
    "App": ("cmu-pill cmu-pill--green", "A web app"),
    "Cascade": ("cmu-pill cmu-pill--outline", "Built in Cascade"),
    "HTML": ("cmu-pill cmu-pill--outline", "Hand-written HTML pages"),
    "Jekyll": ("cmu-pill cmu-pill--outline", "Built with Jekyll on GitHub Pages"),
    "Node": ("cmu-pill cmu-pill--outline", "A Node app"),
    "Rails": ("cmu-pill cmu-pill--outline", "A Ruby on Rails app"),
    "WordPress": ("cmu-pill cmu-pill--outline", "Built in WordPress"),
}
OUT = Path(__file__).resolve().parent.parent / "_data" / "gallery.json"


def checkout(local, repo):
    """A sibling checkout, or one in the themes folder beside them"""
    for path in (Path(local) / repo, Path(local) / "themes" / repo):
        if path.is_dir():
            return path
    return Path(local) / repo


def load(repo, branch, local):
    if local:
        return json.loads((checkout(local, repo) / "docs" / "gallery.json").read_text())
    # Straight from GitHub, not a CDN, so a pushed change shows on the next build
    url = f"https://raw.githubusercontent.com/cmu-web/{repo}/{branch}/docs/gallery.json"
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def pills(entry, repo):
    """The entry's pills with their classes and tooltips; unknown ones dropped."""
    known = []
    for name in entry.get("pills", []):
        if name not in PILLS:
            print(
                f"warning: {repo}: {entry.get('id')}: no pill named {name}",
                file=sys.stderr,
            )
            continue
        cls, title = PILLS[name]
        known.append({"name": name, "class": cls, "title": title})
    return known


def sort_key(entry):
    name = entry["name"].lower()
    return name.removeprefix("the ")


def main():
    local = sys.argv[sys.argv.index("--local") + 1] if "--local" in sys.argv else None
    merged = []
    for label, repo, branch, site in SOURCES:
        try:
            entries = load(repo, branch, local)
        except Exception as error:  # noqa: BLE001 - any failure skips the project
            print(f"warning: skipped {repo}: {error}", file=sys.stderr)
            continue
        for entry in entries:
            entry = dict(entry, project=label, pills=pills(entry, repo))
            for field in ("image", "zoom"):
                if entry.get(field):
                    entry[field] = urljoin(site, entry[field])
            merged.append(entry)
    merged.sort(key=sort_key)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n")
    print(f"_data/gallery.json: {len(merged)} entries")


main()
