**Language:** English · [简体中文](../../zh-CN/modules/conversation.md) · [繁體中文（香港）](../../zh-HK/modules/conversation.md)

# Conversation layer

Evidence: unless noted, confirmed against current source.

## Plain-language model

This layer keeps message history for “one model + one system prompt” and, on each user turn, sends the full history to the model layer for a streamed reply. The Gradio demo opens an independent session per model, so one attack prompt yields two answers in parallel.

Session IDs concatenate model name, system-prompt key, and a counter, e.g. `gpt-4_system_message0_0`.

## Code model

Entry class: [`ConversationManager`](../../../chains/conversation_chain.py).

| Method | Behavior |
| --- | --- |
| `initialize_conversation(model_name, system_message_key)` | Creates the ID; first history item is the system message |
| `get_streaming_response(conversation_id, user_input)` | Append user → call `ModelManager.get_streaming_response` → yield tokens → append full assistant text |
| `get_conversation_history(conversation_id)` | Skip system; convert user/assistant pairs to `(user, assistant)` tuples |

Note: `get_streaming_response` takes the model name with `conversation_id.split('_')[0]`. Current aliases use hyphens (`gemma-2-9b`), so this works. **Do not put underscores in new aliases** or the name will be truncated.

[`app.py`](../../../app.py) `generate_responses` is single-turn (user → assistant) only; the Chat-shaped history is kept for later multi-turn use.

## Next

- Call details: [model layer](models.md)
- How the UI zips two generators: [walkthrough](../walkthrough.md) Step 4
