# 规范转化与发布自检

核心原则：**先筛选定档，再只转化 A 档；机械生成只是草稿，准确靠人工精修 + 单条试跑。**

## 功能用例源头要求

| 要求 | 推荐写法 | 避免 |
|------|----------|------|
| 步骤是机载屏动作 | `进入系统设置` → `关闭 WiFi` → `查看状态栏图标` | `验证 WiFi 模块正常` |
| 一步一事 | 每步 10～30 字，对应一条 `ai:` | 一步里塞多个操作 |
| 预期可观察 | `状态栏显示 HH:MM` | 需 SSH/日志/仪器才能判定 |
| 前置写清环境 | 写在「前置条件」列 | 混进步骤描述 |
| 无模板外壳 | 纯业务句 | `【测试环境】`…`【操作步骤】` 等 |

字段映射与 `ai`/`aiAssert` 细则见：

- [field-to-flow.md](../Midscene安卓自动化脚本/references/field-to-flow.md)
- [ai-instructions.md](../Midscene安卓自动化脚本/references/ai-instructions.md)

## 设计稿融合（有截图/标注时）

有 **Figma 链接** 且 Cursor 已启用 Figma MCP 时，优先走 [figma-to-midscene.md](./figma-to-midscene.md)（`get_design_context` 提取文案与标注）；无 MCP 时按下述截图流程。

1. **读图**：列出可见控件、交互规则（添加/删除/上限/键盘/Toast 等）。
2. **对照 CSV**：用 `midscene自动化输出/cases/*_可自动化用例.csv` 找已有 `用例ID`；缺口标为设计补充。
3. **命名**：
   - 已有 ID：`name: "{用例ID}-{标题摘要}"`
   - 仅设计稿：`name: "DESIGN-{简述}"` 或 `name: "{用例ID}-DESIGN-{简述}"`（同场景合并为一条 task）
4. **合并**：同一行为只保留一条 `flow`，`name` 同时体现 ID 与设计来源。
5. **融合进已有套件**：去重 task、用 `# --- 分段 ---` 注释；规则与姊妹套件一致时写文件头「关联」注释（见 [domain-ui-task-setting.md](../Midscene安卓自动化脚本/references/domain-ui-task-setting.md)）。

## 准确版工作流

```
整理 xlsx/csv（+ 可选设计稿）
  → screen_ui_task_cases.py
  → 人工评审 CSV 档位（约 5～10 分钟）
  → 按模块拆套件名（见 domain-ui-task-setting.md）
  → 提炼共享前置 → agent.aiActContext
  → 仅 A 档：build_midscene_yaml.py 得草稿（或跳过，直接手写分套件终稿）
  → Midscene安卓自动化脚本 逐条精修
  → midscene自动化输出/scripts/ + midscene自动化输出/report/*_自动化用例说明.md
  → traceability_matrix.py → report/*_自动化追溯矩阵.md（对照 A 档待转化清单）
  → 先跑 1～2 条 task（进入+一条主路径）→ 再扩套件
  → 失败回流：改用例或 YAML，并更新档位 / device-lexicon
```

## 发布前自检（每条 task）

- [ ] 来源用例为 **A 档**（或 C 档已改写后再转化）
- [ ] 每条 `ai:` 对应原步骤一行，无跳步、无抽象句
- [ ] 有且仅有 **一条** 主 `aiAssert`，与「预期结果」一致且可观察
- [ ] 弹窗/权限/登录等已在 `aiActContext` 或注释说明
- [ ] 未使用 `assert:`；无 Linux/ADB 断言写在 `aiAssert` 内
- [ ] `android.deviceId`、`androidAdbPath`（Windows）已填写
- [ ] 含 `config` 块（`actionTimeout` / `retryInterval` / `defaultWait`）
- [ ] `task.name` 含用例 ID 或 `DESIGN-` 前缀（便于追溯）
- [ ] 地图/区名与实机一致，文件头有「实机文案」注释
- [ ] 已去掉旧式仅整句引号的 `ai:`；使用 `ai:` / `aiAssert:` 祈使句
- [ ] 单条实机 `midscene run` 通过后再并入大套件

### 新增自检项（Task 设计质量）

- [ ] **无「若有…」条件分支**：无 `若有未设置XX提示，点击关闭` 等让 AI 自行判断分支的步骤（唯一例外是弹窗关闭：`若弹出弹窗或对话框，点击关闭`）
- [ ] **每个 task 自包含闭环**：跳转类 task 开头 `等待直到进入主界面地图页`，结尾 `等待直到回到主界面地图页` + 断言确认
- [ ] **断言具体化**：无 `非白屏、无闪退` / `页面显示正常` / `验证模块正常` 等模糊表述，全部替换为具体文字或控件名称
- [ ] **长链路已拆分**：超过 3 步页面跳转的 task 已拆分为独立 task
- [ ] **变量注释保留**：每个 `{{key}}` 步骤上方有 `# - ai:` / `# - aiAssert:` 原始字面量注释行
- [ ] **env.yaml 变量一致**：使用的所有 `{{key}}` 均在 `midscene自动化输出/config/env.yaml` 中有对应值；`device.id` 已填实机 ID（非 `"<设备ID>"`）
- [ ] **apply 验证通过**：`python tools/apply_device_env.py --all` 执行后所有占位符已替换为实际文案

## 终稿交付清单（套件级）

- [ ] YAML：`midscene自动化输出/scripts/<套件>_自动化测试.yaml`
- [ ] 说明：`midscene自动化输出/report/<套件>_自动化用例说明.md`（模板见 [deliverable-report-template.md](./deliverable-report-template.md)）
- [ ] 追溯：`python tools/traceability_matrix.py` → `report/<stem>_自动化追溯矩阵.md` / `.csv`
- [ ] 文件头：`deviceId` 占位、前置条件、关联套件路径
- [ ] `agent.aiActContext`：权限/更新/**副作用**（保存命名、开始作业、删数据）
- [ ] 危险 task 末尾 `# 人工：…` 或说明 md「风险」列标注

## 工具边界

| 环节 | 工具 | 自动化程度 | 人工必做 |
|------|------|------------|----------|
| 分档 | `tools/screen_ui_task_cases.py` | 规则 + 关键词 | 纠偏 A/B；整机域勿强行标 A |
| 草稿 YAML | `tools/build_midscene_yaml.py` | 机械拆步 + 首条预期 | 逐条改 `ai`、加 `等待直到…` |
| 追溯矩阵 | `tools/traceability_matrix.py` | 扫描 task `name` 中用例ID | 补全未覆盖 A 档；DESIGN task 人工对照 |
| 终稿 | 安卓自动化技能 | 按映射精修 | 试跑、合并共享前置到 `aiActContext` |
| 执行 | `midscene run` | 视觉 AI | 步骤含可见文案；不稳定处拆分等待 |

命令见 [tools.md](./tools.md)。

## 与功能用例设计配合

- 新需求：先用 `测试用例设计` 写功能用例（步骤带 UI 动词）。
- 要自动化：再走 Midscene 组。
- 可选：用例表增加列 **「自动化档位」**（空 / A / B / N），与 `midscene自动化输出/cases` 同步。
