from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from statistics import pstdev
from typing import Any

from docx import Document

from aigc_utils import (
    RECIPE_ADD_QUALIFIER,
    RECIPE_BREAK_TEMPLATE,
    RECIPE_EXPAND_CONTEXT,
    RECIPE_NORMALIZE,
    RECIPE_SPLIT_DENSE,
    collect_typography_flags,
    is_chinese_dominant,
    ordered_unique,
)


TRANSITION_PHRASES = [
    "总的来说",
    "综上所述",
    "需要指出的是",
    "值得注意的是",
    "可以看出",
    "由此可见",
    "因此可以认为",
    "进一步来看",
    "从某种意义上讲",
]

LOW_INFORMATION_PHRASES = [
    "具有重要意义",
    "提供了新的思路",
    "展现出良好前景",
    "具有一定参考价值",
    "能够有效提升",
    "在一定程度上",
    "实现了较好的效果",
    "提供方法论层面的参考",
]

TIGHT_ENUMERATION_RE = re.compile(
    r"(一是|二是|三是|四是|五是|六是|第一，|第二，|第三，|第四，|第五，|第六，)"
)
CLAIM_PATTERNS = [
    re.compile(r"(显著|明显|有效|成功|完成|提升|优化|增强|改善|证明|表明)"),
]
EVIDENCE_PATTERNS = [
    re.compile(r"\[\d+\]"),
    re.compile(r"`[^`]+`"),
    re.compile(r"\d+(\.\d+)?"),
    re.compile(r"(API|SQL|Redis|FastAPI|React|Python|PostgreSQL|Milvus|LangGraph|RAGAS)", re.IGNORECASE),
]

DENSE_OPERATION_WORDS = [
    "通过",
    "实现",
    "提升",
    "优化",
    "增强",
    "构建",
    "完成",
    "建立",
    "开展",
    "结合",
    "搭建",
    "整合",
    "形成",
    "支撑",
]

TECH_TERM_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9\-\+]{1,}\b")
EXPLANATORY_MARKERS = ["用于", "负责", "分别", "其中", "例如", "比如", "即", "也就是说", "用来"]


@dataclass(frozen=True)
class Signal:
    weight: float
    description: str
    recipes: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check DOCX paragraphs for AIGC-style writing risk signals.")
    parser.add_argument("--input", required=True, help="Input DOCX path.")
    parser.add_argument("--output", required=True, help="Output JSON report path.")
    parser.add_argument("--threshold", type=float, default=0.58, help="Risk score threshold for recommended rewrite.")
    return parser.parse_args()


def tokenize(text: str) -> list[str]:
    return [token for token in re.findall(r"[\w\u4e00-\u9fff]+", text.lower()) if token]


def split_sentences(text: str) -> list[str]:
    return [item.strip() for item in re.split(r"[。！？!?；;]+", text) if item.strip()]


def signal_transition_phrases(text: str) -> Signal | None:
    matches = [phrase for phrase in TRANSITION_PHRASES if phrase in text]
    if not matches:
        return None
    return Signal(
        weight=min(0.16, 0.05 * len(matches)),
        description=f"模板化衔接词偏多: {', '.join(matches[:3])}",
        recipes=(RECIPE_ADD_QUALIFIER, RECIPE_EXPAND_CONTEXT),
    )


def signal_low_information(text: str) -> Signal | None:
    matches = [phrase for phrase in LOW_INFORMATION_PHRASES if phrase in text]
    if not matches:
        return None
    return Signal(
        weight=min(0.18, 0.06 * len(matches)),
        description=f"空泛总结语偏多: {', '.join(matches[:3])}",
        recipes=(RECIPE_EXPAND_CONTEXT,),
    )


def signal_tight_enumeration(text: str) -> Signal | None:
    matches = TIGHT_ENUMERATION_RE.findall(text)
    if len(matches) < 2:
        return None
    return Signal(
        weight=min(0.24, 0.09 + 0.04 * len(matches)),
        description=f"压缩型枚举模板偏强: {', '.join(matches[:4])}",
        recipes=(RECIPE_BREAK_TEMPLATE, RECIPE_SPLIT_DENSE),
    )


def signal_colon_semicolon_template(text: str) -> Signal | None:
    colon_count = text.count("：") + text.count(":")
    semicolon_count = text.count("；") + text.count(";")
    if colon_count == 0 or semicolon_count == 0 or len(text) < 70:
        return None
    return Signal(
        weight=min(0.18, 0.08 + 0.04 * semicolon_count),
        description=f"冒号/分号驱动的模板段偏强: colon={colon_count}, semicolon={semicolon_count}",
        recipes=(RECIPE_BREAK_TEMPLATE, RECIPE_SPLIT_DENSE),
    )


def signal_dense_operation_chain(text: str) -> Signal | None:
    dense_hits = [word for word in DENSE_OPERATION_WORDS if word in text]
    list_marks = text.count("、")
    if len(dense_hits) < 4 or list_marks < 2 or len(text) < 80:
        return None
    return Signal(
        weight=min(0.22, 0.08 + 0.02 * len(dense_hits) + 0.01 * list_marks),
        description=f"压缩型学术句偏强: verbs={len(dense_hits)}, list_marks={list_marks}",
        recipes=(RECIPE_SPLIT_DENSE, RECIPE_EXPAND_CONTEXT),
    )


def signal_term_stack_without_explanation(text: str) -> Signal | None:
    if not is_chinese_dominant(text):
        return None
    terms = ordered_unique(term for term in TECH_TERM_RE.findall(text) if len(term) >= 2)
    if len(terms) < 3:
        return None
    if any(marker in text for marker in EXPLANATORY_MARKERS):
        return None
    return Signal(
        weight=0.14,
        description=f"术语堆叠但缺少解释性展开: {', '.join(terms[:4])}",
        recipes=(RECIPE_EXPAND_CONTEXT, RECIPE_SPLIT_DENSE),
    )


def signal_uniform_sentence_lengths(text: str) -> Signal | None:
    sentences = split_sentences(text)
    if len(sentences) < 3:
        return None
    lengths = [len(tokenize(sentence)) for sentence in sentences]
    if not lengths or max(lengths) == 0:
        return None
    mean_length = sum(lengths) / len(lengths)
    if mean_length < 8:
        return None
    std = pstdev(lengths)
    if std > 3.0:
        return None
    return Signal(
        weight=0.1,
        description=f"句长分布过于均匀: mean={mean_length:.1f}, std={std:.2f}",
        recipes=(RECIPE_SPLIT_DENSE,),
    )


def signal_claim_without_evidence(text: str) -> Signal | None:
    if not any(pattern.search(text) for pattern in CLAIM_PATTERNS):
        return None
    if any(pattern.search(text) for pattern in EVIDENCE_PATTERNS):
        return None
    return Signal(
        weight=0.12,
        description="存在效果性论断但缺少明显证据标记",
        recipes=(RECIPE_EXPAND_CONTEXT,),
    )


def signal_typography_issues(text: str) -> Signal | None:
    flags = collect_typography_flags(text)
    if not flags:
        return None
    return Signal(
        weight=min(0.12, 0.04 * len(flags)),
        description=f"端内标点/空格规范存在问题: {', '.join(flags)}",
        recipes=(RECIPE_NORMALIZE,),
    )


def paragraph_report(index: int, text: str, threshold: float) -> dict[str, Any]:
    signals: list[dict[str, Any]] = []
    rewrite_recipe: list[str] = []

    for detector in [
        signal_transition_phrases,
        signal_low_information,
        signal_tight_enumeration,
        signal_colon_semicolon_template,
        signal_dense_operation_chain,
        signal_term_stack_without_explanation,
        signal_uniform_sentence_lengths,
        signal_claim_without_evidence,
        signal_typography_issues,
    ]:
        result = detector(text)
        if result is None:
            continue
        signals.append(
            {
                "weight": round(result.weight, 3),
                "description": result.description,
                "recipes": list(result.recipes),
            }
        )
        rewrite_recipe.extend(result.recipes)

    score = round(min(1.0, sum(item["weight"] for item in signals)), 3)
    typography_flags = collect_typography_flags(text)
    return {
        "paragraph_index": index,
        "excerpt": text[:160],
        "risk_score": score,
        "signals": signals,
        "rewrite_recipe": ordered_unique(rewrite_recipe),
        "typography_flags": typography_flags,
        "recommended_rewrite": score >= threshold,
    }


def build_report(document: Document, threshold: float) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    recipe_counter: Counter[str] = Counter()
    typography_issue_count = 0
    for index, paragraph in enumerate(document.paragraphs):
        text = paragraph.text.strip()
        if len(text) < 30:
            continue
        item = paragraph_report(index, text, threshold)
        items.append(item)
        recipe_counter.update(item["rewrite_recipe"])
        if item["typography_flags"]:
            typography_issue_count += 1

    summary = {
        "paragraphs_scanned": len(items),
        "high_risk_count": sum(1 for item in items if item["recommended_rewrite"]),
        "average_risk": round(sum(item["risk_score"] for item in items) / len(items), 3) if items else 0.0,
        "max_risk": max((item["risk_score"] for item in items), default=0.0),
        "typography_issue_count": typography_issue_count,
        "rewrite_recipe_counts": dict(recipe_counter),
    }
    return {
        "schema_version": 2,
        "threshold": threshold,
        "summary": summary,
        "items": items,
    }


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    document = Document(input_path)
    report = build_report(document, threshold=args.threshold)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
