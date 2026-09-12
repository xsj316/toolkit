#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量重命名工具。

支持为目录下的文件统一添加前缀 / 后缀、替换文件名中的文本，
以及添加三位数字顺序编号。

安全设计：
    默认仅打印预览，不实际改动任何文件；只有显式传入 --apply
    才会真正执行重命名。执行前会做目标名冲突检测，冲突文件自动跳过，
    避免覆盖已有文件。
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """向主解析器注册 rename 子命令及其参数。"""
    p = subparsers.add_parser("rename", help="批量重命名文件")
    p.add_argument("--path", "-p", required=True, help="要处理的目录")
    p.add_argument("--prefix", default="", help="新文件名前缀")
    p.add_argument("--suffix", default="", help="新文件名后缀（插在扩展名之前）")
    p.add_argument(
        "--replace",
        nargs=2,
        metavar=("OLD", "NEW"),
        help="将文件名中的 OLD 文本替换为 NEW",
    )
    p.add_argument("--seq", action="store_true", help="添加三位数字顺序前缀")
    p.add_argument(
        "--apply",
        action="store_true",
        help="真正执行重命名；不指定则只做预览",
    )
    p.set_defaults(handler=run)
    return p


def build_new_name(
    name: str,
    prefix: str = "",
    suffix: str = "",
    replace: tuple[str, str] | None = None,
    seq: int | None = None,
) -> str:
    """根据重命名规则计算新文件名（不含目录部分）。

    规则顺序：替换文本 -> 顺序编号 -> 前缀 -> 后缀（位于扩展名前）。
    """
    stem, ext = os.path.splitext(name)

    new = stem
    if replace:
        old, new_text = replace
        new = new.replace(old, new_text)

    head = prefix
    if seq is not None:
        head += f"{seq:03d}_"

    return f"{head}{new}{suffix}{ext}"


def run(args: argparse.Namespace) -> int:
    """执行批量重命名：先预览，--apply 时真正改名。"""
    root = Path(args.path)
    if not root.is_dir():
        print(f"[错误] 目录不存在: {root}")
        return 1

    # 仅处理顶层普通文件
    files = sorted(f for f in root.iterdir() if f.is_file())
    if not files:
        print(f"[提示] 目录中没有文件: {root}")
        return 0

    # 生成 (原文件, 新文件名) 计划，并跟踪已占用的目标路径
    planned_targets: set[Path] = set()
    renamed = 0
    skipped = 0

    for i, f in enumerate(files, start=1):
        new_name = build_new_name(
            f.name,
            prefix=args.prefix,
            suffix=args.suffix,
            replace=tuple(args.replace) if args.replace else None,
            seq=i if args.seq else None,
        )
        if new_name == f.name:
            continue  # 名字未变化，跳过

        target = f.with_name(new_name)

        # 冲突检测：与其它计划目标或磁盘上已有文件重名则跳过
        if target in planned_targets or target.exists():
            print(f"[跳过] 目标名冲突: {f.name}  ->  {new_name}")
            skipped += 1
            continue

        planned_targets.add(target)
        action = "执行" if args.apply else "预览"
        print(f"[{action}] {f.name}  ->  {new_name}")
        if args.apply:
            f.rename(target)
        renamed += 1

    print(f"[完成] 共 {len(files)} 个文件：重命名 {renamed} 个，跳过 {skipped} 个"
          f"（{'已落盘' if args.apply else '仅预览，未改动文件，加 --apply 生效'}）。")
    return 0
