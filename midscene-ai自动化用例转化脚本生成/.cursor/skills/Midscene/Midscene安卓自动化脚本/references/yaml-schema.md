# Midscene YAML 结构与禁止项

## 最小可运行结构（优先）

不确定 CLI 版本时，只输出以下字段，再按需叠加 `dependsOn` / `shareSteps`：

```yaml
config:
  ai:
    actionTimeout: 30000
    retryInterval: 200
  page:
    defaultWait: 200

android:
  deviceId: "<adb devices 中的 ID>"
  androidAdbPath: "<Windows 建议绝对路径>"

agent:
  testId: "<测试ID>"
  groupName: "<报告组>"
  generateReport: true
  aiActContext: "权限允许；更新跳过；确认框点确认"

tasks:
  - name: "<任务名称>"
    flow:
      - ai: <操作>
      - aiAssert: <可观察断言>
```

## 必须包含

- `config`（含 `actionTimeout` / `retryInterval` / `defaultWait`）
- `android.deviceId`
- `agent.generateReport: true`（需要报告时）
- `tasks[].flow` 中至少一条 `ai:` 与一条 `aiAssert:`

## 禁止

- 使用 `assert:` 嵌套 `ai`（**只用** `aiAssert:`）
- 省略 `config`（默认超时过长）
- YAML 中写真实密码 / 生产 API Key
- 将 **B 档** Linux/ADB 验收写进 `aiAssert`
- 输出当前 CLI **无法解析** 的字段而不提供内联 fallback

## Agent 配置项

| 配置项 | 说明 |
|--------|------|
| `testId` | 测试唯一标识 |
| `groupName` | 报告分组 |
| `generateReport` | 是否生成报告 |
| `aiActContext` | 弹窗、权限、登录态等背景 |
| `replanningCycleLimit` | AI 重规划次数（默认 20） |

## 任务扩展字段（组织约定）

`dependsOn`、`precondition`、`dataPreparation`、`cleanup`、`shareSteps`、`ref:` — 若运行报错，改为 flow 内联重复步骤 + YAML 注释标明依赖。

## 产出路径

| 类型 | 路径 |
|------|------|
| 上游草稿（只读） | `midscene自动化输出/drafts/*_草稿.yaml` |
| **本技能终稿** | `midscene自动化输出/scripts/<套件>_自动化测试.yaml` |

不得将未审阅草稿直接当作终稿。
