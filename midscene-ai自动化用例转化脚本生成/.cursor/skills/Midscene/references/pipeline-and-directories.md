# 流水线与目录约定（单一根目录）

## 唯一产出根：`midscene自动化输出/`

所有 Midscene 相关文件集中在仓库根下 **一个文件夹**，下分 **4 个子目录**（不再使用分散的 `output/`）。

```
midscene自动化输出/
├── README.md       # 入口索引、套件表、命令速查
├── cases/          # 筛选 CSV
├── report/         # 报告与说明 md
├── drafts/         # YAML 草稿
└── scripts/        # YAML 终稿 → midscene run
```

详细表见 [../../midscene自动化输出/README.md](../../../midscene自动化输出/README.md)。

## 标准流水线

```
① 功能用例 xlsx/csv
        ↓  screen_ui_task_cases.py  (--out 默认 midscene自动化输出)
② cases/ + report/ + drafts/
        ↓  人工评审 cases「执行档位」
③ Agent 精修（Midscene安卓自动化脚本）
        ↓
④ scripts/*.yaml
        ↓  midscene run
```

## 子目录职责

| 路径 | 写入方 | 说明 |
|------|--------|------|
| `cases/` | 筛选脚本 | `*_可自动化用例.csv` 等，**必有「执行档位」** |
| `report/` | 筛选脚本、Agent | `*_筛选报告.md`、`*_依赖关系分析.md`、`*_自动化用例说明.md`、`*_figma-控件对照.md` |
| `drafts/` | 筛选脚本 | `*_自动化测试_草稿.yaml`，≤15 task，**非终稿** |
| `scripts/` | `build_midscene_yaml.py`、Agent | `*_自动化测试.yaml`（无「草稿」后缀），**唯一可执行目录** |

## 档位 → 目录

| 档位 | cases/ | drafts/ | scripts/ |
|------|--------|---------|----------|
| **A** | ✅ | 可生成草稿 | 精修后写入 |
| **B** | ✅ + `*_B档半自动.csv` | 通常不写 | 仅 Android 段 + 注释人工项 |
| **C** | ✅ | 改写后再筛 | 手写 flow |
| **D** | `*_不可自动化用例.csv` | — | — |

档位细则：[tiers-abcd.md](../Midscene功能用例筛选/references/tiers-abcd.md)。

## 命名约定

- **stem**：与源表一致，如 `界面和任务设置`（来自 `界面和任务设置.xlsx`）。
- **终稿套件**：按页面拆分，如 `快速任务_自动化测试.yaml`（见 [domain-ui-task-setting.md](../Midscene安卓自动化脚本/references/domain-ui-task-setting.md)）。
- **勿混用**「界面和任务设置」与「界面设置与操作」两套 stem，除非已统一重命名并重新筛选。

## 废弃路径

| 废弃 | 替代 |
|------|------|
| `midscene自动化输出/cases`、`midscene自动化输出/report`、`midscene自动化输出/drafts` | `midscene自动化输出/{cases,report,drafts}` |
| `midscene自动化输出/cases` 下无档位旧 CSV | 以 `cases/<stem>_可自动化用例.csv` 为准 |
| `convert_cases.py` 直出大 YAML | 筛选 + 分套件终稿 |
