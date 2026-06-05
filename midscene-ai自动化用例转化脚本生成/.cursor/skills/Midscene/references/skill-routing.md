# Midscene 技能路由（避免选错）

| 用户说法 | 应选技能 | 产出物 |
|----------|----------|--------|
| 写/设计功能测试用例、PISTF、七列表 | **测试用例设计** | .md / .csv 用例 |
| 评审用例、查覆盖 | **测试用例评审** | 评审意见 |
| 写测试方案 | **测试方案设计** | 方案文档 |
| 哪些用例能做成 Midscene、分档 | **Midscene功能用例筛选** | 分档 CSV + 报告 + YAML 草稿 |
| 写/精修 Midscene YAML、`midscene run` | **Midscene安卓自动化脚本** | `.yaml` + `midscene自动化输出/report/*_说明.md` |
| 设计稿/截图补快速任务等 | **筛选**（对照 CSV）→ **安卓自动化** | DESIGN 命名 task |
| **Figma 链接 + CSV → YAML** | **筛选** → Figma MCP（[figma-to-midscene.md](./figma-to-midscene.md)）→ **安卓自动化** | 终稿 yaml + 可选 figma 对照 md |
| 仅 PNG、无 Figma MCP | **安卓自动化** + [conversion-and-checklist.md](./conversion-and-checklist.md) | DESIGN 命名 task |
| 界面和任务设置多套件 | **安卓自动化** + [domain-ui-task-setting.md](../Midscene安卓自动化脚本/references/domain-ui-task-setting.md) | 分文件终稿 |

## 不要用 Midscene 组做的事

| 需求 | 应改用 |
|------|--------|
| 从零写七列表 / PISTF 功能用例 | `../测试用例设计/` |
| 评审用例质量与覆盖 | `../测试用例评审/` |
| 写测试方案 / QA 计划 | `../测试方案设计/` |

## 旧称对照（仅兼容触发，文档勿再使用）

| 旧称 | 现名 |
|------|------|
| 用例筛选与AI生成 | Midscene功能用例筛选 |
| midscene-安卓测试用例生成 | Midscene安卓自动化脚本 |
| midscene-安卓测试输出 | midscene自动化输出 |
