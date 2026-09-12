#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""随机强密码生成工具。

使用 secrets 模块（密码学安全随机源）生成随机密码，可用于账号、
服务凭据等安全场景。字符集可配置：大写字母 / 小写字母 / 数字 / 特殊符号。
"""

from __future__ import annotations

import argparse
import secrets
import string

# 特殊符号字符集（避开易混淆字符）
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    """向主解析器注册 password 子命令及其参数。"""
    p = subparsers.add_parser("password", help="生成随机强密码")
    p.add_argument("--length", "-l", type=int, default=16, help="密码长度（默认 16）")
    p.add_argument("--count", "-c", type=int, default=1, help="生成数量（默认 1）")
    p.add_argument("--no-upper", action="store_true", help="不含大写字母")
    p.add_argument("--no-lower", action="store_true", help="不含小写字母")
    p.add_argument("--no-digits", action="store_true", help="不含数字")
    p.add_argument("--no-symbols", action="store_true", help="不含特殊符号")
    p.set_defaults(handler=run)
    return p


def generate(
    length: int,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """生成一个指定长度的随机密码。"""
    pool = ""
    if use_lower:
        pool += string.ascii_lowercase
    if use_upper:
        pool += string.ascii_uppercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += SYMBOLS

    if not pool:
        raise ValueError("字符集为空，至少需要保留一类字符")

    # secrets.choice 为密码学安全随机，避免使用可预测的 random 模块
    return "".join(secrets.choice(pool) for _ in range(length))


def run(args: argparse.Namespace) -> int:
    """按参数批量生成并打印密码。"""
    if args.length < 4:
        print("[错误] 密码长度至少为 4")
        return 1
    if args.count < 1:
        print("[错误] 生成数量至少为 1")
        return 1

    try:
        for _ in range(args.count):
            pwd = generate(
                args.length,
                use_upper=not args.no_upper,
                use_lower=not args.no_lower,
                use_digits=not args.no_digits,
                use_symbols=not args.no_symbols,
            )
            print(pwd)
    except ValueError as exc:
        print(f"[错误] {exc}")
        return 1
    return 0
