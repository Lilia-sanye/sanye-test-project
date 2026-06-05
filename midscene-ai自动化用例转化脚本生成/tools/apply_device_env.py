#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 config/env.yaml 中的值注入 scripts/*.yaml 的 {{dot.key}} 占位符。

仓库约定：scripts 保留 {{}} 占位符；midscene run 前执行 --apply。
注释行（行首空白后以 # 开头）不参与替换，便于保留原步骤对照。

用法（仓库根目录）：
  python tools/apply_device_env.py --all
  python tools/apply_device_env.py --inject --all
  python tools/apply_device_env.py --file midscene自动化输出/scripts/地图界面_自动化测试.yaml
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / "midscene自动化输出" / "config" / "env.yaml"
SCRIPTS_DIR = ROOT / "midscene自动化输出" / "scripts"

DEFAULT_SCRIPTS = [
    "地图界面_自动化测试.yaml",
    "主界面_有地图无任务_自动化测试.yaml",
    "主界面_有地图有任务_自动化测试.yaml",
    "快速任务_自动化测试.yaml",
    "新建任务_自动化测试.yaml",
    "编辑任务_自动化测试.yaml",
    "界面设置与操作_自动化测试.yaml",
]

PLACEHOLDER_RE = re.compile(r"\{\{([a-zA-Z0-9_.]+)\}\}")


def load_env() -> dict[str, str]:
    if yaml is None:
        raise SystemExit("需要 PyYAML：pip install pyyaml")
    with ENV_PATH.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return flatten(data)


def flatten(obj: object, prefix: str = "") -> dict[str, str]:
    out: dict[str, str] = {}
    if not isinstance(obj, dict):
        return out
    for key, val in obj.items():
        if str(key).startswith("_"):
            continue
        dot = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(val, dict):
            out.update(flatten(val, dot))
        elif isinstance(val, list):
            out[dot] = "、".join(str(x) for x in val)
        elif val is not None:
            out[dot] = str(val)
    return out


def is_skipped_line(line: str) -> bool:
    """注释行不替换（保留原步骤字面量供对照）。"""
    stripped = line.lstrip()
    if stripped.startswith("#"):
        return True
    return False


def apply_placeholders(line: str, flat: dict[str, str]) -> str:
    def repl(m: re.Match[str]) -> str:
        k = m.group(1)
        return flat[k] if k in flat else m.group(0)

    return PLACEHOLDER_RE.sub(repl, line)


def inject_placeholders(line: str, flat: dict[str, str]) -> str:
    if is_skipped_line(line) or "{{" in line:
        return line
    stripped = line.lstrip()
    # task 名称、testId 等标识字段不参与反向注入，避免误改用例名
    if re.match(r"- name:\s", stripped) or re.match(r"(testId|groupName|groupDescription):", stripped):
        return line
    pairs = sorted(flat.items(), key=lambda x: -len(x[1]))
    for key, val in pairs:
        if not val or val == "<设备ID>":
            continue
        if val in line:
            line = line.replace(val, f"{{{{{key}}}}}", 1)
    return line


def process_file(path: Path, flat: dict[str, str], mode: str) -> int:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    n = 0
    out: list[str] = []
    for line in lines:
        if is_skipped_line(line):
            out.append(line)
            continue
        new = (
            apply_placeholders(line, flat)
            if mode == "apply"
            else inject_placeholders(line, flat)
        )
        if new != line:
            n += 1
        out.append(new)
    if n:
        path.write_text("".join(out), encoding="utf-8")
    return n


def main() -> None:
    ap = argparse.ArgumentParser(description="env.yaml ↔ scripts {{placeholders}}")
    ap.add_argument("--apply", action="store_true", help="{{key}} → 字面量（默认）")
    ap.add_argument("--inject", action="store_true", help="字面量 → {{key}}")
    ap.add_argument("--all", action="store_true", help="处理 DEFAULT_SCRIPTS 列表")
    ap.add_argument("--file", type=str, help="单个 script 相对或绝对路径")
    args = ap.parse_args()

    mode = "inject" if args.inject else "apply"
    flat = load_env()

    if args.file:
        paths = [Path(args.file)]
        if not paths[0].is_absolute():
            paths[0] = ROOT / paths[0]
    elif args.all:
        paths = [SCRIPTS_DIR / name for name in DEFAULT_SCRIPTS]
    else:
        ap.error("请指定 --all 或 --file")

    total = 0
    for p in paths:
        if not p.exists():
            print(f"跳过（不存在）: {p}")
            continue
        c = process_file(p, flat, mode)
        print(f"{mode} {p.name}: {c} 行")
        total += c
    print(f"完成，共 {total} 行变更")


if __name__ == "__main__":
    main()
