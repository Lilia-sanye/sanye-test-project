# Midscene YAML 完整示例

> 精修终稿前请对照 [yaml-schema.md](./yaml-schema.md)、[field-to-flow.md](./field-to-flow.md)。  
> `shareSteps` / `dependsOn` / `ref:` 等字段若 CLI 报错，按 [yaml-schema.md](./yaml-schema.md) 退化为 flow 内联。

---

## 示例 1：配送流程（智能等待 + aiAssert）

```yaml
config:
  ai:
    actionTimeout: 30000
    retryInterval: 200
  page:
    defaultWait: 200

android:
  deviceId: "192.168.140.140"
  androidAdbPath: "D:/soft/android-sdk/platform-tools/adb.exe"

agent:
  testId: "配送流程测试"
  groupName: "功能测试套件"
  groupDescription: "配送流程自动化测试"
  generateReport: true
  autoPrintReportMsg: true
  reportFileName: "配送流程测试报告"
  replanningCycleLimit: 30
  aiActContext: "如果出现权限弹窗，点击允许；如果出现更新提示，跳过；如果出现确认对话框，点击确认"

tasks:
  - name: 配送流程
    repeat: 1
    flow:
      - ai: 点击配送
      - ai: 点击请选择目的地
      - ai: 选择02，点击确认
      - ai: 关门出发
      - ai: 等待直到页面显示"开门取物"
      - ai: 开门取物
      - ai: 点击完成
      - ai: 等待直到页面显示"去配送"
      - ai: 点击左上角退出
      - aiAssert: 页面出现配送、设置等文字
```

---

## 示例 2：用户登录

```yaml
config:
  ai:
    actionTimeout: 30000
    retryInterval: 200
  page:
    defaultWait: 200

android:
  deviceId: "192.168.140.140"
  androidAdbPath: "D:/soft/android-sdk/platform-tools/adb.exe"

agent:
  testId: "登录测试"
  groupName: "用户模块测试"
  generateReport: true
  aiActContext: "权限弹窗点击允许，更新提示点击跳过"

tasks:
  - name: 用户登录
    repeat: 1
    flow:
      - ai: 点击登录按钮
      - ai: 输入用户名 "test@example.com"
      - ai: 输入密码 "password123"
      - ai: 点击确认登录
      - ai: 等待直到页面显示"欢迎"
      - aiAssert: 页面显示用户头像和用户名
```

---

## 示例 3：任务依赖 + shareSteps（组织约定）

**场景**：列表显示依赖先创建任务。

```yaml
config:
  ai:
    actionTimeout: 30000
    retryInterval: 200
  page:
    defaultWait: 200

android:
  deviceId: "192.168.140.140"
  androidAdbPath: "D:/soft/android-sdk/platform-tools/adb.exe"

agent:
  testId: "任务管理测试套件"
  groupName: "任务管理模块测试"
  generateReport: true
  aiActContext: "权限弹窗点击允许，确认对话框点击确认"

shareSteps:
  - name: 登录系统
    flow:
      - ai: 点击登录按钮
      - ai: 输入用户名 "admin"
      - ai: 输入密码 "password123"
      - ai: 点击确认登录
      - ai: 等待直到页面显示"主页"
      - aiAssert: 页面显示主页标识

  - name: 清理测试数据
    flow:
      - ai: 点击任务列表
      - ai: 选择测试任务
      - ai: 点击删除
      - ai: 确认删除
      - aiAssert: 任务已删除

tasks:
  - name: 创建新任务
    dependsOn: ["登录系统"]
    dataPreparation:
      - ai: 点击任务管理
      - ai: 点击新建任务
    flow:
      - ref: 登录系统
      - ai: 点击任务管理
      - ai: 点击新建任务
      - ai: 输入任务名称 "自动化测试任务-001"
      - ai: 输入任务描述 "这是一个测试任务"
      - ai: 选择优先级 "高"
      - ai: 点击保存按钮
      - ai: 等待直到页面显示"创建成功"
      - aiAssert: 页面显示任务创建成功提示
    cleanup:
      - ai: 点击返回任务列表

  - name: 查看任务列表
    dependsOn: ["创建新任务"]
    precondition: "系统中必须存在至少一个任务"
    flow:
      - ref: 登录系统
      - ai: 点击任务管理
      - ai: 点击任务列表
      - ai: 等待直到页面显示任务列表
      - aiAssert: 页面显示"自动化测试任务-001"
      - aiAssert: 任务列表不为空

  - name: 编辑任务
    dependsOn: ["查看任务列表"]
    continueOnFailure: false
    flow:
      - ref: 登录系统
      - ai: 点击任务列表
      - ai: 选择"自动化测试任务-001"
      - ai: 点击编辑按钮
      - ai: 修改任务名称为 "自动化测试任务-已编辑"
      - ai: 点击保存
      - aiAssert: 任务编辑成功
      - aiAssert: 列表中显示新的任务名称

  - name: 删除测试任务
    dependsOn: ["编辑任务"]
    enabled: true
    continueOnFailure: true
    flow:
      - ref: 登录系统
      - ref: 清理测试数据
      - aiAssert: 任务列表中不再显示测试任务
```

---

## 示例 4：数据准备与清理

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
  testId: "多任务测试套件"
  groupName: "完整流程测试"
  generateReport: true

shareSteps:
  - name: 初始化环境
    flow:
      - ai: 点击设置
      - ai: 重置测试数据
      - aiAssert: 数据重置成功

  - name: 登录系统
    flow:
      - ai: 点击登录
      - ai: 输入用户名 "test"
      - ai: 输入密码 "123456"
      - ai: 点击确认

tasks:
  - name: 准备测试数据
    dataPreparation:
      - ref: 初始化环境
      - ref: 登录系统
    flow:
      - ai: 点击新建任务
      - ai: 输入任务名称 "任务1"
      - ai: 点击保存
      - ai: 点击新建任务
      - ai: 输入任务名称 "任务2"
      - ai: 点击保存
      - ai: 点击新建任务
      - ai: 输入任务名称 "任务3"
      - ai: 点击保存
      - aiAssert: 任务列表显示3个任务

  - name: 批量操作任务
    dependsOn: ["准备测试数据"]
    retryOnFailure: 2
    flow:
      - ref: 登录系统
      - ai: 点击任务列表
      - ai: 全选所有任务
      - ai: 点击批量操作
      - ai: 选择批量移动
      - ai: 选择目标分类
      - ai: 确认操作
      - aiAssert: 批量操作成功

  - name: 清理环境
    dependsOn: ["批量操作任务"]
    cleanup:
      - ai: 点击任务管理
      - ai: 清空所有任务
      - aiAssert: 任务列表为空
    flow:
      - ref: 登录系统
      - ai: 点击设置
      - ai: 清空测试数据
      - aiAssert: 测试环境已清空
```
