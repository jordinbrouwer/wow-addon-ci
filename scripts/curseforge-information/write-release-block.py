#!/usr/bin/env python3
"""Rewrite the release block in README.md (between the release markers) with the release badges."""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import log  # noqa: E402
from lib.readme import END, START  # noqa: E402


def block(repo, website, project_id):
    owner_repo = repo.removeprefix("https://github.com/")
    badges = []
    if project_id:
        badges += [
            f"[![CurseForge](https://img.shields.io/curseforge/v/{project_id}?label=CurseForge)]({website})",
            f"[![Downloads](https://img.shields.io/curseforge/dt/{project_id}?label=downloads)]({website})",
        ]
    badges.append(f"[![GitHub release](https://img.shields.io/github/v/release/{owner_repo}?label=GitHub)]({repo}/releases/latest)")
    return f"{START}\n{' '.join(badges)}\n{END}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="https://github.com/<owner>/<repo>")
    parser.add_argument("--website", required=True, help="CurseForge project page")
    parser.add_argument("--project-id", default="", help="CurseForge project ID, for the badges")
    parser.add_argument("--readme", default="README.md")
    args = parser.parse_args()

    with open(args.readme, encoding="utf-8") as f:
        readme = f.read()
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(readme):
        log.fail(f"{args.readme} needs '{START}' and '{END}' lines.")
    new = block(args.repo, args.website, args.project_id)
    readme = pattern.sub(lambda _: new, readme, count=1)
    with open(args.readme, "w", encoding="utf-8") as f:
        f.write(readme)
    log.info(f"Updated the release block in {args.readme}.")


if __name__ == "__main__":
    main()
