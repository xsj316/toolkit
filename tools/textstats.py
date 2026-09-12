#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文本统计工具。

统计文本文件的总行数、非空行数、字符数（含/不含空白）、单词数、
最长行长度与文件字节数。自动尝试 UTF-8 与 GBK 编码。
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

# 匹配单词：英文单词 + 中文连续字符
WORD_RE = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """向主解析器注册 stats 子命令及其参数。"""
    p = subparsers.add_parser("stats", help="统计文本文件指标")
    p.add_argument("--file", "-f", required=True, help="文本文件路径")
    p.set_defaults(handler=run)
    return p


def run(args: argparse.Namespace) -> int:
    """读取文本文件并输出统计指标。"""
    path = Path(args.file)
    if not path.is_file():
        print(f"[错误] 文件不存在: {path}")
        return 1

    try:
        raw = path.read_bytes()
    except OSError as exc:
        print(f"[错误] 无法读取文件: {exc}")
        return 1

    # 尝试 UTF-8 解码，失败则回退到 GBK（Windows 常见中文编码）
    text: str | None = None
    for enc in ("utf-8", "gbk"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        print("[错误] 无法识别文件编码（已尝试 UTF-8 与 GBK）")
        return 1

    lines = text.splitlines()
    non_empty = [ln for ln in lines if ln.strip()]
    total_chars = len(text)
    no_space_chars = len(re.sub(r"\s", "", text))
    words = len(WORD_RE.findall(text))
    max_line_len = max((len(ln) for ln in lines), default=0)

    print(f"文件        : {path}")
    print(f"总行数      : {len(lines)}")
    print(f"非空行数    : {len(non_empty)}")
    print(f"字符数      : {total_chars}")
    print(f"去空白字符数: {no_space_chars}")
    print(f"单词数      : {words}")
    print(f"最长行长度  : {max_line_len}")
    print(f"文件大小    : {path.stat().st_size} 字节")
    return 0
