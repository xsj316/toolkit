#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dev-toolkit 的 tools 子包。

集中存放各类开发辅助工具的模块，每个模块提供一个命令行子命令：
    rename     批量重命名文件
    dedupe     按内容查找重复文件
    tree       以树状结构打印目录
    password   生成随机强密码
    stats      统计文本文件指标

每个模块约定暴露两个接口：
    add_parser(subparsers)  向主解析器注册子命令参数
    run(args)               执行该工具的核心逻辑并返回退出码
"""

__all__ = ["rename", "dedupe", "tree", "password", "textstats"]
