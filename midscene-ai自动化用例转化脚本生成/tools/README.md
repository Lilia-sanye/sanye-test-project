# Midscene 流水线工具

在**仓库根目录**执行。安装依赖：`pip install -r requirements-midscene.txt`。

| 脚本 | 用途 |
|------|------|
| `screen_ui_task_cases.py` | xlsx/csv → 分档 CSV + 报告 + drafts |
| `build_midscene_yaml.py` | A 档 CSV → 机械 YAML 草稿/终稿 |
| `traceability_matrix.py` | 用例 ID ↔ scripts task 追溯矩阵 |
| `apply_device_env.py` | `config/env.yaml` ↔ `scripts` 的 `{{}}` 占位符 |

**维护者专用**（勿打进分发包）：`migrate_env_flow_steps.py`、`fix_task_names.py`。

参数全文：`.cursor/skills/Midscene/references/tools.md`。
