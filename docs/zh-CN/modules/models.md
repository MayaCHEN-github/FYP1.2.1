**语言：** [English](../../en/modules/models.md) · 简体中文 · [繁體中文（香港）](../../zh-HK/modules/models.md)

# 模型层

证据状态：除特别标注外，本页基于当前源码已确认。

## 白话模型

模型层是「把消息列表发给远端大模型，按 token 流式取回文本」的适配器。仓库不本地加载权重：OpenAI 模型走官方 Chat API，其余走 Hugging Face Inference 的 `chat.completions` 接口（经 `nebius` 或 `together` 等 provider）。

调用方只需传别名（如 `gemma-2-9b`）和 `[{role, content}, ...]` 消息列表，不必关心底层 `model_id` 或 provider。

## 代码模型

入口类：[`ModelManager`](../../../models/model_manager.py)。

初始化时：

1. 从 `config.json` 读取 `api_key`、`huggingface_token`
2. 构造 `OpenAI` 客户端
3. 为每个 Hugging Face provider 创建 `InferenceClient`

核心方法 `get_streaming_response(model_name, messages)`：

- 校验 `model_name` 在 `SUPPORTED_MODELS` 内
- `type == "openai"`：将 content 包成 OpenAI 多模态文本块格式，`stream=True`，`temperature=0.7`
- `type == "huggingface"`：简化消息格式后 `stream=True`，`max_tokens=2000`；异常时 yield 错误字符串而非抛栈

流式回调类 `StreamingCallbackHandler` 已定义，但当前主路径未接入 LangChain 链，仅保留供扩展。

完整别名表见 [支持的模型](../references/models.md)。

## 接下去阅读

- 谁组装消息并维护历史：[会话层](conversation.md)
- 批量测试如何固定模型与 prompt：[批量测试](batch-testing.md)
- 拒绝检测器内部也实例化 `ModelManager` 调用 `qwen-72b`：[检测层](detection.md)
