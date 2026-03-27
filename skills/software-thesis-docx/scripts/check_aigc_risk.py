from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
from statistics import pstdev
from typing import Any

from docx import Document


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
]

CLAIM_PATTERNS = [
    re.compile(r"(显著|明显|有效|成功|完成|提升|优化|增强|改善|证明|表明)"),
]

EVIDENCE_PATTERNS = [
    re.compile(r"\[\d+\]"),
    re.compile(r"`[^`]+`"),
    re.compile(r"\d+(\.\d+)?"),
    re.compile(r"(API|SQL|Redis|FastAPI|React|Python|PostgreSQL|Milvus|LangGraph|RAGAS)", re.IGNORECASE),
]


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


def signal_transition_phrases(text: str) -> tuple[float, str] | None:
    matches = [phrase for phrase in TRANSITION_PHRASES if phrase in text]
    if not matches:
        return None
    return min(0.2, 0.06 * len(matches)), f"模板化衔接词偏多: {', '.join(matches[:3])}"


def signal_low_information(text: str) -> tuple[float, str] | None:
    matches = [phrase for phrase in LOW_INFORMATION_PHRASES if phrase in text]
    if not matches:
        return None
    return min(0.22, 0.07 * len(matches)), f"空泛总结语偏多: {', '.join(matches[:3])}"


def signal_uniform_sentence_lengths(text: str) -> tuple[float, str] | None:
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
    return 0.16, f"句长分布过于均匀: mean={mean_length:.1f}, std={std:.2f}"


def signal_repeated_ngrams(text: str) -> tuple[float, str] | None:
    tokens = tokenize(text)
    if len(tokens) < 12:
        return None
    tri_grams = [" ".join(tokens[index : index + 3]) for index in range(len(tokens) - 2)]
    counter = Counter(tri_grams)
    repeated = [item for item, count in counter.items() if count >= 2]
    if not repeated:
        return None
    return min(0.2, 0.05 * len(repeated)), f"重复三元组偏多: {repeated[:3]}"


def signal_claim_without_evidence(text: str) -> tuple[float, str] | None:
    if not any(pattern.search(text) for pattern in CLAIM_PATTERNS):
        return None
    if any(pattern.search(text) for pattern in EVIDENCE_PATTERNS):
        return None
    return 0.18, "存在效果性论断但缺少明显证据标记"


def signal_low_specificity(text: str) -> tuple[float, str] | None:
    tokens = tokenize(text)
    if len(tokens) < 20:
        return None
    unique_ratio = len(set(tokens)) / len(tokens)
    if unique_ratio >= 0.58:
        return None
    return 0.14, f"词汇多样性偏低: unique_ratio={unique_ratio:.2f}"


def paragraph_report(index: int, text: str, threshold: float) -> dict[str, Any]:
    signals: list[dict[str, Any]] = []
    for detector in [
        signal_transition_phrases,
        signal_low_information,
        signal_uniform_sentence_lengths,
        signal_repeated_ngrams,
        signal_claim_without_evidence,
        signal_low_specificity,
    ]:
        result = detector(text)
        if result is None:
            continue
        weight, description = result
        signals.append({"weight": round(weight, 3), "description": description})

    score = round(min(1.0, sum(item["weight"] for item in signals)), 3)
    return {
        "paragraph_index": index,
        "excerpt": text[:160],
        "risk_score": score,
        "signals": signals,
        "recommended_rewrite": score >= threshold,
    }


def build_report(document: Document, threshold: float) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for index, paragraph in enumerate(document.paragraphs):
        text = paragraph.text.strip()
        if len(text) < 30:
            continue
        items.append(paragraph_report(index, text, threshold))

    summary = {
        "paragraphs_scanned": len(items),
        "high_risk_count": sum(1 for item in items if item["recommended_rewrite"]),
        "average_risk": round(sum(item["risk_score"] for item in items) / len(items), 3) if items else 0.0,
        "max_risk": max((item["risk_score"] for item in items), default=0.0),
    }
    return {
        "schema_version": 1,
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
