#!/usr/bin/env python3
"""Update pinned Piper dependencies and bump the Home Assistant app version."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DOCKERFILE = ROOT / "piper_openvino" / "Dockerfile"
CONFIG = ROOT / "piper_openvino" / "config.yaml"
CHANGELOG = ROOT / "piper_openvino" / "CHANGELOG.md"


def read_json(url: str):
    headers = {"Accept": "application/json", "User-Agent": "ha-app-updater"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return json.load(response)


def version_tuple(value: str) -> tuple[int, ...]:
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", value)
    return tuple(map(int, match.groups())) if match else ()


def bump_app_version() -> str:
    text = CONFIG.read_text(encoding="utf-8")
    match = re.search(r"^version:\s*(\d+)\.(\d+)\.(\d+)\s*$", text, re.MULTILINE)
    if not match:
        raise RuntimeError("Could not find app version in config.yaml")
    version = f"{match.group(1)}.{match.group(2)}.{int(match.group(3)) + 1}"
    CONFIG.write_text(text[: match.start()] + f"version: {version}" + text[match.end() :], encoding="utf-8")
    return version


dockerfile = DOCKERFILE.read_text(encoding="utf-8")
changes: list[str] = []

tags = read_json("https://api.github.com/repos/OHF-Voice/wyoming-piper/tags?per_page=100")
stable_tags = [item["name"] for item in tags if version_tuple(item["name"])]
latest_piper = max(stable_tags, key=version_tuple).lstrip("v")
current_piper = re.search(r"^ARG WYOMING_PIPER_VERSION=(\S+)$", dockerfile, re.MULTILINE).group(1)
if version_tuple(latest_piper) > version_tuple(current_piper):
    dockerfile = dockerfile.replace(
        f"ARG WYOMING_PIPER_VERSION={current_piper}", f"ARG WYOMING_PIPER_VERSION={latest_piper}"
    )
    changes.append(f"wyoming-piper {current_piper} -> {latest_piper}")

latest_ort = read_json("https://pypi.org/pypi/onnxruntime-openvino/json")["info"]["version"]
current_ort = re.search(r"onnxruntime-openvino==(\S+)", dockerfile).group(1)
if version_tuple(latest_ort) > version_tuple(current_ort):
    dockerfile = dockerfile.replace(
        f"onnxruntime-openvino=={current_ort}", f"onnxruntime-openvino=={latest_ort}"
    )
    changes.append(f"onnxruntime-openvino {current_ort} -> {latest_ort}")

if changes:
    DOCKERFILE.write_text(dockerfile, encoding="utf-8")
    version = bump_app_version()
    changelog = CHANGELOG.read_text(encoding="utf-8")
    entry = f"\n## {version}\n\n" + "\n".join(f"- {change}." for change in changes) + "\n"
    CHANGELOG.write_text(changelog.replace("# Changelog\n", "# Changelog\n" + entry, 1), encoding="utf-8")
else:
    version = re.search(r"^version:\s*(\S+)$", CONFIG.read_text(encoding="utf-8"), re.MULTILINE).group(1)

output = os.environ.get("GITHUB_OUTPUT")
if output:
    with open(output, "a", encoding="utf-8") as handle:
        handle.write(f"changed={'true' if changes else 'false'}\n")
        handle.write(f"version={version}\n")

print("; ".join(changes) if changes else "Pinned upstream releases are current.")
