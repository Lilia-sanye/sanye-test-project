# 机载屏文案词表（人工维护）

> **执行源**：优先维护 [`midscene自动化输出/config/`](../../../../midscene自动化输出/config/README.md)（按套件拆分 + `apply_device_env.py` 同步）。  
> 本表供 Agent 写稿参考；试跑后以实机为准更新 **对应 suite 配置**，勿只改本文件不同步 scripts。

## 配置入口速查

| 类别 | 配置文件 |
|------|----------|
| 设备 ID / adb | `config/device.yaml` |
| 主界面无任务（A/B/C 草坪 + 面积） | `config/suites/主界面_有地图无任务.yaml` |
| 主界面有任务（A区-前草坪 等） | `config/suites/主界面_有地图有任务.yaml` |
| 快速任务 / 保存任务名 | `config/suites/快速任务.yaml` |
| 新建任务保存名 | `config/suites/新建任务.yaml` |
| 编辑任务种子名 / 改名 | `config/suites/编辑任务.yaml` |
| 页面标题（快速任务、新建任务…） | `config/fragments/ui-pages.yaml` |

## 设计稿 vs 实机（参考）

| 类别 | 设计/文档常用 | 实机可能变体 | 备注 |
|------|---------------|--------------|------|
| 地图名 | 绿城·中央公园 | （按当前地图） | 改 `map.name` |
| 作业区（无任务套件） | A区草坪、B区草坪、C区草坪 | A区-前草坪 等 | 改对应 suite 的 `zones.*` |
| 作业区（有任务套件） | A区-前草坪、B区-东侧花园 | 与无任务套件**分开配置** |
| 页面标题 | 快速任务、新建任务、编辑任务 | — | `fragments/ui-pages.yaml` |
| Toast | 任务已保存、任务已删除 | — | `fragments/ui-toasts.yaml` |

## 维护流程

1. `midscene run` 失败 → 实机截图抄**可见原文**。  
2. 只改**该套件** `config/suites/*.yaml`（或 `device.yaml`）。  
3. `python tools/apply_device_env.py --suite <套件>`。  
4. 再跑对应 `scripts/<套件>_自动化测试.yaml`。

勿将 password、真实 deviceId 写入技能文档；deviceId 只放 `config/device.yaml`（本地维护，勿提交敏感值）。
