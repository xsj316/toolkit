#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dev-toolkit —— 面向开发者的 Python 命令行工具箱入口。

模块化结构，通过子命令调用 tools 子包下的各功能模块：

    rename     批量重命名文件
    dedupe     按内容查找重复文件
    tree       以树状结构打印目录
    password   生成随机强密码
    stats      统计文本文件指标

所有功能均基于 Python 标准库实现，无需安装第三方依赖即可运行。

使用示例:
    python main.py rename --path F:/tmp --prefix "备份_"
    python main.py dedupe --path F:/tmp --recursive
    python main.py tree --path F:/dev-toolkit --depth 3 --size
    python main.py password --length 20 --count 3
    python main.py stats --file README.md
"""

from __future__ import annotations

import argparse
import sys

from tools import dedupe, password, rename, textstats, tree


def main(argv: list[str] | None = None) -> int:
    """工具箱统一入口：注册子命令、解析参数并分发到对应工具模块。"""
    parser = argparse.ArgumentParser(
        prog="dev-toolkit",
        description="面向开发者的 Python 命令行工具箱",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="dev-toolkit 1.0.0"
    )

    # 各工具模块向 subparsers 注册自己的命令行参数
    subparsers = parser.add_subparsers(dest="command", metavar="<命令>")
    rename.add_parser(subparsers)
    dedupe.add_parser(subparsers)
    tree.add_parser(subparsers)
    password.add_parser(subparsers)
    textstats.add_parser(subparsers)

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0

    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
