# 环境变量配置（单文件）

**唯一配置源**：[`env.yaml`](env.yaml)

按文件内分节维护（`device` / `map` / `zones` / `tasks` / `home` / `ui`），换台架只改此文件。

## 与 scripts 的关系

| 位置 | 约定 |
|------|------|
| `scripts/*_自动化测试.yaml` | 活跃步骤使用 `{{节.键}}`；**原步骤**在同一 `flow` 下以 `# - ai:` 注释保留 |
| `agent.aiActContext` / `android` | 直接写 `{{device.id}}` 等，不注释 |
| 注释行 | `apply` 不替换，保留历史字面量对照 |

## 命令

```bash
# midscene run 前：占位符 → 实机字面量
python tools/apply_device_env.py --all

# 从实机抄回文案后：字面量 → 占位符（不改 # 注释行、不改 task name）
python tools/apply_device_env.py --inject --all
```

## 键名速查

| 键 | 示例用途 |
|----|----------|
| `map.name` / `map.nameAlt` | 地图栏（· 与 - 两种标点） |
| `zones.a.label` | 作业区短名 |
| `zones.a.mapLabel` | 含面积标注 |
| `zones.detail.a` | 有任务套件子区名 |
| `tasks.defaultSet` | 默认任务集 |
| `home.emptyPanelTitle` | 无任务面板标题 |
| `home.guideTitle` | 「点击地图区域」引导 |

动态 UI（电量百分比、具体时刻）**不要**写入 config，步骤用语义断言。
