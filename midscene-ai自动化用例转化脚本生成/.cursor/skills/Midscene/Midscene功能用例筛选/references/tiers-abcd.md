# 执行档位 A/B/C/D

筛选结果必须为每条用例标注 **执行档位**，写入 CSV 列 `执行档位`、`档位说明`。

| 档位 | 含义 | 后续动作 |
|------|------|----------|
| **A** | 机载 UI 步骤清晰，无 ADB/Linux/物理/长重启硬阻碍 | 直接生成 Midscene `tasks[].flow` |
| **B** | 含 UI 操作，但验收依赖 ADB、Linux 从板、遮罩/拔卡、长时重启等 | YAML 只写 Android 段；断言拆到「人工验收项」 |
| **C** | 原步骤仅「查看/观察」或缺关键词，但属状态栏/主界面/地图等 **视觉可断言** | 改写为 `ai:` + `aiAssert:`，不标为不可转化 |
| **D** | 步骤缺失、无法推断操作、纯接口/性能/DB、整机域无 UI 动词 | 写入不可自动化 CSV |

## 硬阻碍（命中则不得标 A）

- `adb shell`
- `Linux从板`
- `timedatectl`
- `金属遮罩`
- `拔卡`
- `reboot` / 长时重启
- `重复测试N次` + 人工比对

与 `tools/screen_ui_task_cases.py` 中 `hard_block_patterns` 保持一致。

## B 档产出

- 文件：`midscene自动化输出/cases/<stem>_B档半自动.csv`
- 列：**人工验收项**（ADB/Linux/物理等不可写入 `aiAssert` 的验收）

B 档 YAML 写法见 [Midscene安卓自动化脚本/references/ai-instructions.md](../../Midscene安卓自动化脚本/references/ai-instructions.md)。
