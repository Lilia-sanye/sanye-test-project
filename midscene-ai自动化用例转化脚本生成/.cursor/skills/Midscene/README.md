# Midscene 自动化（技能组）

本目录收纳 **Midscene 相关技能**，与根下 PISTF「测试用例设计」等分离。  
**本文是 Midscene 组的使用入口**；细则见各子目录 `SKILL.md`。

## 技能一览

| 技能 | 何时使用 | 文档 |
|------|----------|------|
| **Midscene功能用例筛选** | 有 xlsx/csv 功能用例，要判断能否做机载 UI 自动化、分 A/B/C/D 档 | [SKILL.md](./Midscene功能用例筛选/SKILL.md) |
| **Midscene安卓自动化脚本** | 要写或精修 `midscene run` 的 YAML 终稿 | [SKILL.md](./Midscene安卓自动化脚本/SKILL.md) |

| 不要用本组 | 应改用 |
|----------|--------|
| 写七列表 / PISTF 功能用例 | `../测试用例设计/` |
| 评审用例覆盖与质量 | `../测试用例评审/` |
| 写测试方案 | `../测试方案设计/` |

## 产出目录（单一根，先看这里）

**所有 Midscene 产物** → [`midscene自动化输出/README.md`](../../midscene自动化输出/README.md)

```
midscene自动化输出/
├── cases/      # 筛选 CSV（执行档位）
├── report/     # 报告、套件说明、Figma 对照
├── drafts/     # YAML 草稿（勿 run）
└── scripts/    # YAML 终稿（midscene run）
```

旧路径 `output/` 已废弃，仅保留跳转说明。

## 技能文档结构（v3.4.1）

```
.cursor/skills/Midscene/
├── README.md              # 本文件：技能入口、命令速查
├── references/            # 流水线、工具、Figma、自检
├── Midscene功能用例筛选/
└── Midscene安卓自动化脚本/
```

**约定**：`SKILL.md` = 工作流；细则在 `references/` 与 `midscene自动化输出/README.md`。

---

## 使用方式

### 1. 在 Cursor / Trae 里怎么唤起

任选一种方式，让 Agent 加载本组技能：

**方式 A：@ 文件（推荐）**

```
@.cursor/skills/Midscene/README.md
@.cursor/skills/Midscene/Midscene功能用例筛选/SKILL.md
```

写 YAML 时再 @：

```
@.cursor/skills/Midscene/Midscene安卓自动化脚本/SKILL.md
```

**方式 B：口头说明（触发词）**

| 意图 | 示例说法 |
|------|----------|
| 筛选用例 | 「按 Midscene 功能用例筛选，筛 `修订版本/界面和任务设置.xlsx`」 |
| 转自动化 | 「功能用例转 Midscene」「筛选用例并分档」 |
| 写脚本 | 「按 Midscene 安卓自动化脚本，精修 YAML」「生成 Midscene YAML」 |
| 跑通流水线 | 「按 Midscene 组文档，从 xlsx 筛到终稿 YAML」 |
| Figma 读 UI 生成脚本 | 「按 figma-to-midscene，用 Figma 链接 + CSV 写 YAML」 |

Trae 用户路径将 `.cursor` 换为 `.trae` 即可（结构相同）。Figma MCP 需在 Trae 中单独启用。

**改 skill 后同步 Trae**（仓库根目录 PowerShell，先删再拷避免嵌套目录）：

```powershell
Remove-Item -Path ".trae\skills\Midscene" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -Path ".cursor\skills\Midscene" -Destination ".trae\skills\Midscene" -Recurse -Force
```

---


### 2. 标准流水线（推荐顺序）

```
① 准备用例文件（xlsx / csv，如 PingCode 导出或七列表 CSV）
        ↓
② Midscene功能用例筛选
   · 运行 screen_ui_task_cases.py（或让 Agent 按 SKILL 执行）
   · 得到 midscene自动化输出/cases、report、drafts/
        ↓
③ 人工评审
   · 打开 midscene自动化输出/cases/*_可自动化用例.csv，看「执行档位」列
   · A 档：可直接写 Midscene
   · B 档：看 *_B档半自动.csv 的「人工验收项」
   · C 档：改步骤或改为 aiAssert 后再转化
   · D 档：保留功能测试，不做 UI 自动化
        ↓
④ Midscene安卓自动化脚本
   · 基于 A 档（常用 P0+A）生成/精修终稿 YAML
   · 写入 midscene自动化输出/scripts/
   · task `name` 建议 `{用例ID}-简述`，便于追溯
        ↓
④b 追溯矩阵（推荐）
   · `python tools/traceability_matrix.py`
   · 得到 report/*_自动化追溯矩阵.md / .csv
        ↓
⑤ 实机执行
   · 填写 deviceId → midscene run <终稿.yaml>
```

有 Figma 设计稿时，在 ③④ 之间插入 **Figma MCP 读屏**（见下节），用设计文案补全 `ai:` / `aiAssert:`。

---

## Figma MCP 接入

在 Cursor 启用 **Figma 插件 MCP** 后，可将设计 Frame 与功能用例 CSV 对齐，生成/精修 Midscene 终稿 YAML。

**不是全自动**：`build_midscene_yaml.py` 不读 Figma；由 Agent 调用 `get_design_context` 等工具，再按安卓自动化技能写 YAML。

```
功能用例 CSV（A 档）
  +  Figma get_design_context（每屏/每状态一个 node-id）
  →  midscene自动化输出/report/<stem>_figma-控件对照.md（推荐）
  →  midscene自动化输出/scripts/<套件>_自动化测试.yaml
  →  midscene run
```

| 步骤 | 做什么 |
|------|--------|
| 1 | `screen_ui_task_cases.py` → 可自动化 CSV |
| 2 | 从 Figma URL 解析 `fileKey`、`nodeId`（`12-34` → `12:34`） |
| 3 | `get_metadata` 找 Frame → 对各屏 `get_design_context` |
| 4 | 提取按钮/标题/Toast 原文 → 对照 CSV 用例 ID |
| 5 | 精修 YAML（勿把 React 参考代码写入 `ai:`） |

**细则全文**：[references/figma-to-midscene.md](./references/figma-to-midscene.md)

**唤起示例**：

```
@.cursor/skills/Midscene/references/figma-to-midscene.md
Figma: https://figma.com/design/<fileKey>/...?node-id=1-2
CSV: midscene自动化输出/cases/界面和任务设置_可自动化用例.csv
更新 快速任务_自动化测试.yaml
```

---

### 3. 命令行（仓库根目录执行）

**全参数、产出路径、脚本行为** 见 [references/tools.md](./references/tools.md)。

**速查**

```bash
# ①② 筛选 + 分档
python tools/screen_ui_task_cases.py --input "修订版本/界面和任务设置.xlsx"

# ④ 终稿 YAML（默认 P0 + A 档）
python tools/build_midscene_yaml.py \
  --csv midscene自动化输出/cases/界面和任务设置_可自动化用例.csv \
  --out midscene自动化输出/scripts/界面设置与操作_自动化测试.yaml

# ⑤ 执行（先改 deviceId）
midscene run midscene自动化输出/scripts/界面设置与操作_自动化测试.yaml
```

---

### 4. 产出物在哪里看

统一根目录：**`midscene自动化输出/`**（详见其 [README.md](../../midscene自动化输出/README.md)）

| 阶段 | 路径 | 说明 |
|------|------|------|
| 筛选 CSV | `cases/<stem>_可自动化用例.csv` 等 | 含 **执行档位** |
| 筛选报告 | `report/<stem>_筛选报告.md` | 统计、档位 |
| 依赖分析 | `report/<stem>_依赖关系分析.md` | 模块、套件建议 |
| YAML 草稿 | `drafts/<stem>_自动化测试_草稿.yaml` | 须审阅，**勿 run** |
| **YAML 终稿** | `scripts/*.yaml` | **仅此处** `midscene run` |
| 套件说明 / Figma | `report/<套件>_自动化用例说明.md` 等 | 与终稿成对 |

---

### 5. 执行档位怎么用

| 档位 | 含义 | 你怎么做 |
|------|------|----------|
| **A** | 机载 UI 可全自动 | 纳入 `build_midscene_yaml.py` 或手写 `tasks[].flow` |
| **B** | UI 可点，验收靠 ADB/Linux/台架 | YAML 只写 Android 段；人工验收项见 B 档 CSV |
| **C** | 需改写成 `ai` / `aiAssert` | 先改步骤描述再重新筛选或手写 flow |
| **D** | 不宜首批 UI 自动化 | 留在功能用例里人工测 |

---

### 6. 常见场景速查

| 场景 | 用哪个技能 / 命令 |
|------|-------------------|
| 新接到一份 xlsx 用例表 | 筛选技能 + `screen_ui_task_cases.py` |
| 只要 P0 冒烟 YAML | 筛选后 `build_midscene_yaml.py --level P0 --tier A` |
| 口述几条机载操作，快速出脚本 | **Midscene安卓自动化脚本**（无需先筛选） |
| 截图补 UI 步骤 | 筛选 SKILL 中「截图 + 筛选用例」流程 |
| 满袋/倒草/规划类用例 | 多数为 D 档；仅含明确「点击/进入设置」等再考虑 A |
| 设计稿补充快速任务/保存弹窗 | 安卓技能 + `DESIGN-` 命名；见 [conversion-and-checklist.md](./references/conversion-and-checklist.md) |
| **Figma 链接 + CSV 写 YAML** | [figma-to-midscene.md](./references/figma-to-midscene.md) + Figma MCP |
| 仅 PNG 无 Figma MCP | 截图走「设计稿融合」；Trae 无 MCP 时同理 |
| 界面和任务设置多套件 | [domain-ui-task-setting.md](./Midscene安卓自动化脚本/references/domain-ui-task-setting.md) |
| 只改某一终稿套件 | @ 安卓技能 + 目标 yaml；勿重跑整表机械生成 |
| 流水线顺序 | 主界面 → 快速任务 → 新建/编辑（编辑放末尾） |

---

### 7. 命名与边界（避免选错技能）

- 本组产出是 **自动化 YAML**，不是「测试用例表」。
- 技能目录名以 `Midscene` 开头，集中在 **`skills/Midscene/`** 下，不要与根目录 `测试用例*` 混淆。
- 旧称「用例筛选与AI生成」「midscene-安卓测试用例生成」已废弃，以本目录下现名为准。

---

## 规范转化与脚本生成（必读）

核心原则：**先筛选定档，再只转化 A 档；机械生成只是草稿，准确靠人工精修 + 单条试跑。**

细则（源头要求、字段映射、`ai`/`aiAssert`、B 档、工作流、发布自检、工具边界）见：

- [references/conversion-and-checklist.md](./references/conversion-and-checklist.md)
- [references/figma-to-midscene.md](./references/figma-to-midscene.md) — Figma MCP + CSV → YAML
- [Midscene安卓自动化脚本/references/field-to-flow.md](./Midscene安卓自动化脚本/references/field-to-flow.md)
- [Midscene安卓自动化脚本/references/ai-instructions.md](./Midscene安卓自动化脚本/references/ai-instructions.md)

命令行见 [references/tools.md](./references/tools.md)。

---

## 流水线示意

```
功能用例 xlsx/csv
  → 筛选 → midscene自动化输出/{cases,report,drafts}
  → 评审 A 档 → 精修 → midscene自动化输出/scripts/
  → midscene run
```

## 相关文档

- [Skills 总目录规范](../README.md)
- [组级 references/](./references/) — 路由、流水线、转化自检、工具命令
- [Midscene功能用例筛选 SKILL](./Midscene功能用例筛选/SKILL.md) + [references/](./Midscene功能用例筛选/references/)
- [Midscene安卓自动化脚本 SKILL](./Midscene安卓自动化脚本/SKILL.md) + [references/](./Midscene安卓自动化脚本/references/)
