**語言：** [English](../../en/modules/models.md) · [簡體中文](../../zh-CN/modules/models.md) · 繁體中文（香港）

# 模型層

證據狀態：除特別標註外，本頁基於當前源碼已確認。

## 白話模型

模型層是「把消息列表發給遠端大模型，按 token 流式取回文本」的適配器。倉庫不本地加載權重：OpenAI 模型走官方 Chat API，其餘走 Hugging Face Inference 的 `chat.completions` 接口（經 `nebius` 或 `together` 等 provider）。

調用方只需傳別名（如 `gemma-2-9b`）和 `[{role, content}, ...]` 消息列表，不必關心底層 `model_id` 或 provider。

## 代碼模型

入口類：[`ModelManager`](../../../models/model_manager.py)。

初始化時：

1. 從 `config.json` 讀取 `api_key`、`huggingface_token`
2. 構造 `OpenAI` 客户端
3. 為每個 Hugging Face provider 創建 `InferenceClient`

核心方法 `get_streaming_response(model_name, messages)`：

- 校驗 `model_name` 在 `SUPPORTED_MODELS` 內
- `type == "openai"`：將 content 包成 OpenAI 多模態文本塊格式，`stream=True`，`temperature=0.7`
- `type == "huggingface"`：簡化消息格式後 `stream=True`，`max_tokens=2000`；異常時 yield 錯誤字符串而非拋棧

流式回調類 `StreamingCallbackHandler` 已定義，但當前主路徑未接入 LangChain 鏈，僅保留供擴展。

完整別名表見 [支持的模型](../references/models.md)。

## 接下去閲讀

- 誰組裝消息並維護歷史：[會話層](conversation.md)
- 批量測試如何固定模型與 prompt：[批量測試](batch-testing.md)
- 拒絕檢測器內部也實例化 `ModelManager` 調用 `qwen-72b`：[檢測層](detection.md)
