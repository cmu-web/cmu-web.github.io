"""Merge the CMU Web projects' galleries into _data/gallery.json.

Each project lists the sites built with it in its docs/gallery.json (the
format is in the Web Kilt's tools/gallery.mjs). This fetches each one, makes
its image addresses absolute against the project's docs site, labels every
entry with its project and writes the merged list, sorted by name, for
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
OUT = Path(__file__).resolve().parent.parent / "_data" / "gallery.json"


def load(repo, branch, local):
    if local:
        return json.loads((Path(local) / repo / "docs" / "gallery.json").read_text())
    # Straight from GitHub, not a CDN, so a pushed change shows on the next build
    url = f"https://raw.githubusercontent.com/cmu-web/{repo}/{branch}/docs/gallery.json"
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


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
            entry = dict(entry, project=label)
            for field in ("image", "zoom"):
                if entry.get(field):
                    entry[field] = urljoin(site, entry[field])
            merged.append(entry)
    merged.sort(key=sort_key)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n")
    print(f"_data/gallery.json: {len(merged)} entries")


main()
