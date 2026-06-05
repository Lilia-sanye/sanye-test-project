# Midscene 技能包 — 安装与首次使用

本包用于在 **Cursor**（或 **Trae**）中，将功能用例筛选、分档并生成/维护 Midscene 安卓 UI 自动化 YAML。

## 1. 解压后的目录结构

```
<你的项目根>/
├── INSTALL.md                          # 本文件
├── requirements-midscene.txt
├── .cursor/skills/Midscene/            # Agent 技能（必放）
├── tools/                              # 流水线脚本
│   ├── screen_ui_task_cases.py
│   ├── build_midscene_yaml.py
│   ├── traceability_matrix.py
│   └── apply_device_env.py
└── midscene自动化输出/
    ├── config/env.yaml                 # 实机文案变量（必改）
    ├── cases/  report/  drafts/  scripts/
    └── README.md
```

将本包内容**合并到目标项目根**（保持上述相对路径），不要多嵌套一层目录。

## 2. 环境准备

### 2.1 Python（筛选与 config 注入）

```bash
pip install -r requirements-midscene.txt
```

| 脚本 | 依赖 |
|------|------|
| `screen_ui_task_cases.py` | openpyxl（读 xlsx） |
| `apply_device_env.py` | pyyaml |
| 其余 | 标准库 |

### 2.2 Midscene CLI（实机执行）

```bash
npm install -g @midscene/cli
adb devices
```

确认 `adb` 在 PATH；Windows 可在 `config/env.yaml` 中配置 `device.adbPath`。

### 2.3 Cursor / Trae 技能

- **Cursor**：确保存在 `.cursor/skills/Midscene/`（本包已含）。
- **Trae**：将技能同步到 Trae 目录：

```powershell
Remove-Item -Path ".trae\skills\Midscene" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -Path ".cursor\skills\Midscene" -Destination ".trae\skills\Midscene" -Recurse -Force
```

对话时推荐 @ 引用：

```
@.cursor/skills/Midscene/README.md
```

## 3. 配置实机变量

编辑 **`midscene自动化输出/config/env.yaml`**（单文件，按节维护）：

| 节 | 必改项 |
|----|--------|
| `device` | `id`、`adbPath` |
| `map` | `name`（注意 · / - 与实机一致） |
| `zones` | `a/b/c.label`、`mapLabel`、`detail.*` |
| `tasks` | `defaultSet`、`secondarySet` 等任务集名 |

说明见 `midscene自动化输出/config/README.md`。

## 4. 标准流水线

在**项目根目录**执行：

```bash
# ① 筛选（输入改为你的 xlsx/csv）
python tools/screen_ui_task_cases.py --input "修订版本/你的用例表.xlsx"

# ② 人工评审 midscene自动化输出/cases/*_可自动化用例.csv 的「执行档位」

# ③ Agent 精修 或 机械草稿后再改
python tools/build_midscene_yaml.py \
  --csv midscene自动化输出/cases/你的表_可自动化用例.csv \
  --out midscene自动化输出/scripts/某套件_自动化测试.yaml

# ④ 追溯矩阵（可选）
python tools/traceability_matrix.py

# ⑤ 注入环境变量（midscene run 前必做）
python tools/apply_device_env.py --all

# ⑥ 执行
midscene run midscene自动化输出/scripts/快速任务_自动化测试.yaml
```

**约定**：`scripts/` 内终稿保留 `{{节.键}}` 占位符；注释行 `# - ai:` 为原步骤对照，不参与注入。

## 5. 用 Cursor Agent 时怎么说

| 意图 | 示例 |
|------|------|
| 筛选用例 | 按 Midscene 功能用例筛选，筛 `修订版本/xxx.xlsx` |
| 写 YAML | 按 Midscene 安卓自动化脚本精修 `scripts/快速任务_自动化测试.yaml` |
| 全流程 | 按 Midscene 组文档从 xlsx 筛到终稿 YAML |

细则：`.cursor/skills/Midscene/README.md`。

## 6. 常见问题

**Q：`screen_ui_task_cases` 报找不到 xlsx**  
A：用 `--input` 指定你的用例表路径；默认路径为 `修订版本/界面和任务设置.xlsx`，可自建 `修订版本/` 目录。

**Q：midscene run 仍显示 `{{map.name}}`**  
A：未执行 `python tools/apply_device_env.py --all`，或 `env.yaml` 缺少对应键。

**Q：打包后缺少 scripts 示例**  
A：在仓库根执行 `.\pack-midscene-skill.ps1`，会将 `midscene自动化输出/` **整目录**复制进包内。

## 7. 文档索引

| 文档 | 内容 |
|------|------|
| `.cursor/skills/Midscene/README.md` | 技能入口、触发词、Figma |
| `midscene自动化输出/README.md` | 产出目录与套件索引 |
| `.cursor/skills/Midscene/references/tools.md` | 工具参数全文 |

---

打包脚本：仓库根目录 `pack-midscene-skill.ps1`（维护者生成 zip 时分发）。
