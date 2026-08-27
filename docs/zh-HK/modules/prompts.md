**語言：** [English](../../en/modules/prompts.md) · [簡體中文](../../zh-CN/modules/prompts.md) · 繁體中文（香港）

# 提示詞層

證據狀態：除特別標註外，本頁基於當前源碼已確認。

## 白話模型

提示詞層管理三類文本素材，並在發送前拼成模型真正看到的對話：

1. **系統提示（system message）**：定義模型角色；多數版本把整份 `database.json` 注入 `{database}` 佔位符，讓模型「知道庫裏有什麼」。
2. **種子（seed）**：表面用戶任務，預設是「列出所有人隱私字段」。
3. **越獄模板（prompt）**：在種子外包一層攻擊話術（目標劫持、拒絕壓制、角色扮演、代碼補全等），模板內用 `{seed}` 佔位。

`generate_full_prompt(seed_key, prompt_key)` 的輸出作為 user 消息；`get_system_message(key)` 的輸出作為 system 消息。

## 代碼模型

入口類：[`PromptManager`](../../../prompts/prompt_manager.py)。

| 素材 | 來源檔案 | 訪問方法 |
| --- | --- | --- |
| 系統提示 | [`system_messages.json`](../../../prompts/prompt_files/system_messages.json) | `get_system_message` |
| 種子 | [`seeds.json`](../../../prompts/prompt_files/seeds.json) | `get_seed` |
| 越獄模板 | [`prompts.py`](../../../prompts/prompt_files/prompts.py) | `get_prompt` / `generate_full_prompt` |

`PromptType` 枚舉標記模板類別（`target_hijacking`、`refusal_suppression`、`code_injection` 等）。`combine_prompts` 可按類型合併多個模板，但主流程多用單鍵選取。

`load_database` 在初始化時把 [`data/database.json`](../../../data/database.json) 讀入 `self.database`，供系統提示格式化。

輔助腳本（非運行時必需）：

- [`prompt_composer.py`](../../../prompts/prompt_files/prompt_composer.py) + [`run_example.py`](../../../run_example.py)：組合示例入口
- [`prompt_combined.py`](../../../prompts/prompt_files/prompt_combined.py) / [`target_hijacking_prompts.py`](../../../prompts/prompt_files/target_hijacking_prompts.py)：兩兩組合模板
- [`generate_combined.py`](../../../prompts/generate_combined.py)：給組合表寫入 `component1` / `component2` 元資料

## 接下去閲讀

- 19 個模板鍵名與類型：[提示詞清單](../references/prompts.md)
- 會話如何把 system + user 送進模型：[會話層](conversation.md)
- 端到端拼裝順序：[端到端流程](../walkthrough.md) Step 2
