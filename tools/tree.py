#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""目录树工具。

以树状结构打印目录内容，支持限制递归深度与显示文件大小。
"""

from __future__ import annotations

import argparse
from pathlib import Path


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """向主解析器注册 tree 子命令及其参数。"""
    p = subparsers.add_parser("tree", help="以树状结构打印目录")
    p.add_argument("--path", "-p", default=".", help="起始目录（默认当前目录）")
    p.add_argument("--depth", "-d", type=int, default=3, help="最大递归深度（默认 3）")
    p.add_argument("--size", action="store_true", help="显示文件大小")
    p.set_defaults(handler=run)
    return p


def _fmt_size(num: int) -> str:
    """将字节数格式化为易读的单位。"""
    for unit in ("B", "KB", "MB", "GB"):
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} TB"


def _walk(
    node: Path,
    prefix: str,
    depth: int,
    max_depth: int,
    show_size: bool,
    lines: list[str],
) -> None:
    """递归遍历目录并生成树状文本行。"""
    if depth > max_depth:
        return

    try:
        # 目录在前、文件在后，各自按名称排序
        children = sorted(node.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except PermissionError:
        lines.append(f"{prefix}└── [无权限访问]")
        return

    for i, child in enumerate(children):
        last = i == len(children) - 1
        branch = "└── " if last else "├── "
        connector = "    " if last else "│   "

        if child.is_dir():
            lines.append(f"{prefix}{branch}{child.name}/")
            _walk(child, prefix + connector, depth + 1, max_depth, show_size, lines)
        else:
            size = f"  ({_fmt_size(child.stat().st_size)})" if show_size else ""
            lines.append(f"{prefix}{branch}{child.name}{size}")


def run(args: argparse.Namespace) -> int:
    """打印目录树。"""
    root = Path(args.path)
    if not root.is_dir():
        print(f"[错误] 目录不存在: {root}")
        return 1

    lines = [f"{root}/"]
    _walk(root, "", 1, args.depth, args.size, lines)
    print("\n".join(lines))
    return 0
