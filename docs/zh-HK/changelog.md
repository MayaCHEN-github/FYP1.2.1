**語言：** [English](../en/changelog.md) · [簡體中文](../zh-CN/changelog.md) · 繁體中文（香港）

# 變更記錄

## 2026-08-27

- 審閲 `cursor/repo-docs-zh-44da` 上的中文 `repo-docs/`，合併進 `docs/`。
- 文檔改為三語：English、簡體中文、繁體中文（香港）；檔案名改為英文，按語言分目錄。
- 根目錄 README 同步提供三個語言版本，並鏈接到本目錄導讀。
- 密鑰示例改為 [`config.example.json`](../../config.example.json)，不再引導提交 `config.json`。
- 補上原先未覆蓋的 `prompt_composer.py` / `run_example.py`，並寫明 `summary_*.json` 不被 `analyze_results.py` 解析。
- 熱力圖檔案名與當前 `analyze_results.py` 對齊：`leak_count_heatmap.png`、`rejection_count_heatmap.png`。

## 2026-07-01

- 首次建立 `repo-docs/` 中文導讀（現已遷入 `docs/zh-CN/`）。
- 覆蓋模塊：模型層、提示詞層、會話層、檢測層、批量測試。
- 覆蓋參考：支持的模型、提示詞清單、混淆矩陣、結果檔案格式。
- 新增根目錄 `AGENTS.md`（英文 agent 指令塊）。

仍未單獨成頁（僅在相關模塊中提及）：

- 倉庫內已有 `results/` 歷史資料與 `analysis_results/` 圖表的解讀範例
- 單元測試與 CI（倉庫當前無測試目錄）
