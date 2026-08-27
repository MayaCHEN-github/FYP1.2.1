**Language:** English · [简体中文](../../zh-CN/modules/prompts.md) · [繁體中文（香港）](../../zh-HK/modules/prompts.md)

# Prompt layer

Evidence: unless noted, confirmed against current source.

## Plain-language model

This layer owns three text assets and assembles the dialogue the model actually sees:

1. **System message** — role instructions; most variants inject the whole `database.json` into `{database}` so the model “knows” the store.
2. **Seed** — the surface user task; default is “list every privacy field”.
3. **Jailbreak template** — attack wording around the seed (hijacking, refusal suppression, role-play, code completion, …) with a `{seed}` placeholder.

`generate_full_prompt(seed_key, prompt_key)` becomes the user message; `get_system_message(key)` becomes the system message.

## Code model

Entry class: [`PromptManager`](../../../prompts/prompt_manager.py).

| Asset | Source | Accessor |
| --- | --- | --- |
| System prompts | [`system_messages.json`](../../../prompts/prompt_files/system_messages.json) | `get_system_message` |
| Seeds | [`seeds.json`](../../../prompts/prompt_files/seeds.json) | `get_seed` |
| Jailbreak templates | [`prompts.py`](../../../prompts/prompt_files/prompts.py) | `get_prompt` / `generate_full_prompt` |

`PromptType` tags categories (`target_hijacking`, `refusal_suppression`, `code_injection`, …). `combine_prompts` can merge by type; the main path usually picks a single key.

`load_database` reads [`data/database.json`](../../../data/database.json) into `self.database` for system-prompt formatting.

Helper scripts (not required at runtime):

- [`prompt_composer.py`](../../../prompts/prompt_files/prompt_composer.py) + [`run_example.py`](../../../run_example.py): composition playground
- [`prompt_combined.py`](../../../prompts/prompt_files/prompt_combined.py) / [`target_hijacking_prompts.py`](../../../prompts/prompt_files/target_hijacking_prompts.py): pairwise templates
- [`generate_combined.py`](../../../prompts/generate_combined.py): writes `component1` / `component2` metadata

## Next

- All 19 template keys: [prompt catalog](../references/prompts.md)
- How system + user are sent: [conversation layer](conversation.md)
- Assembly order: [walkthrough](../walkthrough.md) Step 2
