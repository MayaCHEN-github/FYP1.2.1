**Language:** English · [简体中文](../../zh-CN/references/models.md) · [繁體中文（香港）](../../zh-HK/references/models.md)

# Supported models

Lookup table. Mechanism: [model layer](../modules/models.md).

| Alias | Backend | provider | model_id |
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

Defined in [`models/model_manager.py`](../../../models/model_manager.py) as `SUPPORTED_MODELS`.

Keys: `openai` uses `config.json` `api_key`; `huggingface` uses `huggingface_token`. Template: [`config.example.json`](../../../config.example.json).
