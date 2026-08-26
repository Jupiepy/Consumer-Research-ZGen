#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Xiaohongshu (RED) comment text mining for the Z-Gen "pretty food" study.

Pipeline
--------
1. Load comments from an Excel/CSV file (default column: ``评论内容``).
2. Clean text -- strip @mentions, emoji, URLs and stray whitespace.
3. Tokenize with jieba, drop stopwords.
4. Word-frequency analysis.
5. Rule-based sentiment scoring (transparent domain lexicon + negation).

Outputs (written to ``--output-dir``)
--------------------------------------
* ``word_frequency.csv``    top-N tokens by count
* ``sentiment_results.csv`` per-comment sentiment label and score
* ``summary.json``          aggregate statistics

Usage
-----
::

    py analysis/text_mining.py --input data/red_comments.xlsx
    py analysis/text_mining.py --input data/red_comments.xlsx --top 40 --output-dir output

Note on the crawler: the collection step is intentionally not published (RED
Terms of Service + comment privacy). This module covers the reproducible part --
the analysis of already-collected comments.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import jieba
import pandas as pd

# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #

COMMENT_COLUMN = "评论内容"

# Domain terms so jieba does not over-split them into single characters.
_DOMAIN_TERMS = (
    "漂亮饭", "出片", "氛围感", "情绪价值", "打卡", "宝藏店", "探店",
    "颜值", "拍照", "想吃", "想去", "好吃", "好看", "好美", "好漂亮",
    "不好吃", "不健康", "避雷", "价格侠", "搭子", "海鲜饭", "鹅肝",
)
for _term in _DOMAIN_TERMS:
    jieba.add_word(_term)

STOPWORDS = {
    "的", "了", "我", "你", "他", "她", "它", "我们", "你们", "他们",
    "是", "在", "有", "和", "就", "都", "也", "还", "很", "好",
    "这", "那", "这个", "那个", "这些", "那些", "啊", "呀", "哦",
    "呢", "吧", "吗", "嘛", "啦", "哈", "哈哈", "哈哈哈", "一下",
    "一个", "什么", "怎么", "哪里", "哪", "就是", "真的", "感觉",
    "觉得", "现在", "然后", "但是", "所以", "因为", "或者", "还是",
    "可以", "没有", "不是", "太", "挺", "有点", "一些", "这家",
    "那边", "这里", "那里", "博主", "姐妹", "朋友", "关注", "求求",
    "孩子", "明天", "今天", "回来", "去过", "吃过", "吃", "店",
    "家", "店名", "地址", "位置", "人均", "价格", "多少钱", "价位",
    "均价", "在哪", "哪里", "求", "个", "到", "去", "来", "要",
    "想", "多少", "还有", "看起来", "那么", "让", "被", "一下",
    "这样", "那样", "一样", "已经", "之前", "之后", "时候", "可以",
    "叫", "过", "又", "钱", "下次", "饭", "多少钱", "就是", "还是",
    "说", "给", "看",
}

# Transparent domain lexicon. Each word maps to a signed sentiment score.
# Replace or extend freely -- this is a baseline, not a black-box model.
POSITIVE_WORDS = {
    "好吃", "好美", "好看", "好漂亮", "漂亮", "美", "香", "嫩", "爱",
    "爱吃", "想吃", "喜欢", "推荐", "宝藏", "出片", "氛围感", "食欲",
    "心动", "值得", "惊艳", "嘎嘎", "哇塞", "绝", "幸福", "治愈",
    "满意", "美味", "精致", "高级", "赞", "给力", "离不开", "招牌",
    "不错", "颜值高", "可爱", "好看",
}

NEGATIVE_WORDS = {
    "难吃", "贵", "好贵", "贵死", "避雷", "恶心", "窜", "差", "一般",
    "不推荐", "歇业", "关门", "开不下去", "心停", "遗憾", "失望",
    "不怎么样", "不习惯", "少", "饿肚子", "找不到", "急死", "不好吃",
    "不健康", "不好看", "要死", "太冷", "冷",
}

NEGATIONS = {"不", "没", "别", "无", "非", "未"}

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"   # emoji & pictographs
    "\U00002600-\U000027BF"   # misc symbols / dingbats
    "\U0001F000-\U0001F0FF"
    "️"                   # variation selector
    "]+",
    flags=re.UNICODE,
)
MENTION_PATTERN = re.compile(r"@[\w一-鿿-]+")
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
# RED emoji shortcodes such as [呃R], [微笑], [暗中观察R].
SHORTCODE_PATTERN = re.compile(r"\[[^\[\]]{1,8}\]")
PUNCT_DIGIT_PATTERN = re.compile(r"^[\W\d_]+$")


# --------------------------------------------------------------------------- #
# Text helpers
# --------------------------------------------------------------------------- #

def clean_text(text: str) -> str:
    """Strip mentions, URLs and emoji; collapse whitespace."""
    if not isinstance(text, str):
        return ""
    text = MENTION_PATTERN.sub(" ", text)
    text = URL_PATTERN.sub(" ", text)
    text = EMOJI_PATTERN.sub(" ", text)
    text = SHORTCODE_PATTERN.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> list[str]:
    """Tokenize and drop stopwords / pure punctuation tokens."""
    tokens = []
    for tok in jieba.cut(text):
        tok = tok.strip()
        if not tok:
            continue
        if tok in STOPWORDS:
            continue
        if PUNCT_DIGIT_PATTERN.match(tok):
            continue
        tokens.append(tok)
    return tokens


# --------------------------------------------------------------------------- #
# Analysis
# --------------------------------------------------------------------------- #

def word_frequency(tokens_by_comment: list[list[str]], top: int) -> pd.DataFrame:
    """Aggregate token counts across all comments, keep the top-N.

    Negation tokens ("不", "没", …) are skipped here -- they matter for sentiment
    scoring but are pure noise in a frequency table.
    """
    counter: Counter = Counter()
    for tokens in tokens_by_comment:
        for tok in tokens:
            if tok in NEGATIONS:
                continue
            counter[tok] += 1
    rows = [{"词": word, "词频": count} for word, count in counter.most_common(top)]
    return pd.DataFrame(rows)


def score_sentiment(tokens: list[str]) -> tuple[int, str]:
    """Rule-based sentiment score.

    A negation immediately before a sentiment word flips its sign; the label is
    derived from the summed score (``positive`` / ``negative`` / ``neutral``).
    """
    score = 0
    negate_next = False

    for tok in tokens:
        if tok in NEGATIONS:
            negate_next = True
            continue

        polarity = 0
        if tok in POSITIVE_WORDS:
            polarity = 1
        elif tok in NEGATIVE_WORDS:
            polarity = -1

        if polarity:
            score += -polarity if negate_next else polarity
            negate_next = False

    if score > 0:
        label = "正面"
    elif score < 0:
        label = "负面"
    else:
        label = "中性"
    return score, label


# --------------------------------------------------------------------------- #
# IO
# --------------------------------------------------------------------------- #

def load_comments(path: Path, column: str) -> list[str]:
    """Load the comment column from an Excel or CSV file."""
    if path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    if column not in df.columns:
        raise ValueError(f"列 '{column}' 不存在，实际列名: {list(df.columns)}")
    return df[column].dropna().astype(str).tolist()


def write_outputs(output_dir: Path, top: int,
                  comments: list[str], tokens_by_comment: list[list[str]],
                  freq_df: pd.DataFrame, results: list[dict]) -> None:
    """Persist word frequency, per-comment sentiment and summary."""
    output_dir.mkdir(parents=True, exist_ok=True)

    freq_df.to_csv(output_dir / "word_frequency.csv", index=False, encoding="utf-8-sig")

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_dir / "sentiment_results.csv", index=False, encoding="utf-8-sig")

    labels = results_df["情感倾向"]
    counts = labels.value_counts().to_dict()
    total = len(comments)
    pos = int(counts.get("正面", 0))
    neg = int(counts.get("负面", 0))
    neu = int(counts.get("中性", 0))
    summary = {
        "评论总数": total,
        "正面": pos,
        "负面": neg,
        "中性": neu,
        "正面占比": round(pos / total, 4) if total else 0.0,
        "正面占(正面+负面)": round(pos / (pos + neg), 4) if (pos + neg) else 0.0,
        "top词": freq_df.head(top).to_dict("records"),
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="小红书漂亮饭评论分词 / 词频 / 情感分析")
    parser.add_argument("--input", required=True, help="评论数据文件 (.xlsx 或 .csv)")
    parser.add_argument("--column", default=COMMENT_COLUMN, help="评论列名")
    parser.add_argument("--top", type=int, default=30, help="词频表保留的前 N 个词")
    parser.add_argument("--output-dir", default="output", help="结果输出目录")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    comments = load_comments(input_path, args.column)
    cleaned = [clean_text(c) for c in comments]
    tokens_by_comment = [tokenize(c) for c in cleaned]

    freq_df = word_frequency(tokens_by_comment, args.top)

    results = []
    for raw, tokens in zip(comments, tokens_by_comment):
        score, label = score_sentiment(tokens)
        results.append({"原文": raw, "情感得分": score, "情感倾向": label})

    summary = write_outputs(output_dir, args.top, comments, tokens_by_comment, freq_df, results)

    print(f"载入评论: {len(comments)} 条")
    print(f"情感分布: 正面 {summary['正面']} | 负面 {summary['负面']} | 中性 {summary['中性']}")
    print(f"正面占比: {summary['正面占比']:.1%}")
    print(f"\nTop-10 高频词:")
    for row in freq_df.head(10).itertuples(index=False):
        print(f"  {row[0]:<8} {row[1]}")
    print(f"\n结果已写入: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
