**语言：** [English](../../en/modules/batch-testing.md) · 简体中文 · [繁體中文（香港）](../../zh-HK/modules/batch-testing.md)

# 批量测试

证据状态：除特别标注外，本页基于当前源码已确认。

## 白话模型

批量测试把「同一配置重复多次」变成可统计的防御评估。核心脚本是 `leak_test.py`：固定种子与系统提示，只变换模型和越狱模板，每次记录完整响应、泄露判定、拒绝判定，最后算混淆矩阵并写 JSON。

`auto_prompt_test.py` 在其外包一层循环，对单个模型跑遍全部 prompt 键。`analyze_results.py` 再跨文件聚合，画热力图。

## 代码模型

### leak_test.py

硬编码常量（文件顶部，改实验条件需编辑源码）：

| 常量 | 默认值 | 含义 |
| --- | --- | --- |
| `SEED_KEY` | `seed1` | 种子 |
| `SYSTEM_MESSAGE_KEY` | `system_message2` | 系统提示 |
| `NUM_TESTS` | `20` | 每配置重复次数 |
| `RESULTS_DIR` | `results` | 输出目录 |

`run_test` 循环内不做会话复用，每次直接构造两条消息的列表调用 `ModelManager`。

`analyze_results`（函数，非 `analyze_results.py`）计算矩阵、指标、绕过率、防御成功率，写出带 `metadata` 与 `detailed_results` 的 JSON。

### auto_prompt_test.py

`run_single_test` 用 `subprocess` 调用 `leak_test.py --auto`，从 stdout 解析结果文件路径并读回。全部完成后 `save_summary` 写 `summary_{model}_{timestamp}.json`。

### analyze_results.py

`ResultsAnalyzer` 扫描 `results/*.json`，用文件名启发式解析 `model_name` 与 `prompt_type`（对 `gemma-2-9b_prompt_target_hijacking1_...` 这类命名）。聚合后生成六张热力图与 `analysis_summary.json`。

未覆盖：`summary_*.json` 不参与 `analyze_results.py` 的文件名解析逻辑。

依赖：`pandas`、`matplotlib`、`numpy`（未写入 `requirements.txt`）。

## 接下去阅读

- 结果 JSON 字段：[结果文件格式](../references/result-format.md)
- 全流程步骤：[端到端流程](../walkthrough.md) Step 5–7
