**語言：** [English](../../en/modules/conversation.md) · [簡體中文](../../zh-CN/modules/conversation.md) · 繁體中文（香港）

# 會話層

證據狀態：除特別標註外，本頁基於當前源碼已確認。

## 白話模型

會話層維護「某個模型 + 某條系統提示」下的消息歷史，並在每次用戶輸入後把完整歷史交給模型層流式生成回覆。Gradio 演示裏會為兩個模型各開一條獨立會話，因此同一條攻擊提示會並行得到兩份回答。

會話 ID 由模型名、系統提示鍵和序號拼接，格式形如 `gpt-4_system_message0_0`。

## 代碼模型

入口類：[`ConversationManager`](../../../chains/conversation_chain.py)。

| 方法 | 行為 |
| --- | --- |
| `initialize_conversation(model_name, system_message_key)` | 創建 ID，歷史首條為 system 消息 |
| `get_streaming_response(conversation_id, user_input)` | 追加 user 消息 → 調 `ModelManager.get_streaming_response` → 流式 yield token → 結束後追加 assistant 完整文本 |
| `get_conversation_history(conversation_id)` | 跳過 system，把 user/assistant 轉成 `(user, assistant)` 元組列表 |

注意：`get_streaming_response` 從 `conversation_id` 用 `split('_')[0]` 取模型名。當前別名使用連字符（如 `gemma-2-9b`），因此可以工作；**不要在新別名裏使用下劃線**，否則會截斷模型名。

[`app.py`](../../../app.py) 的 `generate_responses` 不經過多輪對話，僅單輪 user → assistant；歷史結構仍按 Chat 格式保留，便於擴展。

## 接下去閲讀

- 模型調用細節：[模型層](models.md)
- 演示介面如何 zip 兩個生成器：[端到端流程](../walkthrough.md) Step 4
