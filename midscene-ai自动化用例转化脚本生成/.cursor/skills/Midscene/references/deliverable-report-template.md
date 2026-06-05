# 终稿交付：自动化用例说明（模板）

精修终稿 YAML 后，在 `midscene自动化输出/report/` 增加 **与套件同 stem** 的说明文档，便于评审与追溯。

**路径**：`midscene自动化输出/report/<套件stem>_自动化用例说明.md`  
示例：`快速任务_自动化测试.yaml` → `midscene自动化输出/report/快速任务_自动化用例说明.md`

---

## 文档结构（复制填空）

```markdown
# <页面名> — Midscene 自动化说明

**设计稿 / 需求**：（简述或贴图说明）
**终稿脚本**：`midscene自动化输出/scripts/<文件名>.yaml`（**N 条** task）

## 前置条件

- 已建图、定位成功、机器空闲（按项目调整）
- 填写 `android.deviceId`
- （副作用说明：保存写库 / 开始作业 / 删任务等）

## 关联套件

| 套件 | 入口 / 关系 |
|------|-------------|
| `xxx_自动化测试.yaml` | … |

## 任务清单

| # | task name | 用例ID / DESIGN | 风险 |
|---|-----------|-----------------|------|
| 1 | … | 1290xxxx | — |

## 执行

\`\`\`bash
midscene run midscene自动化输出/scripts/<文件名>.yaml
\`\`\`

## 注意

- 固定测试数据命名（便于测后清理）：…
- 实机文案与 [device-lexicon.md](../Midscene安卓自动化脚本/references/device-lexicon.md) 对齐
```

## 追溯约定

- `task.name` 建议：`{用例ID}-{标题摘要}` 或 `{用例ID}-DESIGN-{简述}`
- 说明 md 的「用例ID」列与 CSV `用例ID` 列一致
- 大表筛选报告中的 ID 可通过说明 md 反查落在哪个终稿 yaml
