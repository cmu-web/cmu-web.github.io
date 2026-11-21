"""List the CMU Web projects in _data/projects.json, from their repositories.

Each project describes itself; there is no list to edit by hand. A public
repository in the cmu-web organization is listed when it has exactly one of
the topics in KINDS. Its name is the README's first heading, its sentence is
the repository's description and its address is the repository's website, all
on GitHub. Its picture is the card screenshot (cmu-web-preview.webp) beside the
README's image, which the Update Preview Images workflow keeps current, or the
README's image itself. A repository that can't be read is skipped with a
warning, so one problem never empties the list.

The home page, the Themes page and every project's More From CMU Web section
(js/more-from-cmu-web.js, through /projects.json) show this list.

    python3 tools/projects.py                  fetch from GitHub
    python3 tools/projects.py --local ..       read READMEs from sibling checkouts
    python3 tools/projects.py --profile PATH   also rewrite the org profile's table

GITHUB_TOKEN, when set (as in Actions), raises GitHub's rate limit.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ORG = "cmu-web"
# The topics that list a project, with its kind. Only these exact topics count:
# cmu-web-tool-addon marks a part of another project, reached from that project.
KINDS = {
    "cmu-web-tool": "tool",
    "cmu-web-theme-site": "theme-site",
    "cmu-web-theme-app": "theme-app",
    "cmu-web-theme-document": "theme-document",
}
# A theme's eyebrow: Site, App or Document, then its platform, from these
# topics
PLATFORMS = {
    "jekyll-theme": "Jekyll",
    "wordpress-theme": "WordPress",
    "mkdocs-theme": "MkDocs",
    "forgejo": "Forgejo",
    "vaultwarden": "Vaultwarden",
    "mediawiki": "MediaWiki",
    "hugo-theme": "Hugo",
    "quarto": "Quarto",
    "grouper": "Grouper",
}
PLACEHOLDER = "https://placemellon.andrew.cmu.edu/1040/656.svg?solid&text"
# Temporary: projects without a public repository yet, so their cards can show
# before their first push. Remove each one when its repository is public.
COMING = [
    {
        "repo": "cmu-web-cut-list",
        "name": "The Cut List",
        "description": (
            "Banners, headers and icons for the tools you use at CMU, "
            "sized and cropped in CMU style."
        ),
        "url": "https://cutlist.andrew.cmu.edu/",
        "kind": "tool",
        "eyebrow": "",
        "image": PLACEHOLDER,
        "alt": "Placeholder for The Cut List's home page.",
        "repository": "",
    },
    {
        "repo": "cmu-web-docs-and-donner",
        "name": "Docs & Donner",
        "description": "An MkDocs theme in CMU style, for docs written in Markdown.",
        "url": "https://themes.andrew.cmu.edu/docs-and-donner/",
        "kind": "theme-site",
        "eyebrow": "Site · MkDocs",
        "image": PLACEHOLDER,
        "alt": "Placeholder for Docs & Donner's home page.",
        "repository": "",
    },
    {
        "repo": "cmu-web-scaife-and-sound",
        "name": "Scaife & Sound",
        "description": "A Vaultwarden theme in CMU style, for its web vault.",
        "url": "https://themes.andrew.cmu.edu/scaife-and-sound/",
        "kind": "theme-app",
        "eyebrow": "App · Vaultwarden",
        "image": PLACEHOLDER,
        "alt": "Placeholder for Scaife & Sound's home page.",
        "repository": "",
    },
    {
        "repo": "cmu-web-tech-and-type",
        "name": "Tech & Type",
        "description": "LaTeX and Typst templates in CMU style, for letters and other documents.",
        "url": "https://themes.andrew.cmu.edu/tech-and-type/",
        "kind": "theme-document",
        "eyebrow": "Document · LaTeX and Typst",
        "image": PLACEHOLDER,
        "alt": "Placeholder for Tech & Type's home page.",
        "repository": "",
    },
]
OUT = Path(__file__).resolve().parent.parent / "_data" / "projects.json"


def checkout(local, repo):
    """A sibling checkout, or one in the themes folder beside them"""
    for path in (Path(local) / repo, Path(local) / "themes" / repo):
        if path.is_dir():
            return path
    return Path(local) / repo


def get(url, raw=False):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "cmu-web-projects",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
    return body.decode() if raw else json.loads(body)


def exists(url):
    request = urllib.request.Request(
        url, method="HEAD", headers={"User-Agent": "cmu-web-projects"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status == 200
    except urllib.error.URLError:
        return False


def readme(repo, local):
    if local:
        return (checkout(local, repo["name"]) / "README.md").read_text()
    # Raw files don't count against the API's rate limit
    return get(
        f"https://raw.githubusercontent.com/{ORG}/{repo['name']}/{repo['default_branch']}/README.md",
        raw=True,
    )


def project(repo, local):
    kinds = [KINDS[t] for t in repo["topics"] if t in KINDS]
    if len(kinds) != 1:
        return None
    kind = kinds[0]
    text = readme(repo, local)
    heading = re.search(r"^# (.+)$", text, re.MULTILINE)
    if not heading:
        raise ValueError("its README has no # heading")
    name = heading.group(1).strip()
    if not repo["description"] or not repo["homepage"]:
        raise ValueError("it has no description or website on GitHub")
    raw = f"https://raw.githubusercontent.com/{ORG}/{repo['name']}/{repo['default_branch']}/"
    picture = re.search(r"\]\(((?!https?:)[^)\s]+\.(?:jpg|jpeg|png|webp))\)", text)
    # Until a project's README has a picture, the same placeholder the coming
    # projects use
    image, alt = PLACEHOLDER, f"Placeholder for {name}'s home page."
    if picture:
        card = str(Path(picture.group(1)).parent / "cmu-web-preview.webp")
        image = raw + card if exists(raw + card) else raw + picture.group(1)
        alt = f"{name}'s home page."
    eyebrow = ""
    if kind != "tool":
        platform = next((PLATFORMS[t] for t in repo["topics"] if t in PLATFORMS), "")
        label = {"theme-site": "Site", "theme-app": "App", "theme-document": "Document"}
        eyebrow = " · ".join(filter(None, [label[kind], platform]))
    return {
        "repo": repo["name"],
        "name": name,
        "description": repo["description"],
        "url": repo["homepage"],
        "kind": kind,
        "eyebrow": eyebrow,
        "image": image,
        "alt": alt,
        "repository": repo["html_url"],
    }


def sort_key(entry):
    return re.sub(r"^The ", "", entry["name"]).casefold()


def profile_table(projects):
    rows = ["| Project | Repository | What It Does |", "| --- | --- | --- |"]
    for kind in ("tool", "theme-site", "theme-app"):
        for p in projects:
            if p["kind"] == kind and p["repository"]:
                rows.append(
                    f"| [{p['name']}]({p['url']}) | [`{p['repo']}`]({p['repository']}) "
                    f"| {p['description']} |"
                )
    return "\n".join(rows)


def write_profile(path, projects):
    text = Path(path).read_text()
    start, end = "<!-- projects -->", "<!-- /projects -->"
    if start not in text or end not in text:
        sys.exit(f"{path}: no {start} and {end} markers")
    before, rest = text.split(start, 1)
    after = rest.split(end, 1)[1]
    Path(path).write_text(
        f"{before}{start}\n\n{profile_table(projects)}\n\n{end}{after}"
    )
    print(f"{path}: table rewritten; run Prettier on it to align the columns")


def main(args):
    local = args[args.index("--local") + 1] if "--local" in args else None
    repos = get(f"https://api.github.com/orgs/{ORG}/repos?type=public&per_page=100")
    projects = []
    for repo in repos:
        if repo.get("archived") or repo.get("private"):
            continue
        try:
            entry = project(repo, local)
        except (OSError, ValueError) as error:
            print(f"warning: skipped {repo['name']}: {error}", file=sys.stderr)
            continue
        if entry:
            projects.append(entry)
    listed = {p["repo"] for p in projects}
    projects += [p for p in COMING if p["repo"] not in listed]
    projects.sort(key=sort_key)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(projects, indent=2, ensure_ascii=False) + "\n")
    print(f"_data/projects.json: {len(projects)} projects")
    if "--profile" in args:
        write_profile(args[args.index("--profile") + 1], projects)


if __name__ == "__main__":
    main(sys.argv[1:])
