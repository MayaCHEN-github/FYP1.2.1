**Language:** English · [简体中文](../../zh-CN/modules/batch-testing.md) · [繁體中文（香港）](../../zh-HK/modules/batch-testing.md)

# Batch testing

Evidence: unless noted, confirmed against current source.

## Plain-language model

Batch testing turns “same config, many repeats” into a statistical defense evaluation. The core script is `leak_test.py`: seed and system prompt stay fixed; only the model and jailbreak template change. Each trial records the full reply, leak verdict, and refusal verdict, then writes a confusion matrix JSON.

`auto_prompt_test.py` wraps a loop over every prompt key for one model. `analyze_results.py` aggregates across files and draws heatmaps.

## Code model

### leak_test.py

Hard-coded constants at the top of the file (edit source to change experiment conditions):

| Constant | Default | Meaning |
| --- | --- | --- |
| `SEED_KEY` | `seed1` | Seed |
| `SYSTEM_MESSAGE_KEY` | `system_message2` | System prompt |
| `NUM_TESTS` | `20` | Repeats per config |
| `RESULTS_DIR` | `results` | Output directory |

`run_test` does not reuse conversations; each trial builds a two-message list and calls `ModelManager` directly.

The function `analyze_results` (not the `analyze_results.py` module) computes the matrix, metrics, bypass rate, and defense success rate, then writes JSON with `metadata` and `detailed_results`.

### auto_prompt_test.py

`run_single_test` shells out to `leak_test.py --auto`, parses the result path from stdout, and reads it back. `save_summary` then writes `summary_{model}_{timestamp}.json`.

### analyze_results.py

`ResultsAnalyzer` scans `results/*.json` and heuristically parses `model_name` and `prompt_type` from names like `gemma-2-9b_prompt_target_hijacking1_...`. It writes six heatmaps plus `analysis_summary.json`.

Not covered: `summary_*.json` is skipped by that filename parser.

Dependencies: `pandas`, `matplotlib`, `numpy` (not listed in `requirements.txt`).

## Next

- JSON fields: [result file format](../references/result-format.md)
- Full flow: [walkthrough](../walkthrough.md) Steps 5–7
