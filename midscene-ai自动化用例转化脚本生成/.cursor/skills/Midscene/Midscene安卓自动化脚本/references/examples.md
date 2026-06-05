# YAML 示例片段

## 单任务冒烟

```yaml
config:
  ai:
    actionTimeout: 30000
    retryInterval: 200
  page:
    defaultWait: 200

android:
  deviceId: "192.168.140.140"

agent:
  testId: "WiFi开关"
  generateReport: true
  aiActContext: "权限弹窗点允许；系统更新提示点跳过"

tasks:
  - name: "TC001-关闭WiFi后状态栏"
    flow:
      - ai: 从主界面进入系统设置
      - ai: 在 WiFi 列表中关闭 WiFi 开关
      - ai: 返回主界面
      - aiAssert: 状态栏 WiFi 图标消失
```

## 多任务（内联前置，无 shareSteps）

```yaml
tasks:
  - name: "登录-管理员"
    flow:
      - ai: 点击登录
      - ai: 输入用户名 test
      - ai: 输入密码 "******"
      - ai: 点击登录按钮
      - aiAssert: 主界面显示任务列表

  - name: "创建配送任务"
    flow:
      - ai: 点击配送
      - ai: 点击请选择目的地
      - ai: 选择第一个目的地
      - ai: 点击关门出发
      - aiAssert: 页面显示配送进行中
```

## B 档注释示例

```yaml
  - name: "时间同步-屏显"
    flow:
      - ai: 进入系统设置，将时间改为 14:30
# 人工验收：SSH Linux 从板执行 date，与屏显偏差 ≤1s
```

## 快速任务：地图进入 + 保存为任务（界面和任务设置）

```yaml
# 区域名请与实机一致；关联：新建任务_自动化测试.yaml
agent:
  aiActContext: >
    已建图且定位成功。权限弹窗点允许。
    保存为任务建议命名「快速任务自动化测试」便于清理。

tasks:
  - name: "12903941-首页点击地图进入快速任务"
    flow:
      - ai: 等待直到主界面地图页显示当前地图名及 A/B/C 作业区
      - ai: 点击地图上「A区草坪」绿色区域
      - ai: 等待直到进入「快速任务」页面
      - aiAssert: 标题「快速任务」；右侧有任务列表与可添加区域

  - name: "12903804-DESIGN-保存为任务弹窗键盘"
    flow:
      - ai: 确认任务列表至少有 1 条后点击「保存为任务」
      - ai: 等待直到弹出「保存任务」命名弹窗
      - aiAssert: 输入框自动聚焦且软键盘弹出
      - ai: 输入「快速任务自动化测试」后收起键盘
      - aiAssert: 弹窗在屏幕居中显示

  - name: "12903872-保存Toast回首页"
    flow:
      - ai: 在保存任务弹窗点击「保存」
      - aiAssert: 绿色 Toast「任务已保存」
      - ai: 等待直到返回主界面
      - aiAssert: 任务列表出现「快速任务自动化测试」
```

同源规则（5 次上限、拖拽、× 删除）与新建/编辑套件保持一致，见 [domain-ui-task-setting.md](./domain-ui-task-setting.md)。

完整长示例（配送、登录、shareSteps/dependsOn、数据准备）见 [examples-full.md](./examples-full.md)。精修时以 [yaml-schema.md](./yaml-schema.md) 与 [field-to-flow.md](./field-to-flow.md) 为准。
