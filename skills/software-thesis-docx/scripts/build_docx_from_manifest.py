from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from style_preset_utils import (
    apply_paragraph_style,
    apply_run_style,
    default_style_preset_path,
    extract_style_preset_from_document,
    load_style_preset,
    resolve_role,
)

try:
    from PIL import Image
except Exception:
    Image = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a thesis DOCX from a structured manifest.")
    parser.add_argument("--manifest", required=True, help="Path to the thesis manifest JSON file.")
    parser.add_argument("--output", required=True, help="Path to the output DOCX file.")
    parser.add_argument(
        "--workspace",
        help="Optional workspace root used to resolve relative figure paths after manifest-relative resolution.",
    )
    parser.add_argument(
        "--style-preset",
        help="Optional style preset JSON. Overrides manifest.formatting mode.",
    )
    return parser.parse_args()


def add_update_fields_on_open(document: Document) -> None:
    settings = document.settings.element
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    settings.append(update)


def add_field(paragraph, instruction: str, placeholder: str = ""):
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run = paragraph.add_run()
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(separate)
    run._r.append(text)
    run._r.append(end)
    return run


def ensure_custom_style(document: Document, name: str) -> None:
    if name in document.styles:
        return
    document.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)


def fit_image(path: Path, max_width_cm: float, max_height_cm: float):
    if Image is None:
        return Cm(max_width_cm), None
    with Image.open(path) as img:
        width_px, height_px = img.size
    width_cm = width_px / 96 * 2.54
    height_cm = height_px / 96 * 2.54
    scale = min(max_width_cm / width_cm, max_height_cm / height_cm, 1.0)
    return Cm(width_cm * scale), Cm(height_cm * scale)


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("Manifest root must be a JSON object.")
    return data


def resolve_path(raw_path: str, manifest_path: Path, workspace: Path | None) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    manifest_relative = (manifest_path.parent / path).resolve()
    if manifest_relative.exists():
        return manifest_relative
    if workspace is not None:
        workspace_relative = (workspace / path).resolve()
        if workspace_relative.exists():
            return workspace_relative
    return manifest_relative


def resolve_style_preset(
    manifest: dict[str, Any],
    manifest_path: Path,
    workspace: Path | None,
    cli_style_preset: str | None,
) -> dict[str, Any]:
    if cli_style_preset:
        return load_style_preset(resolve_path(cli_style_preset, manifest_path, workspace))

    formatting = manifest.get("formatting") or {}
    if not isinstance(formatting, dict):
        formatting = {}

    mode = formatting.get("mode")
    if mode is None:
        if formatting.get("style_preset_path"):
            mode = "custom_style_preset"
        elif formatting.get("template_docx_path"):
            mode = "custom_template_docx"
        else:
            mode = "default_preset"

    if mode == "default_preset":
        return load_style_preset(default_style_preset_path())
    if mode == "custom_style_preset":
        preset_path = formatting.get("style_preset_path")
        if not preset_path:
            raise ValueError("formatting.style_preset_path is required for custom_style_preset mode.")
        return load_style_preset(resolve_path(preset_path, manifest_path, workspace))
    if mode == "custom_template_docx":
        template_docx = formatting.get("template_docx_path")
        if not template_docx:
            raise ValueError("formatting.template_docx_path is required for custom_template_docx mode.")
        template_path = resolve_path(template_docx, manifest_path, workspace)
        return extract_style_preset_from_document(Document(template_path), source_label=template_path.name)
    raise ValueError(f"Unsupported formatting.mode: {mode}")


class ThesisDocBuilder:
    def __init__(
        self,
        manifest: dict[str, Any],
        manifest_path: Path,
        output_path: Path,
        workspace: Path | None,
        style_preset: dict[str, Any],
    ) -> None:
        self.manifest = manifest
        self.manifest_path = manifest_path
        self.output_path = output_path
        self.workspace = workspace
        self.style_preset = style_preset
        self.document = Document()
        self._configure_styles()
        self._configure_sections()
        add_update_fields_on_open(self.document)

    def role(self, role_name: str) -> dict[str, Any]:
        return resolve_role(self.style_preset, role_name)

    def resolve_path(self, raw_path: str) -> Path:
        return resolve_path(raw_path, self.manifest_path, self.workspace)

    def _configure_styles(self) -> None:
        ensure_custom_style(self.document, "Caption")
        style_roles = [
            ("Normal", "body_cn"),
            ("Heading 1", "chapter"),
            ("Heading 2", "section"),
            ("Heading 3", "subsection"),
            ("Title", "cover_title_cn"),
            ("Caption", "figure_caption"),
        ]
        for style_name, role_name in style_roles:
            role = self.role(role_name)
            style = self.document.styles[style_name]
            font = style.font
            font.name = role["run"]["ascii_font"]
            font.size = Pt(float(role["run"]["size_pt"]))
            font.bold = bool(role["run"].get("bold", False))
            rpr = style._element.get_or_add_rPr()
            rfonts = rpr.rFonts
            if rfonts is None:
                rfonts = OxmlElement("w:rFonts")
                rpr.append(rfonts)
            rfonts.set(qn("w:ascii"), role["run"]["ascii_font"])
            rfonts.set(qn("w:hAnsi"), role["run"]["ascii_font"])
            rfonts.set(qn("w:eastAsia"), role["run"]["east_asia_font"])
            rfonts.set(qn("w:cs"), role["run"]["ascii_font"])

    def _configure_sections(self) -> None:
        page = self.style_preset.get("page", {})
        for section in self.document.sections:
            section.top_margin = Cm(float(page.get("top_margin_cm", 2.5)))
            section.bottom_margin = Cm(float(page.get("bottom_margin_cm", 2.5)))
            section.left_margin = Cm(float(page.get("left_margin_cm", 2.0)))
            section.right_margin = Cm(float(page.get("right_margin_cm", 2.0)))
            section.header_distance = Cm(float(page.get("header_distance_cm", 1.5)))
            section.footer_distance = Cm(float(page.get("footer_distance_cm", 1.75)))

    def _add_page_number(self, paragraph) -> None:
        add_field(paragraph, "PAGE", "")
        if paragraph.runs:
            page_run = self.role("reference_item")["run"] | {
                "ascii_font": "Times New Roman",
                "east_asia_font": "Times New Roman",
                "size_pt": 10.5,
            }
            apply_run_style(paragraph.runs[-1], page_run)

    def _body_section(self):
        section = self.document.add_section(WD_SECTION_START.NEW_PAGE)
        page = self.style_preset.get("page", {})
        section.top_margin = Cm(float(page.get("top_margin_cm", 2.5)))
        section.bottom_margin = Cm(float(page.get("bottom_margin_cm", 2.5)))
        section.left_margin = Cm(float(page.get("left_margin_cm", 2.0)))
        section.right_margin = Cm(float(page.get("right_margin_cm", 2.0)))
        section.header_distance = Cm(float(page.get("header_distance_cm", 1.5)))
        section.footer_distance = Cm(float(page.get("footer_distance_cm", 1.75)))
        footer_p = section.footer.paragraphs[0]
        footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        self._add_page_number(footer_p)
        return section

    def add_role_text(self, role_name: str, text: str, style_name: str | None = None):
        paragraph = self.document.add_paragraph(style=style_name)
        apply_paragraph_style(paragraph, self.role(role_name)["paragraph"])
        run = paragraph.add_run(text)
        apply_run_style(run, self.role(role_name)["run"])
        return paragraph

    def add_body_text(self, text: str, role_name: str, *, center: bool = False, indent: bool = True) -> None:
        paragraph = self.document.add_paragraph(style="Normal")
        apply_paragraph_style(paragraph, self.role(role_name)["paragraph"])
        if center:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if not indent:
            paragraph.paragraph_format.first_line_indent = Cm(0)
        run = paragraph.add_run(text)
        apply_run_style(run, self.role(role_name)["run"])

    def chapter(self, text: str, role_name: str = "chapter") -> None:
        self.add_role_text(role_name, text, style_name="Heading 1")

    def section(self, text: str, role_name: str = "section") -> None:
        self.add_role_text(role_name, text, style_name="Heading 2")

    def subsection(self, text: str, role_name: str = "subsection") -> None:
        self.add_role_text(role_name, text, style_name="Heading 3")

    def add_keywords(self, label: str, values: list[str] | str, english: bool = False) -> None:
        paragraph = self.document.add_paragraph()
        label_role = "keywords_label_en" if english else "keywords_label_cn"
        text_role = "keywords_text_en" if english else "keywords_text_cn"
        apply_paragraph_style(paragraph, self.role(label_role)["paragraph"])
        text = values if isinstance(values, str) else ("; ".join(values) if english else "；".join(values))
        label_run = paragraph.add_run(label)
        text_run = paragraph.add_run(text)
        apply_run_style(label_run, self.role(label_role)["run"])
        apply_run_style(text_run, self.role(text_role)["run"])

    def add_table_caption(self, text: str) -> None:
        self.add_role_text("table_caption", text)

    def add_figure_caption(self, text: str) -> None:
        self.add_role_text("figure_caption", text)

    def set_cell_text(self, cell, text: str, bold: bool = False, center: bool = False) -> None:
        cell.text = ""
        paragraph = cell.paragraphs[0]
        apply_paragraph_style(paragraph, self.role("table_caption")["paragraph"])
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
        run = paragraph.add_run(text)
        run_style = dict(self.role("table_caption")["run"])
        if bold:
            run_style["bold"] = True
        apply_run_style(run, run_style)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    def add_table(self, caption: str, rows: list[list[str]]) -> None:
        if not rows or not rows[0]:
            raise ValueError("Table rows must be a non-empty 2D array.")
        width = len(rows[0])
        if any(len(row) != width for row in rows):
            raise ValueError("All table rows must have the same width.")
        self.add_table_caption(caption)
        table = self.document.add_table(rows=len(rows), cols=width)
        table.style = "Table Grid"
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for r_idx, row in enumerate(rows):
            for c_idx, value in enumerate(row):
                self.set_cell_text(table.cell(r_idx, c_idx), str(value), bold=(r_idx == 0), center=(r_idx == 0))
        self.document.add_paragraph()

    def add_figure(self, path_str: str, caption: str, max_width_cm: float, max_height_cm: float) -> None:
        image_path = self.resolve_path(path_str)
        if not image_path.exists():
            raise FileNotFoundError(f"Figure not found: {path_str} -> {image_path}")
        paragraph = self.document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        width, height = fit_image(image_path, max_width_cm=max_width_cm, max_height_cm=max_height_cm)
        run = paragraph.add_run()
        if height is not None:
            run.add_picture(str(image_path), width=width, height=height)
        else:
            run.add_picture(str(image_path), width=width)
        self.add_figure_caption(caption)

    def add_reference(self, text: str) -> None:
        paragraph = self.document.add_paragraph(style="Normal")
        apply_paragraph_style(paragraph, self.role("reference_item")["paragraph"])
        run = paragraph.add_run(text)
        apply_run_style(run, self.role("reference_item")["run"])

    def render_cover_and_front_matter(self) -> None:
        metadata = self.manifest.get("metadata", {})
        for _ in range(3):
            self.document.add_paragraph()
        self.add_role_text("cover_label", metadata.get("document_label", "毕业论文"))
        self.add_role_text("cover_title_cn", metadata["title_cn"])
        if metadata.get("title_en"):
            self.add_role_text("cover_title_en", metadata["title_en"])
        for _ in range(3):
            self.document.add_paragraph()
        for label, key in [
            ("学生姓名：", "student_name"),
            ("学    号：", "student_id"),
            ("专    业：", "major"),
            ("学    院：", "college"),
            ("指导教师：", "advisor"),
        ]:
            self.add_role_text("cover_meta", f"{label}{metadata.get(key, '________________')}")
        self.add_role_text("cover_meta", f"完成日期：{metadata.get('date_cn', '________________')}")

        self._body_section()

        abstract_cn = metadata.get("abstract_cn") or []
        if abstract_cn:
            self.add_role_text("abstract_heading_cn", "摘要")
            for paragraph in abstract_cn:
                self.add_body_text(str(paragraph), "body_cn")
            if metadata.get("keywords_cn"):
                self.add_keywords("关键词：", metadata["keywords_cn"])
            self.document.add_page_break()

        abstract_en = metadata.get("abstract_en") or []
        if abstract_en:
            self.add_role_text("abstract_heading_en", "Abstract")
            for paragraph in abstract_en:
                self.add_body_text(str(paragraph), "body_en")
            if metadata.get("keywords_en"):
                self.add_keywords("Keywords: ", metadata["keywords_en"], english=True)
            self.document.add_page_break()

        if metadata.get("include_toc", True):
            self.add_role_text("toc_heading", "目录")
            toc_paragraph = self.document.add_paragraph()
            apply_paragraph_style(toc_paragraph, self.role("body_cn")["paragraph"])
            toc_paragraph.paragraph_format.first_line_indent = Cm(0)
            add_field(toc_paragraph, 'TOC \\o "1-3" \\h \\z \\u', "目录将在打开文档后自动更新")
            self.document.add_page_break()

    def render_blocks(self) -> None:
        blocks = self.manifest.get("blocks") or self.manifest.get("content_blocks")
        if not isinstance(blocks, list):
            raise ValueError("Manifest must contain a top-level 'blocks' array.")

        for index, block in enumerate(blocks, start=1):
            if not isinstance(block, dict):
                raise ValueError(f"Block #{index} must be an object.")
            block_type = block.get("type")
            if block_type == "chapter":
                self.chapter(block["title"])
            elif block_type == "section":
                self.section(block["title"])
            elif block_type == "subsection":
                self.subsection(block["title"])
            elif block_type == "paragraph":
                self.add_body_text(
                    block["text"],
                    "body_en" if bool(block.get("english", False)) else "body_cn",
                    center=bool(block.get("center", False)),
                    indent=block.get("indent", True),
                )
            elif block_type == "figure":
                self.add_figure(
                    block["path"],
                    block["caption"],
                    float(block.get("max_width_cm", 15.2)),
                    float(block.get("max_height_cm", 18.5)),
                )
            elif block_type == "table":
                self.add_table(block["caption"], block["rows"])
            elif block_type == "page_break":
                self.document.add_page_break()
            elif block_type == "references":
                self.chapter(block.get("title", "参考文献"), role_name="reference_heading")
                for item in block.get("items", []):
                    self.add_reference(str(item))
            else:
                raise ValueError(f"Unsupported block type at index {index}: {block_type}")

    def build(self) -> None:
        metadata = self.manifest.get("metadata", {})
        title_cn = metadata.get("title_cn")
        if not title_cn:
            raise ValueError("Manifest metadata.title_cn is required.")
        self.document.core_properties.title = title_cn
        self.document.core_properties.subject = metadata.get("subject", "Software thesis document")
        self.document.core_properties.category = metadata.get("category", "thesis")
        self.document.core_properties.comments = metadata.get("comments", "Generated from a structured thesis manifest.")
        self.render_cover_and_front_matter()
        self.render_blocks()
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.document.save(str(self.output_path))


def main() -> None:
    args = parse_args()
    manifest_path = Path(args.manifest).resolve()
    output_path = Path(args.output).resolve()
    workspace = Path(args.workspace).resolve() if args.workspace else None
    manifest = load_manifest(manifest_path)
    style_preset = resolve_style_preset(manifest, manifest_path=manifest_path, workspace=workspace, cli_style_preset=args.style_preset)
    builder = ThesisDocBuilder(
        manifest,
        manifest_path=manifest_path,
        output_path=output_path,
        workspace=workspace,
        style_preset=style_preset,
    )
    builder.build()
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
