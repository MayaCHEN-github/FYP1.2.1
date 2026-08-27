**語言：** [English](../../en/modules/batch-testing.md) · [簡體中文](../../zh-CN/modules/batch-testing.md) · 繁體中文（香港）

# 批量測試

證據狀態：除特別標註外，本頁基於當前源碼已確認。

## 白話模型

批量測試把「同一配置重複多次」變成可統計的防禦評估。核心腳本是 `leak_test.py`：固定種子與系統提示，只變換模型和越獄模板，每次記錄完整響應、洩露判定、拒絕判定，最後算混淆矩陣並寫 JSON。

`auto_prompt_test.py` 在其外包一層循環，對單個模型跑遍全部 prompt 鍵。`analyze_results.py` 再跨檔案聚合，畫熱力圖。

## 代碼模型

### leak_test.py

硬編碼常量（檔案頂部，改實驗條件需編輯源碼）：

| 常量 | 預設值 | 含義 |
| --- | --- | --- |
| `SEED_KEY` | `seed1` | 種子 |
| `SYSTEM_MESSAGE_KEY` | `system_message2` | 系統提示 |
| `NUM_TESTS` | `20` | 每配置重複次數 |
| `RESULTS_DIR` | `results` | 輸出目錄 |

`run_test` 循環內不做會話複用，每次直接構造兩條消息的列表調用 `ModelManager`。

`analyze_results`（函數，非 `analyze_results.py`）計算矩陣、指標、繞過率、防禦成功率，寫出帶 `metadata` 與 `detailed_results` 的 JSON。

### auto_prompt_test.py

`run_single_test` 用 `subprocess` 調用 `leak_test.py --auto`，從 stdout 解析結果檔案路徑並讀回。全部完成後 `save_summary` 寫 `summary_{model}_{timestamp}.json`。

### analyze_results.py

`ResultsAnalyzer` 掃描 `results/*.json`，用檔案名啓發式解析 `model_name` 與 `prompt_type`（對 `gemma-2-9b_prompt_target_hijacking1_...` 這類命名）。聚合後生成六張熱力圖與 `analysis_summary.json`。

未覆蓋：`summary_*.json` 不參與 `analyze_results.py` 的檔案名解析邏輯。

依賴：`pandas`、`matplotlib`、`numpy`（未寫入 `requirements.txt`）。

## 接下去閲讀

- 結果 JSON 字段：[結果檔案格式](../references/result-format.md)
- 全流程步驟：[端到端流程](../walkthrough.md) Step 5–7
