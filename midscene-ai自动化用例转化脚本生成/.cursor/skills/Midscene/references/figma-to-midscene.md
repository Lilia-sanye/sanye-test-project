# Figma MCP 接入 Midscene

将 **Figma 设计稿**（通过 Cursor **Figma MCP**）与 **功能用例 CSV** 结合，产出可 `midscene run` 的 Android UI 自动化 YAML。  
**不是**一键转换器：Figma 提供控件文案与交互规则，步骤顺序与用例 ID 来自筛选后的 CSV，终稿须 Agent 精修 + 实机试跑。

## 前置条件

| 项 | 要求 |
|----|------|
| 环境 | **Cursor** 已启用 Figma 插件 MCP（`plugin-figma-figma`） |
| 权限 | Agent 可访问目标 Figma 文件（团队账号 / 链接权限） |
| 用例 | 已跑或准备跑 `screen_ui_task_cases.py`，有 `midscene自动化输出/cases/*_可自动化用例.csv` |
| 设计 | 每个屏面对应一个 **Frame**，图层命名清晰；关键规则有标注或说明 |
| Trae | 技能文档可同步；**Figma MCP 是否在 Trae 可用需单独配置**，不可用则导出 PNG 走 [conversion-and-checklist.md](./conversion-and-checklist.md)「设计稿融合」 |

## Figma MCP 读界面（常用工具）

| 工具 | 用途 | 何时用 |
|------|------|--------|
| `get_metadata` | 页面列表、节点树（ID + 名称） | 不知 node-id 时先扫结构 |
| `get_design_context` | **主工具**：截图 + 图层 + hints/标注 | 每个目标 Frame 调一次 |
| `get_screenshot` | 仅要高清截图 | 补充多状态（键盘弹出等） |

### URL → 参数

```
https://figma.com/design/<fileKey>/<fileName>?node-id=12-34
  → fileKey = <fileKey>
  → nodeId  = 12:34   （将 - 改为 :）
```

分支链接 `.../branch/<branchKey>/...` 时，**fileKey 用 branchKey**。

调用示例（Agent 使用 `CallMcpTool`，server: `plugin-figma-figma`）：

```json
{
  "toolName": "get_design_context",
  "arguments": {
    "fileKey": "<fileKey>",
    "nodeId": "12:34",
    "clientFrameworks": "android",
    "clientLanguages": "yaml"
  }
}
```

**不要**把 `get_design_context` 返回的 React/Tailwind 参考代码直接写入 `ai:`。Midscene 需要**中文祈使句 + 屏上可见文案**。

## 推荐流水线

```
① 功能用例 xlsx/csv
        ↓ screen_ui_task_cases.py
② midscene自动化输出/cases/*_可自动化用例.csv（A 档 + 用例ID）
        ↓
③ Figma：按屏 get_design_context（+ 多状态 Frame 各调一次）
        ↓
④ 产出对照表 midscene自动化输出/report/<stem>_figma-控件对照.md（可选但推荐）
        ↓
⑤ Midscene安卓自动化脚本：融合 CSV 步骤 + Figma 文案 → 终稿 YAML
        ↓
⑥ midscene run（deviceId、device-lexicon 对齐实机）
```

## Agent 执行清单（Figma + CSV → YAML）

1. **加载技能**：`Midscene/README.md`、`Midscene功能用例筛选/SKILL.md`、`Midscene安卓自动化脚本/SKILL.md`、本文档。
2. **筛选**：若无 CSV，先跑 `screen_ui_task_cases.py`；精修只取 **执行档位=A**（常用 P0）。
3. **枚举 Figma 屏**：`get_metadata(fileKey)` → 列出 Frame 名；与用户给的 node-id 或链接对齐。
4. **逐屏读取**：对每个 Frame 调 `get_design_context`；多状态（弹窗+键盘 / 弹窗居中）= **多个 node-id**，各读一次。
5. **提取表**（写入对照 md 或内存）：

   | Figma 图层/文案 | 类型 | 建议 ai:/aiAssert: | 对应用例ID |
   |-----------------|------|-------------------|------------|
   | 保存为任务 | 按钮 | `ai: 点击底部「保存为任务」` | 12903804 |
   | 任务已保存 | Toast | `aiAssert: Toast「任务已保存」` | 12903872 |

6. **对照 CSV**：同场景以 CSV「步骤描述」「预期结果」为主干；Figma 补**可见文案**与**设计标注规则**（标 `DESIGN-` 或 `{ID}-DESIGN-`）。
7. **选套件**：界面和任务设置见 [domain-ui-task-setting.md](../Midscene安卓自动化脚本/references/domain-ui-task-setting.md)（快速任务 / 新建 / 编辑 分文件）。
8. **写 YAML**：`tasks[].name` 含用例 ID；`flow` 末行 `aiAssert`；副作用见 [ai-instructions.md](../Midscene安卓自动化脚本/references/ai-instructions.md)。
9. **交付**：终稿 yaml + [deliverable-report-template.md](./deliverable-report-template.md)；说明 md 注明 Figma 节点链接。
10. **试跑**：先「进入 + 1 条主路径」`midscene run` 通过后再扩套件。

## Figma 字段 → Midscene 映射

| Figma 来源 | Midscene 写法 | 注意 |
|------------|---------------|------|
| 文本图层 `characters` / 按钮标签 | `ai: 点击「{原文}」` | 与实机一致；不一致改 [device-lexicon.md](../Midscene安卓自动化脚本/references/device-lexicon.md) |
| 设计标注 / hints | `aiAssert:` 或单独 `DESIGN-*` task | 如键盘弹出、弹窗居中 |
| Frame 名称 | 套件划分、task 分段注释 | 如 `快速任务`、`保存任务-键盘弹出` |
| 组件变体（多状态） | 多个 task 或分支 flow | 每状态一个 node-id |
| 布局坐标、CSS | **不用** | 视觉 AI 按语义找控件 |
| Code Connect 映射 | 仅作理解，**不生成代码** | 机载 Android 非 Web 组件树 |

## 可选产出：Figma 控件对照表

路径建议：`midscene自动化输出/report/<stem>_figma-控件对照.md`

```markdown
# <项目> Figma ↔ Midscene 对照

**Figma 文件**：https://figma.com/design/<fileKey>/...
**CSV**：midscene自动化输出/cases/<stem>_可自动化用例.csv
**终稿套件**：midscene自动化输出/scripts/<套件>_自动化测试.yaml

| Frame | node-id | 控件/文案 | CSV 用例ID | YAML task name |
|-------|---------|-----------|------------|----------------|
| 快速任务 | 12:34 | 开始作业 | 12903808 | 12903808-有任务时开始作业 |
```

便于评审覆盖与后续设计变更 diff。

## Frame ↔ 终稿套件（界面和任务设置示例）

| Figma Frame（示例名） | 建议终稿 yaml |
|----------------------|---------------|
| 主界面-有任务 | `主界面_有地图有任务_自动化测试.yaml` |
| 主界面-无任务 | `主界面_有地图无任务_自动化测试.yaml` |
| 快速任务 | `快速任务_自动化测试.yaml` |
| 新建任务 | `新建任务_自动化测试.yaml` |
| 编辑任务 | `编辑任务_自动化测试.yaml` |
| 保存任务弹窗 | 并入 `快速任务_…` 或 `新建任务_…` 的 DESIGN task |

实际 Frame 名以设计稿为准；上表为命名约定示例。

## 局限与降级

| 情况 | 处理 |
|------|------|
| Trae / 环境无 Figma MCP | 设计师导出 PNG，走截图 + 「设计稿融合」 |
| 地图多边形、拖拽 | Figma 只辅助文案；手势步骤靠 CSV + 试跑调优 |
| 设计稿与实机文案不一致 | 以实机为准，更新 device-lexicon |
| `get_design_context` 过大 | 先 `get_metadata` 拆子节点，分帧读取 |
| 开始作业 / 写库 | 必须标注副作用，不可仅靠 Figma 推断 |

## 与工具脚本边界

| 能力 | `build_midscene_yaml.py` | Figma MCP | Agent |
|------|--------------------------|-----------|-------|
| 读 Figma | ❌ | ✅ | 编排调用 |
| 读 CSV 用例 ID | ✅ | ❌ | 对齐 |
| 写终稿 YAML | 草稿 only | ❌ | ✅ 精修 |

详见 [tools.md](./tools.md)。

## 唤起示例（用户话术）

```
@.cursor/skills/Midscene/README.md
@.cursor/skills/Midscene/references/figma-to-midscene.md

Figma: https://figma.com/design/xxxxx/界面和任务设置?node-id=1-2
CSV: midscene自动化输出/cases/界面和任务设置_可自动化用例.csv
请读取「快速任务」相关 Frame，对照 A 档用例，更新 快速任务_自动化测试.yaml
```

## 相关文档

- [conversion-and-checklist.md](./conversion-and-checklist.md) — 设计稿融合、发布自检
- [domain-ui-task-setting.md](../Midscene安卓自动化脚本/references/domain-ui-task-setting.md) — 套件拆分
- [deliverable-report-template.md](./deliverable-report-template.md) — 说明 md 模板
- Cursor Figma MCP：`get_design_context` 为主；写回 Figma 用 `use_figma`（**本流程不需要**）
