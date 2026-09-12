

# dev-toolkit

面向开发者的 Python 命令行工具箱，模块化设计，全部基于 Python 标准库实现，
无需安装任何第三方依赖即可运行。

## 功能总览

| 命令 | 说明 |
| --- | --- |
| `rename` | 批量重命名文件（前缀 / 后缀 / 文本替换 / 顺序编号） |
| `dedupe` | 按文件内容哈希查找重复文件 |
| `tree` | 以树状结构打印目录 |
| `password` | 生成随机强密码（密码学安全随机源） |
| `stats` | 统计文本文件的行数、字符数、单词数等指标 |

## 目录结构

```
F:\dev-toolkit\
├── main.py                 # 命令行入口
├── requirements.txt        # 依赖清单（当前为标准库，零依赖）
├── README.md               # 本文档
└── tools\                  # 工具子包
    ├── __init__.py
    ├── rename.py           # 批量重命名
    ├── dedupe.py           # 文件去重
    ├── tree.py             # 目录树
    ├── password.py         # 密码生成
    └── textstats.py        # 文本统计
```

## 使用示例

查看帮助：

```bash
python main.py --help
python main.py rename --help
```

### 1. 批量重命名

给 F:\tmp 下的所有文件添加前缀（先预览再落盘，安全）：

```bash
python main.py rename --path F:\tmp --prefix "备份_"
python main.py rename --path F:\tmp --prefix "备份_" --apply
```

添加顺序编号与后缀：

```bash
python main.py rename --path F:\tmp --seq --suffix "_v2" --apply
```

替换文件名中的文本（如将 "draft" 替换为 "final"）：

```bash
python main.py rename --path F:\tmp --replace draft final --apply
```

### 2. 查找重复文件

扫描 F:\tmp 下所有文件（含子目录），按内容 MD5 分组找出重复项。
本工具只发现不删除，由用户手动决定保留哪份：

```bash
python main.py dedupe --path F:\tmp --recursive
```

### 3. 打印目录树

```bash
python main.py tree --path F:\dev-toolkit
python main.py tree --path F:\dev-toolkit --depth 3 --size
```

### 4. 生成随机强密码

生成 5 个长度为 20 的密码（默认包含大小写字母、数字、符号）：

```bash
python main.py password --length 20 --count 5
```

只要数字和字母、去掉特殊符号：

```bash
python main.py password --length 24 --no-symbols
```

### 5. 统计文本文件

```bash
python main.py stats --file README.md
```

## 环境要求

- Python 3.9 及以上
- Windows / Linux / macOS 均可运行

## 运行验证

```bash
python main.py --help          # 确认入口正常
python main.py password -l 16  # 确认各子命令正常
```
*（内容由AI生成，仅供参考）*
