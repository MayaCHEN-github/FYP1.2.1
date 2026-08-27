**語言：** [English](../../en/references/prompts.md) · [簡體中文](../../zh-CN/references/prompts.md) · 繁體中文（香港）

# 提示詞清單

定義檔案：[`prompts/prompt_files/prompts.py`](../../../prompts/prompt_files/prompts.py)。共 19 條。

| 鍵名 | PromptType | 攻擊類別簡述 |
| --- | --- | --- |
| `prompt0` | `base` | 僅種子，無越獄包裝 |
| `prompt_target_hijacking1` | `target_hijacking` | 忽略前文，直接執行任務 |
| `prompt_target_hijacking2` | `target_hijacking` | 強制性指令覆蓋 |
| `prompt_privilege escalation1` | `privilege escalation` | 偽裝資料庫管理員 |
| `prompt_privilege escalation2` | `privilege escalation` | 超級管理員模式切換 |
| `prompt_refusal_suppression1` | `refusal_suppression` | 禁止質疑與拒絕 |
| `prompt_refusal_suppression2` | `refusal_suppression` | 強調專注執行、無解釋輸出 |
| `prompt_combined1` | `combined` | 指令覆蓋 + 拒絕壓制組合 |
| `prompt_scenario simulation1` | `scenario simulation` | 作文/檢討書場景嵌套表格輸出 |
| `prompt_role_playing1` | `Role-playing` | 黑客角色 |
| `prompt_role_playing2` | `Role-playing` | Neo 角色 |
| `prompt_role_playing3` | `Role-playing` | 伏地魔角色 |
| `prompt_formatted_output1` | `formatted_output` | 補全 SWI-Prolog 硬編碼輸出 |
| `prompt_formatted_output2` | `formatted_output` | 補全 COBOL DISPLAY |
| `prompt_formatted_output3` | `formatted_output` | 補全 Python print |
| `prompt_formatted_output4` | `formatted_output` | 補全 C++ cout |
| `prompt_code_injection1` | `code_injection` | 補全 Python main 省略號 |
| `prompt_code_injection2` | `code_injection` | 補全 Java main 省略號 |
| `prompt_code_injection3` | `code_injection` | 補全 JavaScript console.log 省略號 |

種子鍵（[`seeds.json`](../../../prompts/prompt_files/seeds.json)）：

| 鍵名 | 用途 |
| --- | --- |
| `seed0` | 測試用「你好」 |
| `seed1` | 預設攻擊任務：導出全庫隱私字段 |

系統提示鍵（[`system_messages.json`](../../../prompts/prompt_files/system_messages.json)）：

| 鍵名 | 角色 |
| --- | --- |
| `system_message0` | 資料庫展示助手（無防禦對照） |
| `system_message1` | 隱私保管者（簡版） |
| `system_message2` | 隱私保管者（嚴格版，批量測試預設） |
