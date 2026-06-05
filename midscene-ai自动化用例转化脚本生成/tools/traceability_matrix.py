# -*- coding: utf-8 -*-
"""Build manual-case → Midscene YAML task traceability matrix."""
from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_NAME_RE = re.compile(r'^\s*-\s*name:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE)
DEFAULT_CSV = ROOT / "midscene自动化输出" / "cases" / "界面和任务设置_可自动化用例.csv"
DEFAULT_SCRIPTS = ROOT / "midscene自动化输出" / "scripts"
DEFAULT_OUT = ROOT / "midscene自动化输出" / "report"

CASE_ID_RE = re.compile(r"\b(\d{8})\b")
LEGACY_SUITE = "界面设置与操作_完整自动化测试.yaml"


def load_cases(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def extract_case_ids(task_name: str) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for m in CASE_ID_RE.finditer(task_name):
        cid = m.group(1)
        if cid not in seen:
            seen.add(cid)
            ordered.append(cid)
    return ordered


def parse_task_names(yaml_text: str) -> list[str]:
    names: list[str] = []
    for m in TASK_NAME_RE.finditer(yaml_text):
        name = m.group(1).strip().strip('"').strip("'")
        if name:
            names.append(name)
    return names


def scan_yaml_tasks(scripts_dir: Path, include_legacy: bool) -> dict[str, list[dict[str, str]]]:
    """case_id -> list of {suite, task, ids_in_name}"""
    mapping: dict[str, list[dict[str, str]]] = defaultdict(list)

    for ypath in sorted(scripts_dir.glob("*.yaml")):
        if ypath.name == LEGACY_SUITE and not include_legacy:
            continue
        text = ypath.read_text(encoding="utf-8")
        suite = ypath.name
        for name in parse_task_names(text):
            ids = extract_case_ids(name)
            entry = {"suite": suite, "task": name, "ids_in_name": ids}
            if ids:
                for cid in ids:
                    mapping[cid].append(entry)
            else:
                mapping.setdefault("__no_id__", []).append(entry)
    return mapping


def title_index(cases: list[dict[str, str]]) -> dict[str, str]:
    idx: dict[str, str] = {}
    for row in cases:
        cid = (row.get("用例ID") or "").strip()
        title = (row.get("用例标题") or "").strip()
        if cid and title:
            idx[normalize_title(title)] = cid
    return idx


def normalize_title(s: str) -> str:
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"[，。、；：""''（）\-\—\.\,\;\:\!\?]", "", s)
    return s.lower()


def match_legacy_by_title(
    cases: list[dict[str, str]],
    legacy_path: Path,
) -> dict[str, list[dict[str, str]]]:
    """Map case_id from 完整套件 tasks whose name equals 用例标题."""
    tidx = title_index(cases)
    by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    if not legacy_path.is_file():
        return by_id
    suite = legacy_path.name
    for name in parse_task_names(legacy_path.read_text(encoding="utf-8")):
        norm = normalize_title(name)
        cid = tidx.get(norm)
        if cid:
            by_id[cid].append(
                {"suite": suite, "task": name, "ids_in_name": [], "match": "title"}
            )
    return by_id


def merge_mappings(
    primary: dict[str, list[dict[str, str]]],
    legacy: dict[str, list[dict[str, str]]],
) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = defaultdict(list)
    for key, items in primary.items():
        out[key].extend(items)
    for cid, items in legacy.items():
        existing = {(x["suite"], x["task"]) for x in out[cid]}
        for item in items:
            key = (item["suite"], item["task"])
            if key not in existing:
                out[cid].append(item)
    return out


def dedupe_entries(items: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, str]] = []
    for it in items:
        key = (it["suite"], it["task"])
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out


def status_for(
    tier: str,
    entries: list[dict[str, str]],
) -> str:
    if entries:
        suites = {e["suite"] for e in entries}
        if len(suites) > 1 or len(entries) > 1:
            return "已覆盖(多套件)"
        return "已覆盖"
    if tier == "B":
        return "B档-未写YAML"
    if tier == "A":
        return "A档-待转化"
    return "未覆盖"


def render_markdown(
    stem: str,
    cases: list[dict[str, str]],
    mapping: dict[str, list[dict[str, str]]],
    no_id_tasks: list[dict[str, str]],
    include_legacy: bool,
    scripts_dir: Path,
) -> str:
    today = date.today().isoformat()
    tiers = Counter((r.get("执行档位") or "").strip() for r in cases)

    covered_a = 0
    pending_a = 0
    covered_b = 0
    pending_b = 0

    rows_by_tier: dict[str, list[str]] = defaultdict(list)

    for row in sorted(cases, key=lambda r: (r.get("执行档位") or "", r.get("用例ID") or "")):
        cid = (row.get("用例ID") or "").strip()
        tier = (row.get("执行档位") or "").strip()
        title = (row.get("用例标题") or "").strip()
        entries = dedupe_entries(mapping.get(cid, []))
        status = status_for(tier, entries)

        if tier == "A":
            if entries:
                covered_a += 1
            else:
                pending_a += 1
        elif tier == "B":
            if entries:
                covered_b += 1
            else:
                pending_b += 1

        if entries:
            loc = "<br>".join(
                f"`{e['suite']}` → `{e['task'][:60]}{'…' if len(e['task']) > 60 else ''}`"
                for e in entries
            )
        else:
            loc = "—"

        rows_by_tier[tier].append(
            f"| {cid} | {title[:40]}{'…' if len(title) > 40 else ''} | {status} | {loc} |"
        )

    total_tasks = sum(
        len(dedupe_entries(v)) for k, v in mapping.items() if k != "__no_id__"
    )
    id_in_tasks = len([k for k in mapping if k != "__no_id__" and mapping[k]])

    lines = [
        f"# {stem} — 自动化追溯矩阵",
        "",
        f"> 生成日期：{today}  ",
        f"> 源表：`midscene自动化输出/cases/{stem}_可自动化用例.csv`  ",
        f"> 扫描目录：`{scripts_dir.as_posix()}/`（{'含' if include_legacy else '不含'} `{LEGACY_SUITE}`）",
        "",
        "## 汇总",
        "",
        "| 指标 | 数量 |",
        "|------|------|",
        f"| CSV 行数（A+B） | {len(cases)} |",
        f"| A 档 | {tiers.get('A', 0)} |",
        f"| B 档 | {tiers.get('B', 0)} |",
        f"| A 档已出现在终稿 task 名中 | {covered_a} |",
        f"| A 档待转化 | {pending_a} |",
        f"| B 档已有 YAML 追溯 | {covered_b} |",
        f"| B 档未写 YAML | {pending_b} |",
        f"| 终稿中带用例ID的 task 映射键 | {id_in_tasks} |",
        f"| 终稿 task 条数（去重 suite+name） | {total_tasks} |",
        f"| 无 8 位用例ID 前缀的 task | {len(no_id_tasks)} |",
        "",
        "**说明**：task `name` 以 `12901234-` 或 `12901234-12901235-` 形式书写时，视为已追溯；仅 `DESIGN-` / `PARAM-` 前缀的 task 见文末附录。",
        "",
    ]

    for tier in ("A", "B", "C"):
        if tier not in rows_by_tier:
            continue
        lines.extend(
            [
                f"## {tier} 档明细",
                "",
                "| 用例ID | 用例标题 | 状态 | 套件 / task |",
                "|--------|----------|------|-------------|",
                *rows_by_tier[tier],
                "",
            ]
        )

    if no_id_tasks:
        lines.extend(
            [
                "## 附录：终稿中无 8 位用例ID 的 task",
                "",
                "多为设计稿补充（DESIGN）或参数页流程（PARAM），需在套件说明中人工对照需求。",
                "",
                "| 套件 | task name |",
                "|------|-----------|",
            ]
        )
        for t in no_id_tasks:
            lines.append(f"| `{t['suite']}` | `{t['task']}` |")
        lines.append("")

    multi = [
        (cid, dedupe_entries(items))
        for cid, items in mapping.items()
        if cid != "__no_id__" and len(dedupe_entries(items)) > 1
    ]
    if multi:
        lines.extend(
            [
                "## 附录：同一用例ID 对应多个 task",
                "",
                "| 用例ID | 套件 / task |",
                "|--------|-------------|",
            ]
        )
        for cid, items in sorted(multi, key=lambda x: x[0]):
            loc = "<br>".join(f"`{e['suite']}` → `{e['task'][:50]}…`" if len(e["task"]) > 50 else f"`{e['suite']}` → `{e['task']}`" for e in items)
            lines.append(f"| {cid} | {loc} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("重新生成：`python tools/traceability_matrix.py`")
    return "\n".join(lines)


def write_trace_csv(
    out_path: Path,
    cases: list[dict[str, str]],
    mapping: dict[str, list[dict[str, str]]],
) -> None:
    fieldnames = [
        "用例ID",
        "用例标题",
        "执行档位",
        "自动化状态",
        "套件文件",
        "task名称",
    ]
    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in cases:
            cid = (row.get("用例ID") or "").strip()
            tier = (row.get("执行档位") or "").strip()
            entries = dedupe_entries(mapping.get(cid, []))
            status = status_for(tier, entries)
            if entries:
                for e in entries:
                    w.writerow(
                        {
                            "用例ID": cid,
                            "用例标题": row.get("用例标题", ""),
                            "执行档位": tier,
                            "自动化状态": status,
                            "套件文件": e["suite"],
                            "task名称": e["task"],
                        }
                    )
            else:
                w.writerow(
                    {
                        "用例ID": cid,
                        "用例标题": row.get("用例标题", ""),
                        "执行档位": tier,
                        "自动化状态": status,
                        "套件文件": "",
                        "task名称": "",
                    }
                )


def main() -> None:
    ap = argparse.ArgumentParser(description="Build Midscene traceability matrix")
    ap.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    ap.add_argument("--scripts-dir", type=Path, default=DEFAULT_SCRIPTS)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    ap.add_argument(
        "--include-legacy",
        action="store_true",
        help=f"Also match tasks in {LEGACY_SUITE} by 用例标题",
    )
    args = ap.parse_args()

    csv_path = args.csv.resolve()
    stem = csv_path.stem.replace("_可自动化用例", "")
    cases = load_cases(csv_path)
    mapping = scan_yaml_tasks(args.scripts_dir, include_legacy=False)

    if args.include_legacy:
        legacy_path = args.scripts_dir / LEGACY_SUITE
        legacy_map = match_legacy_by_title(cases, legacy_path)
        mapping = merge_mappings(mapping, legacy_map)

    no_id = dedupe_entries(mapping.pop("__no_id__", []))

    md = render_markdown(
        stem, cases, mapping, no_id, args.include_legacy, args.scripts_dir
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)
    md_path = args.out_dir / f"{stem}_自动化追溯矩阵.md"
    md_path.write_text(md, encoding="utf-8")

    csv_out = args.out_dir / f"{stem}_自动化追溯矩阵.csv"
    write_trace_csv(csv_out, cases, mapping)

    print(f"Wrote {md_path}")
    print(f"Wrote {csv_out}")
    a_pending = sum(
        1
        for r in cases
        if (r.get("执行档位") or "").strip() == "A"
        and not dedupe_entries(mapping.get((r.get("用例ID") or "").strip(), []))
    )
    print(f"A-tier pending: {a_pending}")


if __name__ == "__main__":
    main()
