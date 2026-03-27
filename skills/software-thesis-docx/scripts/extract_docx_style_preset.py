from __future__ import annotations

import argparse
from pathlib import Path

from docx import Document

from style_preset_utils import extract_style_preset_from_document, save_style_preset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract a reusable thesis style preset from a DOCX template.")
    parser.add_argument("--input", required=True, help="Path to the source DOCX template.")
    parser.add_argument("--output", required=True, help="Path to the output style preset JSON.")
    parser.add_argument(
        "--source-label",
        help="Optional human-readable label to store in preset metadata.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    document = Document(input_path)
    preset = extract_style_preset_from_document(document, source_label=args.source_label or input_path.name)
    save_style_preset(output_path, preset)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
