#!/usr/bin/env python3
"""Export README resource bullets to a small machine-readable JSON index."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
OUTPUT = ROOT / "resources.json"

HEADING_RE = re.compile(r"^## (?P<title>.+)$")
RESOURCE_RE = re.compile(r"^- \[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\)(?: - (?P<description>.*))?$")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def main() -> int:
    sections: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for line in README.read_text(encoding="utf-8").splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            title = heading.group("title")
            if title == "Contents":
                current = None
            else:
                current = {"id": slugify(title), "title": title, "resources": []}
                sections.append(current)
            continue

        resource = RESOURCE_RE.match(line)
        if current is None or resource is None:
            continue

        resources = current["resources"]
        assert isinstance(resources, list)
        resources.append(
            {
                "name": resource.group("name"),
                "url": resource.group("url"),
                "description": resource.group("description") or "",
            }
        )

    payload = {
        "schema_version": "1.0",
        "name": "Awesome GEO",
        "repository_url": "https://github.com/trakkr-aisearch/awesome-geo",
        "license": "CC0-1.0",
        "maintainer": {
            "name": "Trakkr",
            "url": "https://trakkr.ai",
        },
        "source": "README.md",
        "sections": [
            section for section in sections if section.get("resources")
        ],
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
