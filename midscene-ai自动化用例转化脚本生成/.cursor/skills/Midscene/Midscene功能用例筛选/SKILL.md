---
name: "midscene-functional-case-screening"
id: "midscene-functional-case-screening"
display_name: "Midscene功能用例筛选"
description: "从 xlsx/csv 筛选【功能测试用例】中可转 Midscene 的条目，分 A/B/C/D 档并出 YAML 草稿。不编写七列表用例、不生成 AI 功能用例正文。下游用 Midscene安卓自动化脚本 写终稿 YAML。"
author: "AI Assistant"
version: "3.4.1"
category: "Midscene自动化"
skill_category: "Midscene"
skill_index: "../README.md"
tags:
  - Midscene
  - 功能用例筛选
  - 自动化分档
  - 截图辅助
  - 测试转化
  - 任务依赖

trigger:
  keywords:
    - "Midscene功能用例筛选"
    - "功能用例转Midscene"
    - "筛选用例"
    - "转化为自动化测试"
    - "用例转化"
    - "Midscene分档"
    # 兼容旧称（避免歧义，文档中勿再使用）
    - "用例筛选与AI生成"
    - "生成AI用例"
    - "截图生成用例"
    - "设计稿"
    - "Figma"
    - "figma-to-midscene"
    - "界面和任务设置"
    - "作业任务"
  patterns:
    - "筛选.*可转化.*用例"
    - "筛选.*Midscene"
    - "将.*功能用例.*转.*自动化"
    - "截图.*生成.*自动化步骤"

config:
  supported_formats:
    - "xlsx"
    - "xls"
    - "csv"
  midscene_keywords_high:
    - "点击"
    - "输入"
    - "选择"
    - "滑动"
    - "等待"
  midscene_keywords_mid:
    - "验证"
    - "检查"
    - "显示"
  midscene_keywords_ui_extra:
    - "进入"
    - "打开"
    - "关闭"
    - "拖动"
    - "缩放"
    - "长按"
    - "添加"
    - "返航"
    - "充电"
  hard_block_patterns:
    - "adb shell"
    - "Linux从板"
    - "timedatectl"
    - "金属遮罩"
    - "拔卡"
  batch_script: "tools/screen_ui_task_cases.py"
  screen_output_dir: "output"
  final_yaml_dir: "midscene自动化输出/scripts"

capabilities:
  - "读取本地测试用例文件（Excel、CSV格式）"
  - "智能筛选适合自动化测试的用例"
  - "分析用例步骤描述提取可自动化操作"
  - "支持截图识别生成AI测试用例"
  - "生成符合Midscene规范的YAML脚本"
  - "输出详细的用例筛选报告（含可自动化/不可自动化用例详情）"
  - "支持生成报告文档（Markdown格式）"
  - "自动创建输出目录结构，将生成的文档归类到统一目录"
  - "智能分析用例间的依赖关系（前置条件、数据依赖）"
  - "自动识别测试准备和清理类用例"
  - "按业务流程组织测试用例顺序"
  - "支持测试套件的分组和优先级设置"
  - "生成任务依赖关系图和执行顺序"
  - "识别可共享的公共步骤"
  - "支持循环依赖检测和警告"

parameters:
  - name: file_path
    type: string
    description: "测试用例文件路径（xlsx/xls/csv格式）"
    required: true

  - name: filter_keywords
    type: array
    description: "筛选关键词（如：点击、输入、选择等UI操作）"
    required: false

  - name: screenshot_path
    type: string
    description: "截图文件路径（用于AI用例生成）"
    required: false

  - name: output_format
    type: string
    description: "输出格式（yaml/json）"
    required: false
    default: "yaml"

  - name: report_format
    type: string
    description: "报告输出格式（markdown/text）"
    required: false
    default: "markdown"

  - name: output_dir
    type: string
    description: "输出目录路径（可选，默认在当前目录创建output目录）"
    required: false
    default: "./output"

  - name: analyze_dependencies
    type: boolean
    description: "是否分析任务依赖关系（默认true）"
    required: false
    default: true

  - name: generate_test_suite
    type: boolean
    description: "是否生成测试套件组织（默认true）"
    required: false
    default: true

  - name: dependency_field
    type: string
    description: "前置条件字段名（如：前置条件、precondition）"
    required: false
    default: "前置条件"

  - name: module_field
    type: string
    description: "模块字段名（如：所属模块、module）"
    required: false
    default: "所属模块"

  - name: priority_field
    type: string
    description: "优先级字段名（如：优先级、priority、等级）"
    required: false
    default: "优先级"

  - name: steps_field
    type: string
    description: "操作步骤字段名（如：步骤描述、操作步骤）"
    required: false
    default: "步骤描述"

  - name: title_field
    type: string
    description: "用例标题字段名"
    required: false
    default: "用例标题"

usage:
  prerequisites:
    - "本地测试用例文件格式支持：xlsx, xls, csv"
    - "截图文件格式支持：png, jpg, jpeg"
    - "结合 Midscene 安卓测试生成技能使用效果更佳"

  screening_criteria:
    - "用例步骤包含UI操作（点击、输入、选择等）"
    - "用例步骤描述清晰、可自动化执行"
    - "用例为冒烟测试或核心功能测试优先级更高"
    - "排除纯接口测试、性能测试等不适用场景"

  steps:
    - "step: 读取本地测试用例文件"
    - "step: 分析用例结构和内容"
    - "step: 根据关键词筛选可自动化用例"
    - "step: 提取用例步骤中的UI操作"
    - "step: 创建输出目录结构"
    - "step: 生成符合Midscene规范的YAML脚本"
    - "step: 输出筛选报告和用例清单"

  output_structure: |
    output/
    ├── report/                    # 报告目录
    │   └── 用例筛选报告.md         # 筛选概览报告
    ├── cases/                     # 用例清单目录
    │   ├── 可自动化用例.csv        # 可转化用例清单
    │   └── 不可自动化用例.csv      # 不可转化用例清单
    └── scripts/                   # 测试脚本目录
        └── 自动化测试.yaml         # Midscene测试脚本

  example:
    input: "筛选 C:\\Users\\wangli02\\Desktop\\回充.xlsx 中的用例，生成自动化测试脚本"
    output: |
      筛选结果：
      - 总用例数：40条
      - 可自动化用例：25条
      - 筛选关键词：点击、输入、选择、等待、验证

      输出目录：midscene自动化输出/
      ├── report/用例筛选报告.md
      ├── cases/可自动化用例.csv
      ├── cases/不可自动化用例.csv
      └── scripts/自动化测试.yaml
---

# Midscene 功能用例筛选

> **路径**：`.cursor/skills/Midscene/Midscene功能用例筛选/SKILL.md`。分类入口：[Midscene/README.md](../README.md)；总规范：[skills/README.md](../../README.md)。

从 **xlsx / csv 功能用例表** 中筛出可转为 **Midscene 机载 Android UI 自动化** 的条目，输出 **A/B/C/D 分档 + 报告 + YAML 草稿**。

> **命名说明**：本技能不叫「AI 用例生成」或「测试用例生成」——不产出七列表功能用例，只产出**自动化筛选结果与脚本素材**。

## 参考文档（按需加载）

| 文档 | 内容 |
|------|------|
| [references/tiers-abcd.md](./references/tiers-abcd.md) | A/B/C/D 档位、硬阻碍、B 档 CSV |
| [references/column-mapping.md](./references/column-mapping.md) | 表头映射、PingCode/七列表、模板剥离 |
| [references/screening-rules.md](./references/screening-rules.md) | 筛选规则 v3、整机域、关键词 |
| [references/output-artifacts.md](./references/output-artifacts.md) | `output/` 产出清单 |
| [references/dependencies-and-suite.md](./references/dependencies-and-suite.md) | 依赖分析、**拆终稿套件**、共享步骤 |
| [../Midscene安卓自动化脚本/references/domain-ui-task-setting.md](../Midscene安卓自动化脚本/references/domain-ui-task-setting.md) | 界面和任务设置终稿文件名与顺序 |
| [../references/conversion-and-checklist.md](../references/conversion-and-checklist.md) | 设计稿融合、发布自检 |
| [../references/deliverable-report-template.md](../references/deliverable-report-template.md) | 下游说明 md 模板 |
| [../references/figma-to-midscene.md](../references/figma-to-midscene.md) | Figma MCP + CSV 联合流程 |
| [../references/skill-routing.md](../references/skill-routing.md) | 与其它技能的路由对照 |
| [../references/pipeline-and-directories.md](../references/pipeline-and-directories.md) | 流水线与目录约定 |
| [../references/tools.md](../references/tools.md) | `screen_ui_task_cases.py` 命令与脚本边界 |

## 产出目录约定

| 目录 | 内容 | 谁写入 |
|------|------|--------|
| `midscene自动化输出/report/` | `*_筛选报告.md`、`*_依赖关系分析.md` | 本技能 / `screen_ui_task_cases.py` |
| `midscene自动化输出/cases/` | 可自动化、**B档半自动**、不可自动化、共享步骤 CSV | 本技能 / 脚本 |
| `midscene自动化输出/drafts/` | `*_自动化测试_草稿.yaml`（须审阅） | 本技能 / 脚本 |
| `midscene自动化输出/scripts/` | **终稿** YAML（`midscene run`） | **Midscene安卓自动化脚本** |

## 技能路由

见 [../references/skill-routing.md](../references/skill-routing.md)。本技能产出：**分档 CSV + 报告 + YAML 草稿**。

## 技能边界（必读）

| 使用本技能 | 不要使用本技能 |
|------------|----------------|
| 筛选用例、评估能否自动化、批量出 YAML 草稿 | 从零编写 PISTF 七列表功能用例 → 用 **测试用例设计** |
| 结合截图补全 UI 步骤 | 评审用例质量 → 用 **测试用例评审** |
| 输出 `output/` 报告与 CSV | 直接写最终可运行 YAML（无筛选）→ 用 **Midscene安卓自动化脚本** |

**流水线**：**Midscene功能用例筛选**（本分档 + 草稿）→ **Midscene安卓自动化脚本**（审阅、补全 `deviceId` / `aiActContext`、套件与依赖）。

**批量试跑脚本**：参数与产出见 [../references/tools.md](../references/tools.md)。

```bash
python tools/screen_ui_task_cases.py --input "修订版本/界面和任务设置.xlsx"
```

## 功能概览

| 功能 | 说明 |
|------|------|
| 用例文件读取 | 支持 xlsx、xls、csv 格式的测试用例文件 |
| 智能筛选 | 根据UI操作关键词筛选可自动化用例 |
| AI用例生成 | 通过截图识别界面元素生成测试用例 |
| YAML脚本生成 | 输出符合Midscene规范的自动化脚本 |
| 转化报告 | 生成用例筛选报告和统计数据 |
| 目录管理 | 自动创建结构化输出目录，归类生成的文档 |
| **任务依赖分析** | **智能识别用例间的依赖关系和执行顺序** |
| **测试套件组织** | **按模块和优先级分组，优化执行顺序** |
| **共享步骤识别** | **自动识别公共操作步骤** |
| **执行档位 A/B/C/D** | **区分可直接自动化、半自动、改写法后可转化、不宜首批** |

## 执行档位（v3 必标）

每条用例须标注 CSV 列 `执行档位`、`档位说明`。**A/B/C/D 定义、硬阻碍、B 档 CSV** 见 [references/tiers-abcd.md](./references/tiers-abcd.md)。

## 用例表列名映射

**先识别表头再映射**；PingCode / 七列表 / 模板剥离细则见 [references/column-mapping.md](./references/column-mapping.md)。

## 任务依赖与套件组织

依赖识别、循环依赖警告、模块分组、P0→P2 顺序、共享步骤与草稿 YAML 范围见 [references/dependencies-and-suite.md](./references/dependencies-and-suite.md)。

## 输出目录结构

`output/` 树、CSV 关键列、报告要点见 [references/output-artifacts.md](./references/output-artifacts.md)。终稿目录见 [../references/pipeline-and-directories.md](../references/pipeline-and-directories.md)。

## 筛选规则（v3）

完整规则（适用场景、B/D 边界、整机域、关键词）见 [references/screening-rules.md](./references/screening-rules.md)。与 `tools/screen_ui_task_cases.py` 保持一致。

## Agent 执行清单（用户给文件路径时）

1. 读取表头，确认列映射；无法映射则向用户确认字段名。
2. 对每条用例：技能分类 + **执行档位 A/B/C/D** + 档位说明；地图/键盘/Toast 见 [references/screening-rules.md](./references/screening-rules.md) §5。
3. 创建 `midscene自动化输出/report/`、`midscene自动化输出/cases/`、`midscene自动化输出/drafts/`（或用户指定 `output_dir`）。
4. 写出：筛选报告、依赖分析（含 **建议终稿套件文件名**）、各档 CSV、共享步骤 CSV（若有）。
5. 为 **P0 且 A 档** 在 `midscene自动化输出/drafts/` 生成 YAML **草稿**（≤15 task）；终稿由下游按 [domain-ui-task-setting.md](../Midscene安卓自动化脚本/references/domain-ui-task-setting.md) **分套件**精修。
6. 提示下游产出：`midscene自动化输出/scripts/*.yaml` + `midscene自动化输出/report/*_自动化用例说明.md`。
7. **不要**在此技能中交付未经审阅的终稿或大套件一次性跑全量。

有 `tools/screen_ui_task_cases.py` 且路径为 xlsx 时，**优先运行脚本** 再基于产出审阅补全，避免口径漂移。

## 设计稿 + CSV 联合流程

**有 Figma 链接 + MCP**：按 [../references/figma-to-midscene.md](../references/figma-to-midscene.md) 执行（`get_design_context` → 控件对照 md → 下游 YAML）。

**仅截图 / 无 MCP**：

1. 用户提供截图/设计标注时：列出交互规则表（添加/删除/上限/键盘/Toast）。
2. 与 CSV `用例ID` 对照：已有 ID 写入报告「已覆盖」；缺口标 `DESIGN-` 建议项。
3. 将 DESIGN 项交给 **Midscene安卓自动化脚本** 写入对应终稿套件（快速/新建/编辑），命名见 [../references/conversion-and-checklist.md](../references/conversion-and-checklist.md)。

## 使用方式

### 方式1：筛选用例文件

```
用户：筛选 C:\Users\wangli02\Desktop\回充.xlsx 中的用例，生成自动化测试脚本
助手：[读取文件 → 分析用例 → 筛选可自动化用例 → 生成YAML脚本]
```

### 方式2：截图生成用例

```
用户：根据截图 C:\Users\wangli02\Desktop\screenshot.png 生成测试用例
助手：[识别截图中的UI元素 → 生成测试步骤 → 输出YAML脚本]
```

### 方式3：筛选 + 截图结合

```
用户：筛选用例文件中的用例，然后根据截图补充UI元素
助手：[读取用例 → 筛选可用用例 → 识别截图UI → 生成完整脚本]
```

## 输出示例

### 筛选报告

```
用例筛选报告
============
文件路径：C:\Users\wangli02\Desktop\回充.xlsx
总用例数：40条
筛选结果：
  ✓ 可自动化用例：25条（P0: 3条，P1: 8条，P2: 14条）
  ✗ 不可自动化用例：15条（接口测试、性能测试等）

筛选关键词匹配：
  - 点击：匹配 18 条
  - 输入：匹配 5 条
  - 选择：匹配 12 条
  - 等待：匹配 8 条
  - 验证：匹配 15 条
```

### 生成的YAML脚本

```yaml
# 自动生成的 Midscene 测试脚本
config:
  ai:
    actionTimeout: 30000
    retryInterval: 200
  page:
    defaultWait: 200

android:
  deviceId: "<设备ID>"

agent:
  testId: "低电回充测试"
  groupName: "回充功能测试"
  generateReport: true

tasks:
  - name: 低电回充流程
    flow:
      - ai: 点击配送
      - ai: 点击请选择目的地
      - ai: 选择02，点击确认
      - ai: 关门出发
      - ai: 等待直到页面显示"开门取物"
      - aiAssert: 页面出现配送、设置等文字
```

## 截图识别用例生成

当提供截图时，AI会：

1. **识别界面元素**：按钮、输入框、列表、文本等
2. **提取操作序列**：分析用户可能的操作路径
3. **生成测试步骤**：将识别结果转化为可执行步骤
4. **输出YAML脚本**：生成符合Midscene规范的脚本

### 截图识别示例

输入截图包含：
- 配送按钮
- 目的地选择列表
- 确认按钮
- 状态显示区域

输出测试步骤：
```yaml
tasks:
  - name: 配送测试
    flow:
      - ai: 点击配送按钮
      - ai: 点击请选择目的地
      - ai: 选择目的地选项
      - ai: 点击确认按钮
      - ai: 等待页面显示配送状态
      - aiAssert: 配送状态显示正常
```

### 依赖关系分析报告示例

```
# 任务依赖关系分析报告

## 分析概览
- 总用例数：50条
- 识别出的依赖关系：18个
- 检测到的循环依赖：0个
- 建议的执行顺序：已生成

## 依赖关系示意

用户登录 → 查看任务列表 → 创建新任务 → 编辑任务 / 查看详情 → 删除任务（清理）

## 建议的执行顺序

1. 用户登录（P0）
2. 查看任务列表（P0）
3. 创建新任务（P0）
4. 查看任务详情（P1）
5. 编辑任务（P1）
6. 删除任务（P1）

## 识别的共享步骤

| 步骤名称 | 使用次数 | 来源用例 |
|---------|---------|---------|
| 用户登录 | 8次 | 多个用例 |
| 返回首页 | 5次 | 多个用例 |
| 查看任务列表 | 3次 | 多个用例 |

## 特殊处理说明

- 建议将"用户登录"提取为共享步骤
- 建议将"清理测试数据"作为最后一个任务
- 检测到3个用例有类似的操作步骤，建议合并
```

### 完整的自动化测试脚本示例（含依赖关系）

```yaml
config:
  ai:
    actionTimeout: 30000
    retryInterval: 200
  page:
    defaultWait: 200

android:
  deviceId: "<设备ID>"

agent:
  testId: "任务管理测试套件"
  groupName: "任务管理完整流程"
  generateReport: true

# 共享步骤库
shareSteps:
  - name: 用户登录
    flow:
      - ai: 点击登录按钮
      - ai: 输入用户名 "admin"
      - ai: 输入密码 "123456"
      - ai: 点击确认登录
      - aiAssert: 页面显示主页

  - name: 返回首页
    flow:
      - ai: 点击返回按钮
      - aiAssert: 页面显示主页

# 任务列表（含依赖关系）
tasks:
  - name: 用户登录
    precondition: "无"
    flow:
      - ref: 用户登录
      - aiAssert: 登录成功

  - name: 查看任务列表
    dependsOn: ["用户登录"]
    precondition: "用户已登录"
    flow:
      - ref: 用户登录
      - ai: 点击任务管理
      - ai: 点击任务列表
      - aiAssert: 任务列表页面显示正常

  - name: 创建新任务
    dependsOn: ["查看任务列表"]
    precondition: "任务列表页面可见"
    flow:
      - ref: 用户登录
      - ai: 点击新建任务
      - ai: 输入任务名称 "测试任务-001"
      - ai: 点击保存
      - aiAssert: 任务创建成功提示
      - aiAssert: 任务列表显示新任务

  - name: 查看任务详情
    dependsOn: ["创建新任务"]
    precondition: "存在测试任务"
    flow:
      - ref: 用户登录
      - ai: 点击任务列表
      - ai: 选择"测试任务-001"
      - ai: 点击查看详情
      - aiAssert: 任务详情页面显示正常

  - name: 编辑任务
    dependsOn: ["查看任务详情"]
    precondition: "任务详情页面可见"
    flow:
      - ref: 用户登录
      - ai: 点击任务列表
      - ai: 选择"测试任务-001"
      - ai: 点击编辑
      - ai: 修改任务名称为 "测试任务-已编辑"
      - ai: 点击保存
      - aiAssert: 编辑成功提示

  - name: 删除任务
    dependsOn: ["编辑任务"]
    precondition: "任务已编辑完成"
    cleanup:
      - ai: 点击任务列表
      - ai: 选择测试任务
      - ai: 点击删除
      - ai: 确认删除
    flow:
      - ref: 用户登录
      - ai: 点击任务列表
      - ai: 选择"测试任务-已编辑"
      - ai: 点击删除
      - ai: 确认删除
      - aiAssert: 任务已从列表中移除
```

## 最佳实践

1. **用例准备**：确保原用例步骤描述清晰，包含具体操作
2. **优先级筛选**：优先选择P0、P1级别的核心用例
3. **补充描述**：用例描述模糊时，提供截图帮助识别
4. **分批处理**：大量用例建议分批筛选和生成
5. **人工审核**：生成的脚本建议人工审核后执行
6. **依赖关系维护**：定期检查和更新用例间的依赖关系
7. **共享步骤管理**：及时提取和更新共享步骤库
8. **数据清理**：重要测试应包含数据准备和清理步骤

## 相关技能

- [Midscene安卓自动化脚本](../Midscene安卓自动化脚本/SKILL.md) — **下游**：精修 YAML、套件、依赖、`aiActContext`
- [Midscene 技能组索引](../README.md) · [组级 references/](../references/)
- [Skills 目录规范](../../README.md)
- [测试用例格式转换](../../测试用例格式转换/SKILL.md) — xlsx/csv 格式互转（筛选前可先统一格式）

功能用例编写/评审请用 **测试用例设计 / 测试用例评审**（不在 Midscene 分类下）。

## 试跑参考（界面和任务设置.xlsx）

| 指标 | 约值 |
|------|------|
| 总用例 | 313 |
| A 档 | 232 |
| B 档 | 52 |
| C 档 | 28 |
| D 档 | 1 |

详见仓库 `midscene自动化输出/report/界面和任务设置_筛选报告.md`（运行 `tools/screen_ui_task_cases.py` 生成）。
