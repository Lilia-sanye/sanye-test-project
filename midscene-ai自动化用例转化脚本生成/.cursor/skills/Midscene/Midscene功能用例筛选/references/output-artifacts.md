# 筛选产出物清单

根目录：**`midscene自动化输出/`**（入口 [README.md](../../../../midscene自动化输出/README.md)）。

## 目录树

```
midscene自动化输出/
├── cases/
│   ├── <stem>_可自动化用例.csv
│   ├── <stem>_B档半自动.csv
│   ├── <stem>_不可自动化用例.csv
│   └── <stem>_共享步骤.csv
├── report/
│   ├── <stem>_筛选报告.md
│   └── <stem>_依赖关系分析.md
└── drafts/
    └── <stem>_自动化测试_草稿.yaml
```

终稿 YAML：**`scripts/<套件>_自动化测试.yaml`**（非 drafts）。

## CSV 关键列

| 列 | 说明 |
|----|------|
| 执行档位 | A / B / C / D |
| 档位说明 | 分档理由 |
| 人工验收项 | 仅 B 档 CSV |

## 报告要点

**筛选报告**：总数、各档数量、关键词统计。

**依赖分析**：模块分档、建议终稿 `scripts/` 文件名、执行顺序。

Figma 对照、套件说明 md 也放在 **`report/`**。

流水线见 [../../references/pipeline-and-directories.md](../../references/pipeline-and-directories.md)。
