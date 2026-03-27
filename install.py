#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


OWNER = "Jonnys-Li"
REPO = "software-thesis-docx-skill"
DEFAULT_REF = "main"
DEFAULT_NAME = "software-thesis-docx"
SKILL_SUBPATH = Path("skills/software-thesis-docx")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the software-thesis-docx Codex skill.")
    parser.add_argument("--ref", default=DEFAULT_REF, help="Git ref to install from. Defaults to main.")
    parser.add_argument("--dest", help="Destination skills directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.")
    parser.add_argument("--name", default=DEFAULT_NAME, help="Installed skill directory name.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing installation.")
    return parser.parse_args()


def codex_skills_dir() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()
    return codex_home / "skills"


def destination_dir(dest: str | None, name: str) -> Path:
    base = Path(dest).expanduser() if dest else codex_skills_dir()
    return base / name


def download_repo_zip(ref: str, tmp_dir: Path) -> Path:
    quoted_ref = urllib.parse.quote(ref, safe="")
    url = f"https://codeload.github.com/{OWNER}/{REPO}/zip/{quoted_ref}"
    zip_path = tmp_dir / "repo.zip"
    with urllib.request.urlopen(url) as response, zip_path.open("wb") as output:
        shutil.copyfileobj(response, output)
    return zip_path


def safe_extract(zip_file: zipfile.ZipFile, dest_dir: Path) -> None:
    dest_root = dest_dir.resolve()
    for info in zip_file.infolist():
        candidate = (dest_dir / info.filename).resolve()
        if candidate != dest_root and not str(candidate).startswith(str(dest_root) + os.sep):
            raise RuntimeError("Archive contains files outside the destination.")
    zip_file.extractall(dest_dir)


def extract_skill(zip_path: Path, tmp_dir: Path) -> Path:
    with zipfile.ZipFile(zip_path) as archive:
        safe_extract(archive, tmp_dir)
        top_levels = sorted({name.split("/")[0] for name in archive.namelist() if name})
    if len(top_levels) != 1:
        raise RuntimeError("Unexpected GitHub archive layout.")
    repo_root = tmp_dir / top_levels[0]
    skill_dir = repo_root / SKILL_SUBPATH
    if not (skill_dir / "SKILL.md").is_file():
        raise RuntimeError(f"Missing SKILL.md in extracted skill path: {skill_dir}")
    return skill_dir


def install_skill(source_dir: Path, target_dir: Path, force: bool) -> None:
    if target_dir.exists():
        if not force:
            raise RuntimeError(f"Destination already exists: {target_dir}")
        shutil.rmtree(target_dir)
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_dir, target_dir)


def main() -> int:
    args = parse_args()
    target_dir = destination_dir(args.dest, args.name)
    with tempfile.TemporaryDirectory(prefix="software-thesis-docx-") as tmp:
        tmp_dir = Path(tmp)
        zip_path = download_repo_zip(args.ref, tmp_dir)
        skill_dir = extract_skill(zip_path, tmp_dir)
        install_skill(skill_dir, target_dir, args.force)

    print(f"Installed {args.name} to {target_dir}")
    requirements = target_dir / "requirements.txt"
    if requirements.is_file():
        print(f"Optional dependency step: python -m pip install -r {requirements}")
    print("Restart Codex to pick up new skills.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Installation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
