**Language:** English · [简体中文](../../zh-CN/modules/models.md) · [繁體中文（香港）](../../zh-HK/modules/models.md)

# Model layer

Evidence: unless noted, confirmed against current source.

## Plain-language model

The model layer is an adapter: send a message list to a remote LLM and stream tokens back. This repo does **not** load local weights. OpenAI models use the official Chat API; everything else uses Hugging Face Inference `chat.completions` (via `nebius` or `together`).

Callers pass an alias (e.g. `gemma-2-9b`) and `[{role, content}, ...]`. They do not need the upstream `model_id` or provider.

## Code model

Entry class: [`ModelManager`](../../../models/model_manager.py).

On init:

1. Read `api_key` and `huggingface_token` from `config.json`
2. Build an `OpenAI` client
3. Create an `InferenceClient` per Hugging Face provider

Core method `get_streaming_response(model_name, messages)`:

- Rejects aliases outside `SUPPORTED_MODELS`
- `type == "openai"`: wraps content as OpenAI multimodal text parts, `stream=True`, `temperature=0.7`
- `type == "huggingface"`: simplified messages, `stream=True`, `max_tokens=2000`; on error, yields an error string instead of raising

`StreamingCallbackHandler` exists but is not wired into the main LangChain path; it is left for extension.

Full alias table: [supported models](../references/models.md).

## Next

- Who assembles messages and history: [conversation layer](conversation.md)
- How batch tests pin model + prompt: [batch testing](batch-testing.md)
- Refusal detection also constructs `ModelManager` and calls `qwen-72b`: [detection](detection.md)
