from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from docx import Document


@dataclass(frozen=True)
class RewriteRule:
    match_text: str
    replace_text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rewrite exact-match single-run paragraphs in a DOCX while preserving paragraph formatting.")
    parser.add_argument("--input", required=True, help="Input DOCX path.")
    parser.add_argument("--output", required=True, help="Output DOCX path.")
    parser.add_argument("--replacements", required=True, help="JSON file containing exact paragraph rewrites.")
    return parser.parse_args()


def load_replacements(path: Path) -> list[RewriteRule]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    items: Any
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict) and isinstance(data.get("items"), list):
        items = data["items"]
    else:
        raise ValueError("Replacement file must be a list or an object with an 'items' array.")
    return [RewriteRule(match_text=item["match_text"], replace_text=item["replace_text"]) for item in items]


def replace_paragraph_text(paragraph, new_text: str) -> None:
    if not paragraph.runs:
        raise ValueError("Target paragraph has no runs.")
    if len(paragraph.runs) != 1:
        raise ValueError(f"Target paragraph is not single-run: {len(paragraph.runs)}")
    paragraph.runs[0].text = new_text


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    replacement_path = Path(args.replacements).resolve()
    rules = load_replacements(replacement_path)

    shutil.copy2(input_path, output_path)
    document = Document(output_path)

    for rule in rules:
        matches = [paragraph for paragraph in document.paragraphs if paragraph.text == rule.match_text]
        if len(matches) != 1:
            raise ValueError(
                f"Expected exactly one paragraph match, found {len(matches)} for: {rule.match_text[:60]}..."
            )
        replace_paragraph_text(matches[0], rule.replace_text)

    document.save(output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
