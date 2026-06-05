# Midscene 仓库工具（CLI 与产出）

脚本位于仓库根目录 `tools/`。产出根目录：**`midscene自动化输出/`**（见 [../../midscene自动化输出/README.md](../../midscene自动化输出/README.md)）。

---

## 环境（首次）

```bash
npm install -g @midscene/cli
adb devices
```

---

## `screen_ui_task_cases.py` — 筛选分档

### 作用

读取 xlsx/csv → 标注 A/B/C/D → 写入 **`midscene自动化输出/cases`**、**`report`**、**`drafts`**。

### 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--input` | `修订版本/界面和任务设置.xlsx` | 源用例 |
| `--out` | `midscene自动化输出` | 产出根（其下自动建 cases/report/drafts） |
| `--stem` | 输入文件 stem | 产出文件名前缀 |

### 示例

```bash
python tools/screen_ui_task_cases.py --input "修订版本/界面和任务设置.xlsx"
```

### 产出（`<stem>` = 表名）

| 路径 | 内容 |
|------|------|
| `midscene自动化输出/cases/<stem>_可自动化用例.csv` | A+B+C + 执行档位 |
| `midscene自动化输出/cases/<stem>_B档半自动.csv` | B 档 |
| `midscene自动化输出/cases/<stem>_不可自动化用例.csv` | D 档 |
| `midscene自动化输出/report/<stem>_筛选报告.md` | 统计 |
| `midscene自动化输出/report/<stem>_依赖关系分析.md` | 依赖 |
| `midscene自动化输出/drafts/<stem>_自动化测试_草稿.yaml` | ≤15 task 草稿 |

---

## `build_midscene_yaml.py` — CSV → 终稿草稿

### 作用

从 `cases/*_可自动化用例.csv` 机械生成 YAML 到 **`midscene自动化输出/scripts/`**（**仍须精修**）。

### 参数

| 参数 | 默认值 |
|------|--------|
| `--csv` | `midscene自动化输出/cases/界面和任务设置_可自动化用例.csv` |
| `--out` | `midscene自动化输出/scripts/界面设置与操作_自动化测试.yaml` |
| `--level` | `P0` |
| `--tier` | `A` |

### 示例

```bash
python tools/build_midscene_yaml.py \
  --csv midscene自动化输出/cases/界面和任务设置_可自动化用例.csv \
  --out midscene自动化输出/scripts/界面设置与操作_自动化测试.yaml
```

---

## `traceability_matrix.py` — 手工用例 ↔ YAML 追溯

### 作用

读取 `cases/*_可自动化用例.csv`，扫描 `scripts/*.yaml` 中每个 task 的 `name`，提取 `12901234-` 形式的 8 位用例ID，生成覆盖矩阵。

### 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--csv` | `midscene自动化输出/cases/界面和任务设置_可自动化用例.csv` | 源表 |
| `--scripts-dir` | `midscene自动化输出/scripts` | 终稿目录 |
| `--out-dir` | `midscene自动化输出/report` | 报告目录 |
| `--include-legacy` | 关 | 额外按**用例标题**匹配 `界面设置与操作_完整自动化测试.yaml` |

### 示例

```bash
python tools/traceability_matrix.py
python tools/traceability_matrix.py --include-legacy
```

### 产出

| 路径 | 内容 |
|------|------|
| `report/<stem>_自动化追溯矩阵.md` | 汇总、A/B 档明细、无ID task 附录 |
| `report/<stem>_自动化追溯矩阵.csv` | 用例ID、状态、套件、task（可导入表格） |

**约定**：终稿 task `name` 建议以 `{用例ID}-简述` 开头；合并用例写 `12903804-12903805-简述`。仅 `DESIGN-` / `PARAM-` 前缀的 task 不会计入用例ID 覆盖。

**何时重跑**：新增或修改 `scripts/*.yaml` 后、发布前自检。

---

## `apply_device_env.py` — 实机文案配置 → 终稿

### 作用

从 `midscene自动化输出/config/` 按**套件隔离**替换 `scripts/*.yaml` 中的 `{{map.name}}`、`{{zones.a.label}}`、`{{device.id}}` 等占位符。

### 目录

| 路径 | 说明 |
|------|------|
| `config/device.yaml` | 全局 deviceId、adbPath |
| `config/suites/<套件>.yaml` | 仅该套件脚本生效 |
| `config/fragments/ui-*.yaml` | 可选片段，由 suites 的 `imports` 显式引用 |

### 示例

```bash
python tools/apply_device_env.py --suite 主界面_有地图无任务
python tools/apply_device_env.py --device
python tools/apply_device_env.py --all
```

细则见 [../../midscene自动化输出/config/README.md](../../midscene自动化输出/config/README.md)。

---

## `midscene run`

```bash
midscene run midscene自动化输出/scripts/快速任务_自动化测试.yaml
```

---

## 推荐流水线

```
screen_ui_task_cases.py → 审阅 cases → build_midscene_yaml.py（可选）→ Agent 精修 scripts → midscene run
```

发布自检：[conversion-and-checklist.md](./conversion-and-checklist.md)。
