# fyp1.2.1 项目导读

这是一个毕业设计（FYP）实验仓库，用来评估大语言模型在「系统提示要求保护隐私数据库」时，是否会被各类越狱提示（jailbreak prompt）诱导泄露 `data/database.json` 中的模拟个人信息。

项目有两条使用路径：用 Gradio 界面并排对比两个模型的单次响应；用命令行脚本批量重复实验、汇总混淆矩阵并生成热力图。

## 文档地图

| 文档 | 用途 |
| --- | --- |
| [端到端流程](walkthroughs/端到端流程.md) | 从配置到结果分析的完整路径 |
| [模型层](modules/模型层.md) | 如何调用 OpenAI 与 HuggingFace 推理 |
| [提示词层](modules/提示词层.md) | 种子、越狱模板、系统提示的组装 |
| [会话层](modules/会话层.md) | 对话历史与流式输出 |
| [检测层](modules/检测层.md) | 泄露检测与拒绝检测 |
| [批量测试](modules/批量测试.md) | `leak_test.py` 与结果分析 |
| [支持的模型](references/支持的模型.md) | 模型别名与后端映射 |
| [提示词清单](references/提示词清单.md) | 全部 prompt 键名与类型 |
| [混淆矩阵定义](references/混淆矩阵定义.md) | TP/FP/TN/FN 在本项目中的含义 |
| [结果文件格式](references/结果文件格式.md) | `results/` 与 `analysis_results/` 字段 |
| [术语表](glossary.md) | 中文阅读句柄与英文标识对照 |

## 阅读路径

| 你想做什么 | 从这里开始 |
| --- | --- |
| 快速理解项目在测什么 | 本页 → [端到端流程](walkthroughs/端到端流程.md) Step 1–3 |
| 跑 Gradio 演示 | [端到端流程](walkthroughs/端到端流程.md) Step 4 |
| 跑批量实验并看指标 | [端到端流程](walkthroughs/端到端流程.md) Step 5–7 → [批量测试](modules/批量测试.md) |
| 改越狱模板或系统提示 | [提示词层](modules/提示词层.md) → [提示词清单](references/提示词清单.md) |
| 换模型或接新 API | [模型层](modules/模型层.md) → [支持的模型](references/支持的模型.md) |
| 理解泄露/拒绝怎么判 | [检测层](modules/检测层.md) → [混淆矩阵定义](references/混淆矩阵定义.md) |

## 运行前准备

1. 安装依赖：`pip install -r requirements.txt`
2. 在仓库根目录准备 [`config.json`](../config.json)，填入 `api_key`（OpenAI）与 `huggingface_token`（HuggingFace Inference）。
3. 确认 [`data/database.json`](../data/database.json) 存在；系统提示会把整库注入 `{database}` 占位符。

> 安全提示：仓库中的 `config.json` 当前含明文密钥，提交前请轮换密钥并改用环境变量或本地忽略文件。文档不展开密钥内容。

## 变更记录

见 [change-log.md](change-log.md)。
