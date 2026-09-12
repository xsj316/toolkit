#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文件去重工具。

按文件内容 MD5 哈希分组，找出内容完全相同的重复文件并分组展示。

安全设计：
    本工具只负责“发现”重复文件，绝不自动删除任何文件；
    由用户根据输出结果自行决定保留哪个、删除哪个。
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

CHUNK_SIZE = 1024 * 1024  # 分块读取大小：1MB，节省内存


def file_md5(path: Path) -> str:
    """计算文件的 MD5 哈希值（分块读取，适用于大文件）。"""
    h = hashlib.md5()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(CHUNK_SIZE), b""):
            h.update(block)
    return h.hexdigest()


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """向主解析器注册 dedupe 子命令及其参数。"""
    p = subparsers.add_parser("dedupe", help="按内容查找重复文件")
    p.add_argument("--path", "-p", required=True, help="要扫描的目录")
    p.add_argument(
        "--recursive", "-r", action="store_true", help="递归扫描子目录"
    )
    p.set_defaults(handler=run)
    return p


def run(args: argparse.Namespace) -> int:
    """扫描目录并按内容哈希分组，输出重复文件清单。"""
    root = Path(args.path)
    if not root.is_dir():
        print(f"[错误] 目录不存在: {root}")
        return 1

    # 收集待扫描文件列表
    if args.recursive:
        candidates = [f for f in root.rglob("*") if f.is_file()]
    else:
        candidates = [f for f in root.iterdir() if f.is_file()]

    if not candidates:
        print(f"[提示] 目录中没有文件: {root}")
        return 0

    # 按 MD5 分组
    groups: dict[str, list[Path]] = {}
    for f in candidates:
        groups.setdefault(file_md5(f), []).append(f)

    dup_groups = {h: v for h, v in groups.items() if len(v) > 1}
    if not dup_groups:
        print(f"[结果] 扫描 {len(candidates)} 个文件，未发现重复文件。")
        return 0

    print(f"[结果] 扫描 {len(candidates)} 个文件，发现 {len(dup_groups)} 组重复文件：\n")
    for h, paths in dup_groups.items():
        size = paths[0].stat().st_size
        print(f"  ┌ 哈希 {h[:12]}...  大小 {size} 字节（{len(paths)} 份）")
        for p in paths:
            print(f"  │   {p}")
        print("  └ 建议仅保留其中一份\n")

    print("本工具不自动删除文件，请根据上述结果手动处理。")
    return 0
