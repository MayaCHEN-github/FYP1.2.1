**Language:** English · [简体中文](../zh-CN/index.md) · [繁體中文（香港）](../zh-HK/index.md)

# fyp1.2.1 project guide

This is a final-year project (FYP) experiment repo. It evaluates whether large language models leak simulated personal records from [`data/database.json`](../../data/database.json) when the system prompt says “protect this privacy database” and the user message is a jailbreak template.

There are two usage paths: a Gradio UI that compares two models on one prompt, and CLI scripts that repeat the experiment, compute a confusion matrix, and draw heatmaps.

For a shorter install/command overview see the root [README.md](../../README.md).

## Doc map

| Page | Purpose |
| --- | --- |
| [End-to-end walkthrough](walkthrough.md) | Full path from config to analysis |
| [Model layer](modules/models.md) | OpenAI and Hugging Face inference |
| [Prompt layer](modules/prompts.md) | Seeds, jailbreak templates, system messages |
| [Conversation layer](modules/conversation.md) | Chat history and streaming |
| [Detection layer](modules/detection.md) | Leak detection and refusal detection |
| [Batch testing](modules/batch-testing.md) | `leak_test.py` and result analysis |
| [Supported models](references/models.md) | Alias → backend mapping |
| [Prompt catalog](references/prompts.md) | Every prompt key and type |
| [Confusion-matrix definition](references/confusion-matrix.md) | What TP/FP/TN/FN mean here |
| [Result file format](references/result-format.md) | Fields in `results/` and `analysis_results/` |
| [Glossary](glossary.md) | English identifiers ↔ Chinese reading handles |

## Reading paths

| If you want to… | Start here |
| --- | --- |
| Understand what is being measured | This page → [walkthrough](walkthrough.md) Steps 1–3 |
| Run the Gradio demo | [walkthrough](walkthrough.md) Step 4 |
| Run batch experiments and read metrics | [walkthrough](walkthrough.md) Steps 5–7 → [batch testing](modules/batch-testing.md) |
| Change templates or system prompts | [prompt layer](modules/prompts.md) → [prompt catalog](references/prompts.md) |
| Swap models or wire a new API | [model layer](modules/models.md) → [supported models](references/models.md) |
| Understand leak / refusal decisions | [detection](modules/detection.md) → [confusion matrix](references/confusion-matrix.md) |

## Before you run

1. Install dependencies: `pip install -r requirements.txt`
2. Copy [`config.example.json`](../../config.example.json) to `config.json` at the repo root and fill in `api_key` (OpenAI) and `huggingface_token` (Hugging Face Inference).
3. Confirm [`data/database.json`](../../data/database.json) exists; system prompts inject the whole store into `{database}`.

> [!WARNING]
> Do not commit a `config.json` that contains live keys. These docs never print secret values.

For heatmaps, also install: `pip install pandas matplotlib numpy`.

## Changelog

See [changelog.md](changelog.md).
