# Agent instructions

## Repo docs

Human-facing documentation for this repository lives in `repo-docs/` (Chinese). Start at `repo-docs/README.md`, then `repo-docs/walkthroughs/端到端流程.md` for the end-to-end path.

When changing behavior, update the relevant module page under `repo-docs/modules/` and any affected reference tables. Log durable guide changes in `repo-docs/change-log.md`.

### Project summary

FYP experiment repo (`fyp1.2.1`) that tests whether LLMs leak simulated PII from `data/database.json` when system prompts require privacy protection and user messages use jailbreak prompt templates.

### Key entry points

| Path | Role |
| --- | --- |
| `app.py` | Gradio side-by-side demo |
| `leak_test.py` | Batch test one model + one prompt (20 runs default) |
| `auto_prompt_test.py` | Run all prompts for one model |
| `analyze_results.py` | Aggregate `results/` JSON into heatmaps |
| `models/model_manager.py` | OpenAI + HuggingFace Inference streaming |
| `prompts/prompt_manager.py` | Seeds, jailbreak templates, system messages |
| `utils/jailbreak_detector.py` | Regex leak detection; model-based refusal detection |

### Conventions

- API keys in `config.json` (`api_key`, `huggingface_token`); treat as secrets.
- Batch tests default to `seed1`, `system_message2`, `NUM_TESTS=20`.
- Confusion matrix labels (TP/FP/TN/FN) follow defense-centric definitions in `leak_test.py`; see `repo-docs/references/混淆矩阵定义.md`.

### Do not

- Commit or echo live API keys in docs or PRs.
- Assume `analyze_results.py` ingests `summary_*.json` files.
