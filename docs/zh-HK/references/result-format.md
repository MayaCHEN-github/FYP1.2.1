**語言：** [English](../../en/references/result-format.md) · [簡體中文](../../zh-CN/references/result-format.md) · 繁體中文（香港）

# 結果檔案格式

## leak_test 單次結果

路徑：`results/{model}_{prompt_key}_{timestamp}.json`

### metadata

| 字段 | 類型 | 含義 |
| --- | --- | --- |
| `model` | string | 模型別名 |
| `prompt` | string | prompt 鍵名 |
| `seed` | string | 種子鍵名 |
| `system_message` | string | 系統提示鍵名 |
| `timestamp` | string | `YYYYMMDD_HHMMSS` |
| `total_tests` | int | 重複次數 |
| `bypass_count` | int | TP |
| `defense_success_count` | int | TN |
| `defense_failure_count` | int | FP |
| `irrelevant_count` | int | FN |
| `bypass_rate` | float | 繞過率 |
| `defense_success_rate` | float | 防禦成功率 |
| `confusion_matrix` | object | `{TP, FP, TN, FN}` |
| `metrics` | object | `{Accuracy, Precision, Recall, F1 Score}` |

### detailed_results[]

| 字段 | 含義 |
| --- | --- |
| `test_number` | 第幾次重複（1-based） |
| `contains_leak` | 正則洩露檢測 |
| `contains_refusal` | 模型拒絕檢測 |
| `leakage_details` | 洩露檢測描述文本 |
| `refusal_details` | 拒絕檢測描述文本 |
| `response` | 模型完整輸出 |

## auto_prompt_test 彙總

路徑：`results/summary_{model}_{timestamp}.json`

| 頂層鍵 | 含義 |
| --- | --- |
| `metadata.model` | 被測模型 |
| `metadata.timestamp` | 彙總時間 |
| `prompt_stats` | 每個 prompt 的 metadata / confusion_matrix / metrics 快照 |
| `detailed_results` | 各次 `leak_test` 完整結果列表 |

`analyze_results.py` **不會**讀取這類彙總檔案。

## analyze_results 輸出

路徑：`analysis_results/analysis_summary.json`

| 頂層鍵 | 含義 |
| --- | --- |
| `model_analysis` | 按模型 → prompt → 聚合計數 |
| `prompt_analysis` | 按 prompt → 模型 → 聚合計數 |

熱力圖 PNG（同目錄，由當前 `analyze_results.py` 寫出）：

- `tp_count_heatmap.png`
- `tn_count_heatmap.png`
- `fp_count_heatmap.png`
- `fn_count_heatmap.png`
- `leak_count_heatmap.png`
- `rejection_count_heatmap.png`

`analyze_results.py` 從**檔案名**解析模型與 prompt 類型；命名需保持 `{model}_prompt_{type}{n}_{timestamp}.json` 或 `{model}_prompt{n}_{timestamp}.json` 風格，否則該檔案會被跳過。
