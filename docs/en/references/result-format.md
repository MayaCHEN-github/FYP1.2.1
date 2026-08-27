**Language:** English · [简体中文](../../zh-CN/references/result-format.md) · [繁體中文（香港）](../../zh-HK/references/result-format.md)

# Result file format

## leak_test per-config file

Path: `results/{model}_{prompt_key}_{timestamp}.json`

### metadata

| Field | Type | Meaning |
| --- | --- | --- |
| `model` | string | Model alias |
| `prompt` | string | Prompt key |
| `seed` | string | Seed key |
| `system_message` | string | System-prompt key |
| `timestamp` | string | `YYYYMMDD_HHMMSS` |
| `total_tests` | int | Repeat count |
| `bypass_count` | int | TP |
| `defense_success_count` | int | TN |
| `defense_failure_count` | int | FP |
| `irrelevant_count` | int | FN |
| `bypass_rate` | float | Bypass rate |
| `defense_success_rate` | float | Defense success rate |
| `confusion_matrix` | object | `{TP, FP, TN, FN}` |
| `metrics` | object | `{Accuracy, Precision, Recall, F1 Score}` |

### detailed_results[]

| Field | Meaning |
| --- | --- |
| `test_number` | Repeat index (1-based) |
| `contains_leak` | Regex leak verdict |
| `contains_refusal` | Model refusal verdict |
| `leakage_details` | Leak-detector description |
| `refusal_details` | Refusal-detector description |
| `response` | Full model output |

## auto_prompt_test summary

Path: `results/summary_{model}_{timestamp}.json`

| Top-level key | Meaning |
| --- | --- |
| `metadata.model` | Model under test |
| `metadata.timestamp` | Summary time |
| `prompt_stats` | Per-prompt snapshots of metadata / confusion_matrix / metrics |
| `detailed_results` | Full `leak_test` payloads |

`analyze_results.py` does **not** read these summary files.

## analyze_results output

Path: `analysis_results/analysis_summary.json`

| Top-level key | Meaning |
| --- | --- |
| `model_analysis` | model → prompt → aggregated counts |
| `prompt_analysis` | prompt → model → aggregated counts |

Heatmap PNGs in the same directory (current `analyze_results.py`):

- `tp_count_heatmap.png`
- `tn_count_heatmap.png`
- `fp_count_heatmap.png`
- `fn_count_heatmap.png`
- `leak_count_heatmap.png`
- `rejection_count_heatmap.png`

`analyze_results.py` parses model and prompt type from the **file name**. Keep `{model}_prompt_{type}{n}_{timestamp}.json` or `{model}_prompt{n}_{timestamp}.json`, or the file is skipped.
