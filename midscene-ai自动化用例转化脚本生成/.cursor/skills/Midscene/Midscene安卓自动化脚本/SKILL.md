---
name: "midscene-android-automation-yaml"
id: "midscene-android-automation-yaml"
display_name: "Midscene安卓自动化脚本"
description: "编写可 midscene run 的 Android UI 自动化 YAML（ai/aiAssert）。产出为自动化脚本，不是功能测试用例表。承接 Midscene功能用例筛选 的 A/B 档 CSV 或口述步骤。勿与测试用例设计混用。"
author: "AI Assistant"
version: "3.4.1"
category: "Midscene自动化"
skill_category: "Midscene"
skill_index: "../README.md"
tags:
  - Midscene
  - 安卓自动化
  - YAML脚本
  - 任务依赖
  - 测试套件

trigger:
  keywords:
    - "Midscene安卓自动化脚本"
    - "Midscene YAML"
    - "Midscene脚本"
    - "安卓自动化脚本"
    - "创建测试脚本"
    - "YAML测试脚本"
    - "精修YAML草稿"
    - "融合进快速任务"
    - "合并到YAML"
    - "界面和任务设置"
    - "作业任务"
    - "根据设计稿"
    - "根据截图生成自动化"
    - "Figma"
    - "figma-to-midscene"
    - "Figma MCP"
    # 兼容旧称
    - "生成安卓测试"
    - "安卓自动化测试"
    - "midscene-安卓测试用例生成"
    - "安卓测试用例生成"
  patterns:
    - "生成.*Midscene.*(脚本|YAML)"
    - "编写.*自动化测试.*yaml"
    - "精修.*YAML.*草稿"
    - "midscene.*run"
  avoid_when:
    - "写测试用例"
    - "设计测试用例"
    - "PISTF"
    - "测试方案"
    - "筛选用例"
    - "功能用例表"

config:
  default_timeout: 30000
  default_retry_interval: 200
  default_wait: 200

capabilities:
  - "生成符合 Midscene 规范的 YAML 测试脚本"
  - "支持安卓设备配置（deviceId、adb路径）"
  - "支持全局提速配置（AI超时、重试间隔）"
  - "支持 Agent 配置（测试报告、AI行为上下文）"
  - "支持多任务定义和流程步骤"
  - "支持 AI 操作和断言指令"
  - "支持任务依赖关系管理（前置条件、依赖任务）"
  - "支持测试套件组织（分组、顺序、并行控制）"
  - "支持数据准备和清理步骤"
  - "支持测试用例失败时的恢复策略"
  - "支持任务执行顺序控制"
  - "支持共享步骤重用"

parameters:
  - name: device_id
    type: string
    description: "安卓设备ID（通过 adb devices 获取）"
    required: true

  - name: adb_path
    type: string
    description: "ADB 工具路径（可选）"
    required: false

  - name: tasks
    type: array
    description: "测试任务列表，每个任务包含名称、步骤、依赖关系等"
    required: true

  - name: ai_context
    type: string
    description: "AI 行为上下文，用于处理弹窗等场景"
    required: false

  - name: test_suite_name
    type: string
    description: "测试套件名称（可选）"
    required: false

  - name: enable_dependency_management
    type: boolean
    description: "是否启用任务依赖管理（默认true）"
    required: false
    default: true

  - name: enable_data_preparation
    type: boolean
    description: "是否启用数据准备和清理步骤（默认false）"
    required: false
    default: false

  - name: share_steps
    type: array
    description: "共享步骤定义，可被多个任务重用"
    required: false

usage:
  prerequisites:
    - "已安装 Midscene CLI 工具"
    - "已配置 AI 模型环境变量"
    - "安卓设备已连接（通过 USB 或 ADB 无线连接）"

  steps:
    - "提供设备ID和测试任务步骤"
    - "生成 YAML 测试脚本"
    - "使用 midscene 命令运行脚本"

  example:
    input: "生成安卓测试脚本，设备ID: 192.168.140.140，任务：点击配送，选择目的地，确认出发"
    output: |
      config:
        ai:
          actionTimeout: 30000
          retryInterval: 200
        page:
          defaultWait: 200

      android:
        deviceId: "192.168.140.140"

      agent:
        testId: "配送流程测试"
        groupName: "功能测试"
        generateReport: true

      tasks:
        - name: 配送流程
          flow:
            - ai: 点击配送
            - ai: 点击请选择目的地
            - ai: 关门出发
            - aiAssert: 页面显示配送成功

---

# Midscene 安卓自动化脚本

> **路径**：`.cursor/skills/Midscene/Midscene安卓自动化脚本/SKILL.md`。分类入口：[Midscene/README.md](../README.md)。

生成可在机载 Android（或指定设备）上执行的 **Midscene YAML 自动化脚本**。

> **命名说明**：本技能不叫「测试用例生成」——不编写七列表功能用例，只编写 `midscene run` 可执行的 **YAML**。

## 参考文档（按需加载）

| 文档 | 内容 |
|------|------|
| [references/yaml-schema.md](./references/yaml-schema.md) | 最小结构、必须/禁止、Agent 与任务字段 |
| [references/field-to-flow.md](./references/field-to-flow.md) | 用例表字段 → `ai` / `aiAssert` |
| [references/ai-instructions.md](./references/ai-instructions.md) | `ai`/`aiAssert` 写法、B 档注释 |
| [references/examples.md](./references/examples.md) | 单任务 / 多任务 YAML 片段 |
| [references/examples-full.md](./references/examples-full.md) | 配送、登录、依赖、数据准备等完整示例 |
| [references/domain-ui-task-setting.md](./references/domain-ui-task-setting.md) | **界面和任务设置**：套件拆分、入口、执行顺序 |
| [references/device-lexicon.md](./references/device-lexicon.md) | 实机可见文案词表（人工维护） |
| [../references/conversion-and-checklist.md](../references/conversion-and-checklist.md) | 转化工作流、设计稿融合、发布自检 |
| [../references/deliverable-report-template.md](../references/deliverable-report-template.md) | 终稿说明 md 模板 |
| [../references/figma-to-midscene.md](../references/figma-to-midscene.md) | **Figma MCP** + CSV → YAML |
| [../references/pipeline-and-directories.md](../references/pipeline-and-directories.md) | 草稿 vs 终稿目录 |
| [../references/tools.md](../references/tools.md) | `build_midscene_yaml.py`、`midscene run`、脚本边界 |

## 产出目录约定

| 类型 | 路径 |
|------|------|
| 上游草稿（只读参考） | `midscene自动化输出/drafts/*_自动化测试_草稿.yaml` |
| **本技能终稿输出** | `midscene自动化输出/scripts/<套件名>_自动化测试.yaml` |

不得将未审阅的草稿直接当作终稿提交。

## 技能路由

见 [../references/skill-routing.md](../references/skill-routing.md)。本技能产出：**`midscene自动化输出/scripts/*.yaml` 终稿**。

## 技能边界（必读）

| 使用本技能 | 不要使用本技能 |
|------------|----------------|
| 编写/精修 `midscene run` 的 YAML | 从零写功能测试用例表 → **测试用例设计** |
| 将筛选后的 A 档用例转为 `tasks[].flow` | 批量筛选用例、出分档报告 → **Midscene功能用例筛选** |
| 配置 deviceId、aiActContext、套件 | 仅评审用例文字 → **测试用例评审** |

**推荐流水线**：**Midscene功能用例筛选** → 审阅 `midscene自动化输出/cases/*_可自动化用例.csv`（**执行档位=A**）→ 本技能产出终稿 YAML 至 `midscene自动化输出/scripts/`。

## 快速开始

### 1. 准备工作

```bash
# 安装 Midscene CLI
npm install -g @midscene/cli

# 配置 AI 模型环境变量
export MIDSCENE_MODEL_BASE_URL="https://your-model/v1"
export MIDSCENE_MODEL_API_KEY="your-api-key"
export MIDSCENE_MODEL_NAME="your-model-name"
```

### 2. 使用方式

```
用户：生成安卓测试脚本，设备ID: 192.168.140.140，任务：登录测试
助手：请提供具体的测试步骤...
用户：点击登录，输入用户名test，输入密码123456，点击登录按钮，验证成功
助手：[生成完整YAML脚本]
```

## 生成的脚本结构

最小可运行模板、必须/禁止项、Agent 与任务扩展字段见 [references/yaml-schema.md](./references/yaml-schema.md)。片段示例见 [references/examples.md](./references/examples.md)。

## 字段转化与 AI 指令

用例表 → `flow` 映射见 [references/field-to-flow.md](./references/field-to-flow.md)。`ai` / `aiAssert` / B 档注释见 [references/ai-instructions.md](./references/ai-instructions.md)。发布自检见 [../references/conversion-and-checklist.md](../references/conversion-and-checklist.md)。

## 核心功能

### 任务依赖与共享步骤（组织约定）

普渡机载项目 **默认**：通用前置写入 `agent.aiActContext`；跨套件同源规则用 YAML 文件头「关联」注释，**不必**强行使用 `shareSteps`/`dependsOn`（除非已验证当前 `@midscene/cli` 支持）。

`shareSteps`、`dependsOn`、`ref:` 细则见 [references/yaml-schema.md](./references/yaml-schema.md)。不确定时 **只输出最小结构**。

### 共享步骤示例（CLI 支持时）

```yaml
shareSteps:
  - name: 登录系统
    flow:
      - ai: 点击登录按钮
      - aiAssert: 页面显示欢迎信息

tasks:
  - name: 创建新任务
    dependsOn: ["登录系统"]
    flow:
      - ref: 登录系统
      - ai: 点击新建任务
      - ai: 输入任务名称 "测试任务"
      - ai: 点击保存
      - aiAssert: 任务创建成功

  - name: 编辑任务
    dependsOn: ["创建新任务"]  # 依赖前面的任务
    flow:
      - ref: 登录系统         # 重用共享步骤
      - ai: 点击任务列表
      - ai: 选择刚创建的任务
      - ai: 点击编辑
      - ai: 修改任务名称
      - ai: 点击保存
      - aiAssert: 修改成功
```

## 运行测试

```bash
# 运行单个测试脚本
midscene run test-script.yaml

# 生成报告
midscene run test-script.yaml --report
```

## 示例脚本

| 文档 | 内容 |
|------|------|
| [references/examples.md](./references/examples.md) | 单任务冒烟、多任务内联前置 |
| [references/examples-full.md](./references/examples-full.md) | 配送流程、登录、shareSteps/dependsOn、数据准备与清理（完整 YAML） |

## 最佳实践

### 任务依赖设计原则
1. **明确依赖关系**：每个任务的依赖关系要清晰，避免循环依赖
2. **合理分组**：相关的任务组织在一起，便于管理和维护
3. **数据准备和清理**：重要测试要包含数据准备和清理步骤
4. **失败处理**：合理设置失败时的处理策略
5. **共享步骤**：通用操作（如登录、返回首页）提取为共享步骤

### Task 设计自检规则（必读）

> 以下规则源于实机执行中反复验证的经验，**每个 task 产出后必须逐条自检**。

#### 规则 1：消除「若有…」条件分支
- ❌ 禁止：`- ai: 若有未设置返航点提示，点击关闭`
- ✅ 正确：**将分支拆为独立 task**，用断言覆盖「无论哪种情况，按钮必须有响应」
  ```yaml
  # 错误写法
  - ai: 点击「返航」按钮
  - ai: 若有未设置返航点提示，点击关闭
  # → AI 自主判断"是否有提示"，极易误判导致超时

  # 正确写法：拆为独立 task
  - name: "返航按钮点击有响应"
    flow:
      - ai: 点击底部快捷栏「返航」按钮
      - ai: 等待1.5秒
      - aiAssert: 弹出返航确认弹窗或未设置返航点提示，或开始返航流程，按钮点击有响应
      - ai: 若弹出弹窗或对话框，点击弹窗中的关闭、取消或返回按钮关闭弹窗
      - ai: 等待直到回到主界面地图页
  ```
  条件分支中唯一可保留的模糊指令是**弹窗/对话框关闭**（因为无论弹窗内容是确认还是提示，关闭操作都是找到 X/取消/返回），但前提是断言已经验证了「按钮有响应」。

#### 规则 2：每个 task 结尾回到起始状态
- 涉及页面跳转的 task，**末尾必须显式** `等待直到回到主界面地图页` + 断言确认
- 禁止前一个 task 停留在子页面、下一个 task 假设"已在主界面"
- 每个 task 的开头也写 `等待直到进入主界面地图页`，形成自包含闭环
  ```yaml
  - name: "设置按钮跳转设置页并返回"
    flow:
      - ai: 等待直到进入主界面地图页          # ← 入口自检
      - ai: 点击底部快捷栏「设置」按钮
      - ai: 等待直到进入设置页面
      - aiAssert: 页面顶部标题显示「设置」
      - ai: 点击左上角返回按钮
      - ai: 等待直到回到主界面地图页          # ← 出口恢复
      - aiAssert: 回到主界面地图页，底部快捷栏可见
  ```

#### 规则 3：断言必须具体，禁止模糊表述
- ❌ 禁止：`非白屏、无闪退` / `验证模块正常` / `页面显示正常`
- ✅ 正确：**断言具体可见的文字、控件或状态**
  ```yaml
  # 错误
  - aiAssert: 页面为系统或应用设置页，非白屏、无闪退

  # 正确
  - aiAssert: 页面顶部标题或导航栏显示「设置」
  - aiAssert: 设置页可见菜单项列表（如地图管理或设备信息等入口）
  ```

#### 规则 4：变量步骤上方保留原始字面量注释
- 使用 `{{key}}` 变量替换的步骤，**上方必须保留** `# - ai:` / `# - aiAssert:` 注释行，写出替换前的原始字面量
- `apply_device_env.py --apply` 会跳过 `#` 注释行，注释行始终保留原始参照
- 目的：后续维护时直接查看注释行即可了解变量应填什么格式的字段
  ```yaml
  flow:
    # - aiAssert: 地图可见「A区草坪 2000m²」「B区草坪 1500m²」「C区草坪 4000m²」等区域名称
    - aiAssert: 地图上可见「{{zones.a.mapLabel}}」或「{{zones.a.label}}」
    - aiAssert: 地图上可见「{{zones.b.mapLabel}}」或「{{zones.b.label}}」
    - aiAssert: 地图上可见「{{zones.c.mapLabel}}」或「{{zones.c.label}}」
  ```

#### 规则 5：长链路 task 应拆分为短 task
- 超过 3 步页面跳转的 task（如：主界面→新建页→添加区域→返回），应拆为独立 task
- 一个 task 只验证一个核心行为，避免中间步骤失败无法定位原因
  ```yaml
  # 拆分前：一条 task 走完 3 层页面
  - name: "新建任务并添加区域"
    flow:
      - ai: 点击「新建任务」→ 进入新建页
      - ai: 点击地图区域 → 添加区域
  # → 中间失败不知道卡在哪个环节

  # 拆分后：
  # Task 10：主界面 → 新建任务页（只验证入口跳转）
  # Task 12：新建任务页 → 添加区域（只验证区域添加）
  ```

### 测试用例组织模式
- **冒烟测试套件**：快速验证核心功能
- **功能测试套件**：按模块组织完整功能测试
- **回归测试套件**：涵盖历史修复和核心功能
- **端到端测试**：模拟真实用户完整业务流程

### 性能和稳定性建议
- 合理设置重试次数和超时时间
- 失败时提供明确的错误信息
- 重要用例增加 `repeat`（需 CLI 支持时）
- 包含必要的 `等待直到页面显示` 步骤

## Agent 执行清单

1. 确认输入来源：用户口述 / CSV（**执行档位=A**）/ 草稿 yaml / **Figma 链接**（[figma-to-midscene.md](../references/figma-to-midscene.md)）/ 设计稿截图（先读图再写 flow）。
2. 界面和任务设置域：读 [references/domain-ui-task-setting.md](./references/domain-ui-task-setting.md)，按入口选套件或融合进已有 yaml。
3. 必填 `deviceId`；Windows 写 `androidAdbPath`；文件头注释实机区名/地图名。
4. 每条 task：`name` 含 `{用例ID}-` 或 `DESIGN-`；`flow` 末行 `aiAssert`；禁止抽象句「验证模块正常」。
5. **设计稿融合**：见 [../references/conversion-and-checklist.md](../references/conversion-and-checklist.md)；同场景合并 task，去重。
6. **副作用**：写库/开始作业/删数据 → `aiActContext` + task 末 `# 人工：`（见 [references/ai-instructions.md](./references/ai-instructions.md)）。
7. **B 档**：仅 Android `flow` + 注释人工验收项。
8. 输出：`midscene自动化输出/scripts/<套件>_自动化测试.yaml` + `midscene自动化输出/report/<套件>_自动化用例说明.md`。
9. **试跑顺序**：先写「进入 + 1 条主路径」→ `midscene run` 通过 → 再扩 5 次/拖拽/保存/开始作业。
10. 交付：run 命令、占位符、关联套件路径、危险 task 说明。

批量机械草稿： [../references/tools.md](../references/tools.md)（`build_midscene_yaml.py` 产出须精修，不可直接当分套件终稿）。

## 相关技能

- [Midscene功能用例筛选](../Midscene功能用例筛选/SKILL.md) — **上游**：分档、报告、草稿
- [Midscene 技能组索引](../README.md) · [组级 references/](../references/) · [转化自检](../references/conversion-and-checklist.md)
- [Skills 目录规范](../../README.md)

功能用例编写请用 **测试用例设计**（非本分类）。
