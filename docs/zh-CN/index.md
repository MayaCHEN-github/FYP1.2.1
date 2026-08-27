**语言：** [English](../en/index.md) · 简体中文 · [繁體中文（香港）](../zh-HK/index.md)

# fyp1.2.1 项目导读

这是一个毕业设计（FYP）实验仓库，用来评估大语言模型在「系统提示要求保护隐私数据库」时，是否会被各类越狱提示（jailbreak prompt）诱导泄露 [`data/database.json`](../../data/database.json) 中的模拟个人信息。

项目有两条使用路径：用 Gradio 界面并排对比两个模型的单次响应；用命令行脚本批量重复实验、汇总混淆矩阵并生成热力图。

更短的安装与命令一览见根目录 [README.zh-CN.md](../../README.zh-CN.md)。

## 文档地图

| 文档 | 用途 |
| --- | --- |
| [端到端流程](walkthrough.md) | 从配置到结果分析的完整路径 |
| [模型层](modules/models.md) | 如何调用 OpenAI 与 Hugging Face 推理 |
| [提示词层](modules/prompts.md) | 种子、越狱模板、系统提示的组装 |
| [会话层](modules/conversation.md) | 对话历史与流式输出 |
| [检测层](modules/detection.md) | 泄露检测与拒绝检测 |
| [批量测试](modules/batch-testing.md) | `leak_test.py` 与结果分析 |
| [支持的模型](references/models.md) | 模型别名与后端映射 |
| [提示词清单](references/prompts.md) | 全部 prompt 键名与类型 |
| [混淆矩阵定义](references/confusion-matrix.md) | TP/FP/TN/FN 在本项目中的含义 |
| [结果文件格式](references/result-format.md) | `results/` 与 `analysis_results/` 字段 |
| [术语表](glossary.md) | 中文阅读句柄与英文标识对照 |

## 阅读路径

| 你想做什么 | 从这里开始 |
| --- | --- |
| 快速理解项目在测什么 | 本页 → [端到端流程](walkthrough.md) Step 1–3 |
| 跑 Gradio 演示 | [端到端流程](walkthrough.md) Step 4 |
| 跑批量实验并看指标 | [端到端流程](walkthrough.md) Step 5–7 → [批量测试](modules/batch-testing.md) |
| 改越狱模板或系统提示 | [提示词层](modules/prompts.md) → [提示词清单](references/prompts.md) |
| 换模型或接新 API | [模型层](modules/models.md) → [支持的模型](references/models.md) |
| 理解泄露/拒绝怎么判 | [检测层](modules/detection.md) → [混淆矩阵定义](references/confusion-matrix.md) |

## 运行前准备

1. 安装依赖：`pip install -r requirements.txt`
2. 复制 [`config.example.json`](../../config.example.json) 为仓库根目录的 `config.json`，填入 `api_key`（OpenAI）与 `huggingface_token`（Hugging Face Inference）。
3. 确认 [`data/database.json`](../../data/database.json) 存在；系统提示会把整库注入 `{database}` 占位符。

> [!WARNING]
> 不要把含真实密钥的 `config.json` 提交进 git。文档不展开密钥内容。

画热力图前额外安装：`pip install pandas matplotlib numpy`。

## 变更记录

见 [changelog.md](changelog.md)。
