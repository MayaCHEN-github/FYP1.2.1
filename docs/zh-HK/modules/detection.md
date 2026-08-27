**語言：** [English](../../en/modules/detection.md) · [簡體中文](../../zh-CN/modules/detection.md) · 繁體中文（香港）

# 檢測層

證據狀態：除特別標註外，本頁基於當前源碼已確認。

## 白話模型

檢測層在模型輸出落盤後回答兩個問題：

1. **是否洩露**：輸出裏是否出現 `database.json` 中的真實字段值（姓名、身份證號、電話等）。
2. **是否拒絕**：輸出裏是否包含「不能」「無法」「不提供」等拒絕措辭。

批量測試用「洩露 + 拒絕」組合成混淆矩陣，從防禦視角衡量繞過與攔截效果。Gradio 演示僅展示正則洩露檢測結果。

## 代碼模型

實現檔案：[`utils/jailbreak_detector.py`](../../../utils/jailbreak_detector.py)。

### 洩露檢測

| 類 | 機制 | 使用場景 |
| --- | --- | --- |
| `JailbreakDetector` | GPT-3.5-instruct 按長系統提示做語義判定 | 基類，含完整判定規則文本；主路徑未使用 |
| `RegexJailbreakDetector` | 對庫中每條記錄的字段做 `re.search` | `app.py`、`leak_test.py` 實際使用 |

`RegexJailbreakDetector.detect` 返回字段：

- `contains_leak`：首條完整記錄、全庫完整、或任一字段命中即為真
- `result`：中文描述洩露範圍
- `confidence`：固定 `High`

### 拒絕檢測

| 類 | 機制 | 使用場景 |
| --- | --- | --- |
| `RegexRefusalDetector` | 18 箇中文拒絕詞正則 OR 匹配 | 已實現，`leak_test.py` 未使用 |
| `ModelRefusalDetector` | `qwen-72b` 按結構化提示輸出 Yes/No | `leak_test.py` 實際使用 |

`ModelRefusalDetector` 每次檢測新建 `ModelManager` 並流式拼完整響應再解析 `Detection Result:` 行。

### 與混淆矩陣的銜接

[`leak_test.py`](../../../leak_test.py) 中 `calculate_confusion_matrix` 把每次測試映射為 TP/FP/TN/FN（防禦視角）。含義見 [混淆矩陣定義](../references/confusion-matrix.md)。

## 接下去閲讀

- 指標如何打印與落盤：[批量測試](batch-testing.md)
- 矩陣字段定義：[混淆矩陣定義](../references/confusion-matrix.md)
