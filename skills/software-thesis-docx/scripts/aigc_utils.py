from __future__ import annotations

import re
from typing import Iterable


REWRITE_PROFILES = {"academic_safe", "explicit_low_aigc"}

RECIPE_EXPAND_CONTEXT = "expand_context"
RECIPE_BREAK_TEMPLATE = "break_template_enumeration"
RECIPE_ADD_QUALIFIER = "add_qualifier_or_example"
RECIPE_NORMALIZE = "normalize_typography"
RECIPE_SPLIT_DENSE = "split_dense_sentence"

CJK_RE = re.compile(r"[\u4e00-\u9fff]")
LATIN_RE = re.compile(r"[A-Za-z]")
SPACE_BETWEEN_CN_EN_RE = re.compile(r"[\u4e00-\u9fff]\s+[A-Za-z0-9\[]|[A-Za-z0-9\]]\s+[\u4e00-\u9fff]")
SPACE_BEFORE_CITATION_RE = re.compile(r"\s+\[\d+\]")
HALFWIDTH_PUNCT_IN_CN_RE = re.compile(r"[,:;()][\u4e00-\u9fff]|[\u4e00-\u9fff][,:;()]")

ENUMERATION_PREFIX_RE = re.compile(
    r"(?:(?<=^)|(?<=[：:；;。]))\s*"
    r"(一是|二是|三是|四是|五是|六是|"
    r"第一，|第二，|第三，|第四，|第五，|第六，|"
    r"第一是|第二是|第三是|第四是|第五是|第六是|"
    r"第一个方面是|第二个方面是|第三个方面是|第四个方面是|第五个方面是|第六个方面是)"
)

SPLIT_CUES = [
    "其中",
    "同时",
    "此外",
    "另外",
    "在前端",
    "在后端",
    "在数据层",
    "在系统",
    "系统",
    "用户",
    "从而",
    "因此",
    "并且",
    "随后",
    "然后",
]

COMMON_REPLACEMENTS = [
    (re.compile(r"该系统可"), "该系统能够"),
    (re.compile(r"系统可"), "系统能够"),
    (re.compile(r"可在"), "能够在"),
    (re.compile(r"可为"), "能够为"),
    (re.compile(r"没法"), "难以"),
]


def is_chinese_dominant(text: str) -> bool:
    cjk_count = len(CJK_RE.findall(text))
    latin_count = len(LATIN_RE.findall(text))
    return cjk_count >= max(12, latin_count)


def parse_paragraph_indices(raw: str | None) -> list[int] | None:
    if not raw:
        return None
    result: list[int] = []
    for part in raw.split(","):
        token = part.strip()
        if not token:
            continue
        result.append(int(token))
    return sorted(set(result))


def collect_typography_flags(text: str) -> list[str]:
    flags: list[str] = []
    if SPACE_BETWEEN_CN_EN_RE.search(text):
        flags.append("space_between_cn_en")
    if SPACE_BEFORE_CITATION_RE.search(text):
        flags.append("space_before_citation")
    if is_chinese_dominant(text) and HALFWIDTH_PUNCT_IN_CN_RE.search(text):
        flags.append("halfwidth_punctuation_in_chinese")
    if is_chinese_dominant(text) and ("(" in text or ")" in text):
        flags.append("ascii_parentheses_in_chinese")
    if "；" in text and ";" in text:
        flags.append("mixed_semicolon_style")
    if "：" in text and ":" in text:
        flags.append("mixed_colon_style")
    return flags


def normalize_typography(text: str) -> str:
    rewritten = text.strip()
    rewritten = re.sub(r"[ \t]+", " ", rewritten)
    rewritten = re.sub(r"\s+([，。；：！？）】])", r"\1", rewritten)
    rewritten = re.sub(r"([（【])\s+", r"\1", rewritten)
    rewritten = re.sub(r"\s+(\[\d+\])", r"\1", rewritten)
    rewritten = re.sub(r"(\[\d+\])\s+", r"\1", rewritten)
    rewritten = re.sub(r"\s{2,}", " ", rewritten)

    if is_chinese_dominant(rewritten):
        rewritten = re.sub(r"(?<=[\u4e00-\u9fff]),(?=[\u4e00-\u9fffA-Za-z0-9])", "，", rewritten)
        rewritten = re.sub(r"(?<=[\u4e00-\u9fff]):(?=[\u4e00-\u9fffA-Za-z0-9])", "：", rewritten)
        rewritten = re.sub(r"(?<=[\u4e00-\u9fff]);(?=[\u4e00-\u9fffA-Za-z0-9])", "；", rewritten)
        rewritten = re.sub(r"(?<=[\u4e00-\u9fff])\((?=[A-Za-z\u4e00-\u9fff])", "（", rewritten)
        rewritten = re.sub(r"(?<=[A-Za-z0-9\u4e00-\u9fff])\)(?=[\u4e00-\u9fff，。；：！？、]|$)", "）", rewritten)
        rewritten = re.sub(r"([\u4e00-\u9fff])\s+([\u4e00-\u9fff])", r"\1\2", rewritten)
        rewritten = re.sub(r"([\u4e00-\u9fff])\s+([A-Za-z0-9\[])", r"\1\2", rewritten)
        rewritten = re.sub(r"([A-Za-z0-9\]])\s+([\u4e00-\u9fff])", r"\1\2", rewritten)

    return rewritten


def enumeration_items(text: str) -> tuple[str, list[str]] | None:
    matches = list(ENUMERATION_PREFIX_RE.finditer(text))
    if len(matches) < 2:
        return None

    intro = text[: matches[0].start()].strip()
    items: list[str] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        content = text[start:end].strip(" ：:；;，,。")
        if content:
            items.append(content)
    if len(items) < 2:
        return None
    return intro, items


def rewrite_template_enumeration(text: str, profile: str) -> str:
    parsed = enumeration_items(text)
    if parsed is None:
        return text

    intro, items = parsed
    if intro:
        intro_text = intro.rstrip("：:；;，,。") + "。"
    else:
        intro_text = ""

    if profile == "explicit_low_aigc":
        labels = [
            "第一个方面是",
            "第二个方面是",
            "第三个方面是",
            "第四个方面是",
            "第五个方面是",
            "第六个方面是",
        ]
    else:
        labels = [
            "第一，",
            "第二，",
            "第三，",
            "第四，",
            "第五，",
            "第六，",
        ]

    sentences: list[str] = []
    for index, item in enumerate(items):
        label = labels[index] if index < len(labels) else f"第{index + 1}项，"
        content = item.rstrip("。")
        if profile == "explicit_low_aigc":
            sentences.append(f"{label}{content}。")
        else:
            sentences.append(f"{label}{content}。")

    return intro_text + "".join(sentences)


def split_dense_sentence(text: str, profile: str) -> str:
    if len(text) < 90 or text.count("，") < 3:
        return text

    rewritten = text
    max_splits = 2 if profile == "explicit_low_aigc" else 1
    for _ in range(max_splits):
        if len(rewritten) < 90 or rewritten.count("，") < 3:
            break
        comma_positions = [match.start() for match in re.finditer("，", rewritten)]
        if not comma_positions:
            break

        candidate_positions: list[int] = []
        for position in comma_positions:
            left_len = len(rewritten[:position])
            right_len = len(rewritten[position + 1 :])
            if left_len < 28 or right_len < 28:
                continue
            if re.search(r"第[一二三四五六七八九十]$", rewritten[max(0, position - 3) : position]):
                continue
            tail = rewritten[position + 1 : position + 8]
            if any(tail.startswith(cue) for cue in SPLIT_CUES):
                candidate_positions.append(position)

        if candidate_positions:
            target = min(candidate_positions, key=lambda item: abs(item - len(rewritten) / 2))
        else:
            filtered = [
                item
                for item in comma_positions
                if not re.search(r"第[一二三四五六七八九十]$", rewritten[max(0, item - 3) : item])
            ]
            target = min(filtered or comma_positions, key=lambda item: abs(item - len(rewritten) / 2))

        rewritten = rewritten[:target] + "。" + rewritten[target + 1 :].lstrip("，, ")
    return rewritten


def apply_phrase_variation(text: str, profile: str) -> str:
    rewritten = text
    for pattern, replacement in COMMON_REPLACEMENTS:
        rewritten = pattern.sub(replacement, rewritten)

    rewritten = rewritten.replace("比如", "例如" if profile == "academic_safe" else "例如说")
    rewritten = rewritten.replace("举个例子", "例如" if profile == "academic_safe" else "例如说")

    if profile == "explicit_low_aigc":
        if rewritten.startswith("本文在"):
            rewritten = "在本文中，" + rewritten[3:]
        elif rewritten.startswith(("本文针对", "本文围绕", "本文完成", "本文对", "本文从", "本文所")):
            rewritten = "在本文中，" + rewritten[2:]
        elif rewritten.startswith("本文"):
            rewritten = "从本文的研究内容来看，" + rewritten
        elif rewritten.startswith("系统") or rewritten.startswith("该系统"):
            rewritten = "从系统实现角度看，" + rewritten

        rewritten = rewritten.replace("主要解决", "主要目的是解决")
        rewritten = rewritten.replace("提升", "提高")
    else:
        rewritten = rewritten.replace("主要解决", "重点解决")

    return rewritten


def ordered_unique(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def rewrite_text_by_recipe(
    text: str,
    recipes: Iterable[str],
    profile: str,
    *,
    normalize_typography_enabled: bool = False,
) -> str:
    if profile not in REWRITE_PROFILES:
        raise ValueError(f"Unsupported rewrite profile: {profile}")

    rewritten = text.strip()
    active_recipes = set(recipes)

    if RECIPE_BREAK_TEMPLATE in active_recipes:
        rewritten = rewrite_template_enumeration(rewritten, profile)
    if RECIPE_SPLIT_DENSE in active_recipes:
        rewritten = split_dense_sentence(rewritten, profile)
    if RECIPE_EXPAND_CONTEXT in active_recipes or RECIPE_ADD_QUALIFIER in active_recipes:
        rewritten = apply_phrase_variation(rewritten, profile)
    if normalize_typography_enabled or RECIPE_NORMALIZE in active_recipes:
        rewritten = normalize_typography(rewritten)

    rewritten = re.sub(r"(第[一二三四五六七八九十])。(?=[\u4e00-\u9fff])", r"\1，", rewritten)

    return rewritten
