# Midscene 自动化产出目录

**唯一根目录**：本文件夹收纳筛选 → 精修 → 执行 的全部 Midscene 产物。  
勿再在根目录外分散存放 cases / 报告 / 草稿（旧 `output/` 已废弃，见 [../output/README.md](../output/README.md)）。

## 目录一览（仅 4 层）

```
midscene自动化输出/
├── README.md          ← 本说明（入口）
├── config/env.yaml    ← 实机文案变量（单文件分节）
├── cases/             ← 筛选 CSV（含「执行档位」）
├── report/            ← 筛选报告、依赖分析、套件说明、Figma 对照
├── drafts/            ← 机械草稿 YAML（须审阅，不可直接 run）
└── scripts/           ← 终稿 YAML（midscene run 只用此目录）
```

## 各目录做什么

| 目录 | 内容 | 命名示例 | 谁写入 | 能否 `midscene run` |
|------|------|----------|--------|---------------------|
| **cases/** | 可自动化 / B档 / 不可自动化 / 共享步骤 CSV | `<stem>_可自动化用例.csv` | `tools/screen_ui_task_cases.py` | — |
| **report/** | 筛选报告、依赖分析、Figma 对照、套件说明、**追溯矩阵** | `<stem>_筛选报告.md`、`<stem>_自动化追溯矩阵.md/.csv` | 筛选脚本 + `traceability_matrix.py` + Agent | — |
| **drafts/** | P0+A 机械草稿（≤15 task） | `<stem>_自动化测试_草稿.yaml` | 筛选脚本 | ❌ |
| **scripts/** | 人工精修终稿 | `<页面>_自动化测试.yaml` | Agent / `build_midscene_yaml.py` + 精修 | ✅ |

`<stem>` = 源 xlsx/csv 文件名（无扩展名），如 `界面和任务设置`。

## 推荐流水线

```
修订版本/<用例>.xlsx
    ↓  python tools/screen_ui_task_cases.py
cases/ + report/ + drafts/
    ↓  评审 cases 中「执行档位」（A 档写终稿）
    ↓  Agent 精修 或  build_midscene_yaml.py → 再改
scripts/<套件>_自动化测试.yaml
    ↓  python tools/apply_device_env.py --all   # 注入 config/env.yaml
    ↓  midscene run scripts/...
    ↓  traceability_matrix.py（更新覆盖追溯）
```

## 常用命令（仓库根目录）

```bash
# ① 筛选
python tools/screen_ui_task_cases.py --input "修订版本/界面和任务设置.xlsx"

# ② 机械终稿（仍须精修）
python tools/build_midscene_yaml.py \
  --csv midscene自动化输出/cases/界面和任务设置_可自动化用例.csv \
  --out midscene自动化输出/scripts/界面设置与操作_自动化测试.yaml

# ③ 追溯矩阵（精修 YAML 后重跑）
python tools/traceability_matrix.py

# ④ 环境变量（换台架改 config/env.yaml，run 前必做）
python tools/apply_device_env.py --all

# ⑤ 执行
midscene run midscene自动化输出/scripts/快速任务_自动化测试.yaml
```

**追溯矩阵**：扫描 `scripts/*.yaml` 中 task `name` 里的 8 位用例ID，对照 `cases/*_可自动化用例.csv`，输出：

- `report/<stem>_自动化追溯矩阵.md` — 汇总 + A/B 明细 + 无ID task 附录  
- `report/<stem>_自动化追溯矩阵.csv` — 可导入 Excel 做进度跟踪  

含历史大套件标题匹配时：`python tools/traceability_matrix.py --include-legacy`

## 界面和任务设置 — 套件索引

| 终稿 scripts/ | 说明 md（report/） |
|---------------|-------------------|
| `主界面_有地图无任务_自动化测试.yaml` | `主界面_有地图无任务_自动化用例说明.md` |
| `主界面_有地图有任务_自动化测试.yaml` | `主界面_有地图有任务_自动化用例说明.md` |
| `快速任务_自动化测试.yaml` | `快速任务_自动化用例说明.md` |
| `新建任务_自动化测试.yaml` | `新建任务_自动化用例说明.md` |
| `编辑任务_自动化测试.yaml` | `编辑任务_自动化用例说明.md` |
| `地图界面_自动化测试.yaml` | — |
| `界面设置与操作_自动化测试.yaml` | `界面设置与操作_figma-控件对照.md`（P0 集成冒烟） |
| `界面设置与操作_完整自动化测试.yaml` | 历史大套件，按需拆分 |

细则见 `.cursor/skills/Midscene/`。

## 禁止事项

- ❌ 在 **cases/** 放无「执行档位」列的旧 CSV  
- ❌ 把 **drafts/** 或 **cases/** 下的 yaml/csv 当终稿执行  
- ❌ 在 **scripts/** 新建 `*_草稿.yaml`（草稿只放 **drafts/**）  
- ❌ 使用已废弃路径 `output/cases`、`midscene自动化输出/cases` 双份维护
