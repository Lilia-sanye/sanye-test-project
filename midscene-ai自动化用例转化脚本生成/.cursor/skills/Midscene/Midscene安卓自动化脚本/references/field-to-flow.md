# 功能用例字段 → YAML 映射

| 来源字段 | 写入 YAML | 注意 |
|----------|-----------|------|
| 前置条件（业务部分） | `agent.aiActContext` 或 task 首条前的 `# 前置：` 注释 | 共性前置放 agent 级 |
| 操作步骤 / 步骤描述 | 每步一行 `ai:` | 按 `1、`、`1.` 拆行；含界面可见文案 |
| 预期结果 | 最后一条 `aiAssert:` | 一条主断言、≤120 字；多条预期可拆多条用例 |
| 用例标题 | `tasks[].name` | 建议 `{用例ID}-{标题}`，去掉 `TC-` 前缀 |
| 用例等级 | 套件分批 | 优先 `P0` + **A 档** 单独成套件 |

## 转化前剥离

来自满袋检测等模板的包裹须先剥离（见筛选技能 [column-mapping.md](../../Midscene功能用例筛选/references/column-mapping.md)）。

## 机械转化后必改

`tools/build_midscene_yaml.py` 产出仅为草稿，精修时至少：

1. 抽象句改为带 UI 文案的祈使句。
2. 不稳定步骤前加 `等待直到…`。
3. 合并重复前置到 `aiActContext`。
4. B 档非 UI 预期移到注释或 B 档 CSV「人工验收项」。

发布自检见 [../../references/conversion-and-checklist.md](../../references/conversion-and-checklist.md)。
