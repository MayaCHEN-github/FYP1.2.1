**語言：** [English](../en/index.md) · [簡體中文](../zh-CN/index.md) · 繁體中文（香港）

# fyp1.2.1 項目導讀

這是一個畢業設計（FYP）實驗倉庫，用來評估大語言模型在「系統提示要求保護隱私資料庫」時，是否會被各類越獄提示（jailbreak prompt）誘導洩露 [`data/database.json`](../../data/database.json) 中的模擬個人資訊。

項目有兩條使用路徑：用 Gradio 介面並排對比兩個模型的單次響應；用命令列腳本批量重複實驗、彙總混淆矩陣並生成熱力圖。

更短的安裝與命令一覽見根目錄 [README.zh-HK.md](../../README.zh-HK.md)。

## 文檔地圖

| 文檔 | 用途 |
| --- | --- |
| [端到端流程](walkthrough.md) | 從配置到結果分析的完整路徑 |
| [模型層](modules/models.md) | 如何調用 OpenAI 與 Hugging Face 推理 |
| [提示詞層](modules/prompts.md) | 種子、越獄模板、系統提示的組裝 |
| [會話層](modules/conversation.md) | 對話歷史與流式輸出 |
| [檢測層](modules/detection.md) | 洩露檢測與拒絕檢測 |
| [批量測試](modules/batch-testing.md) | `leak_test.py` 與結果分析 |
| [支持的模型](references/models.md) | 模型別名與後端映射 |
| [提示詞清單](references/prompts.md) | 全部 prompt 鍵名與類型 |
| [混淆矩陣定義](references/confusion-matrix.md) | TP/FP/TN/FN 在本項目中的含義 |
| [結果檔案格式](references/result-format.md) | `results/` 與 `analysis_results/` 字段 |
| [術語表](glossary.md) | 中文閲讀句柄與英文標識對照 |

## 閲讀路徑

| 你想做什麼 | 從這裏開始 |
| --- | --- |
| 快速理解項目在測什麼 | 本頁 → [端到端流程](walkthrough.md) Step 1–3 |
| 跑 Gradio 演示 | [端到端流程](walkthrough.md) Step 4 |
| 跑批量實驗並看指標 | [端到端流程](walkthrough.md) Step 5–7 → [批量測試](modules/batch-testing.md) |
| 改越獄模板或系統提示 | [提示詞層](modules/prompts.md) → [提示詞清單](references/prompts.md) |
| 換模型或接新 API | [模型層](modules/models.md) → [支持的模型](references/models.md) |
| 理解洩露/拒絕怎麼判 | [檢測層](modules/detection.md) → [混淆矩陣定義](references/confusion-matrix.md) |

## 運行前準備

1. 安裝依賴：`pip install -r requirements.txt`
2. 複製 [`config.example.json`](../../config.example.json) 為倉庫根目錄的 `config.json`，填入 `api_key`（OpenAI）與 `huggingface_token`（Hugging Face Inference）。
3. 確認 [`data/database.json`](../../data/database.json) 存在；系統提示會把整庫注入 `{database}` 佔位符。

> [!WARNING]
> 不要把含真實密鑰的 `config.json` 提交進 git。文檔不展開密鑰內容。

畫熱力圖前額外安裝：`pip install pandas matplotlib numpy`。

## 變更記錄

見 [changelog.md](changelog.md)。
