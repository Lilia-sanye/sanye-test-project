# -*- coding: utf-8 -*-
"""Build Midscene final YAML from screened CSV (P0 A-tier by default)."""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINAL_DIR = ROOT / "midscene自动化输出" / "scripts"


def parse_steps(steps: str) -> list[str]:
    steps = (steps or "").replace("\r\n", "\n").strip()
    if not steps:
        return []
    lines: list[str] = []
    for part in re.split(r"\n+", steps):
        part = part.strip()
        part = re.sub(r"^\d+[、.]\s*", "", part)
        part = re.sub(r"^\d+\s*", "", part)
        part = part.lstrip("、.． ")
        if len(part) >= 2:
            lines.append(part)
    return lines[:10]


def parse_assert(expect: str) -> str:
    if not expect:
        return "页面显示与用例预期一致"
    for line in expect.replace("\r\n", "\n").split("\n"):
        line = line.strip()
        while True:
            n = re.sub(r"^\d+[、.]\s*", "", line).lstrip("、.． ")
            if n == line:
                break
            line = n
        if len(line) >= 4:
            return line[:120]
    return expect.strip()[:120]


def yaml_quote(s: str) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def build_flow(case: dict) -> list[str]:
    flow: list[str] = []
    for step in parse_steps(case.get("步骤描述", "")):
        flow.append(f"ai: {yaml_quote(step)}")
    if not flow:
        flow.append(f"ai: {yaml_quote(case.get('用例标题', '执行用例')[:80])}")
    flow.append(f"aiAssert: {yaml_quote(parse_assert(case.get('预期结果', '')))}")
    return flow


def build_yaml(cases: list[dict], *, suite_id: str, group: str, ai_context: str) -> str:
    lines = [
        "# 终稿：由 build_midscene_yaml.py 生成（P0 A 档）",
        "# 执行前填写 android.deviceId；审阅 aiActContext",
        "config:",
        "  ai:",
        "    actionTimeout: 30000",
        "    retryInterval: 200",
        "  page:",
        "    defaultWait: 200",
        "",
        "android:",
        '  deviceId: "<设备ID>"',
        '  androidAdbPath: "D:/soft/android-sdk/platform-tools/adb.exe"',
        "",
        "agent:",
        f"  testId: {yaml_quote(suite_id)}",
        f"  groupName: {yaml_quote(group)}",
        "  generateReport: true",
        "  autoPrintReportMsg: true",
        f"  aiActContext: {yaml_quote(ai_context)}",
        "",
        "tasks:",
    ]
    for case in cases:
        title = case.get("用例标题", "未命名")[:40].replace('"', "'")
        name = f"{case.get('用例ID', '')}-{title}"
        lines.append(f"  - name: {yaml_quote(name)}")
        lines.append("    repeat: 1")
        lines.append("    flow:")
        for step in build_flow(case):
            # build_flow returns full line like 'ai: "..."'
            lines.append(f"      - {step}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def load_filtered_csv(
    path: Path,
    *,
    level: str | None = "P0",
    tier: str | None = "A",
) -> list[dict]:
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig")))
    out = []
    for r in rows:
        if level and r.get("等级") != level:
            continue
        if tier and r.get("执行档位") != tier:
            continue
        out.append(r)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv",
        type=Path,
        default=ROOT / "midscene自动化输出" / "cases" / "界面和任务设置_可自动化用例.csv",
    )
    parser.add_argument("--out", type=Path, default=FINAL_DIR / "界面设置与操作_自动化测试.yaml")
    parser.add_argument("--level", default="P0")
    parser.add_argument("--tier", default="A")
    parser.add_argument("--suite-id", default="界面设置与操作-P0-A")
    parser.add_argument("--group", default="界面操作和任务设置")
    args = parser.parse_args()

    cases = load_filtered_csv(args.csv, level=args.level or None, tier=args.tier or None)
    if not cases:
        raise SystemExit("无匹配用例，请检查 CSV 与筛选条件")

    ctx = (
        "权限弹窗点击允许；更新提示点击跳过；确认对话框点击确认；"
        "若出现引导页按提示关闭"
    )
    text = build_yaml(cases, suite_id=args.suite_id, group=args.group, ai_context=ctx)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"tasks={len(cases)} -> {args.out}")


if __name__ == "__main__":
    main()
