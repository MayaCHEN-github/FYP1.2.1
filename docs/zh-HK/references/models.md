**語言：** [English](../../en/references/models.md) · [簡體中文](../../zh-CN/references/models.md) · 繁體中文（香港）

# 支持的模型

查表用；機制説明見 [模型層](../modules/models.md)。

| 別名 | 後端類型 | provider | model_id |
| --- | --- | --- | --- |
| `gpt-3.5-turbo` | openai | — | `gpt-3.5-turbo` |
| `gpt-4` | openai | — | `gpt-4` |
| `qwen-72b` | huggingface | nebius | `Qwen/Qwen2.5-72B-Instruct` |
| `qwen-32b` | huggingface | nebius | `Qwen/Qwen2.5-32B-Instruct` |
| `qwen-7b` | huggingface | together | `Qwen/Qwen2.5-7B-Instruct` |
| `llama-3.3-70b` | huggingface | nebius | `meta-llama/Llama-3.3-70B-Instruct` |
| `llama-3.1-8b` | huggingface | nebius | `meta-llama/Llama-3.1-8B-Instruct` |
| `llama-3.1-70b` | huggingface | nebius | `meta-llama/Llama-3.1-70B-Instruct` |
| `gemma-3-27b` | huggingface | nebius | `google/gemma-3-27b-it` |
| `gemma-2-27b` | huggingface | nebius | `google/gemma-2-27b-it` |
| `gemma-2-9b` | huggingface | nebius | `google/gemma-2-9b-it` |

定義位置：[`models/model_manager.py`](../../../models/model_manager.py) 的 `SUPPORTED_MODELS`。

密鑰：`openai` 類型用 `config.json` 的 `api_key`；`huggingface` 類型用 `huggingface_token`。模板見 [`config.example.json`](../../../config.example.json)。
