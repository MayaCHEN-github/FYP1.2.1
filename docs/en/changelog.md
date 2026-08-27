**Language:** English · [简体中文](../zh-CN/changelog.md) · [繁體中文（香港）](../zh-HK/changelog.md)

# Changelog

## 2026-08-27

- Reviewed the Chinese `repo-docs/` from `cursor/repo-docs-zh-44da` and merged it into `docs/`.
- Documentation is now three locales: English, Simplified Chinese, and Hong Kong Traditional Chinese. Filenames are English; locales live in separate folders.
- Root README exists in the same three locales and links here.
- Key setup now points at [`config.example.json`](../../config.example.json) instead of committing `config.json`.
- Added the previously missing `prompt_composer.py` / `run_example.py` coverage, and documented that `summary_*.json` is not parsed by `analyze_results.py`.
- Heatmap filenames match current `analyze_results.py`: `leak_count_heatmap.png`, `rejection_count_heatmap.png`.

## 2026-07-01

- First Chinese guide under `repo-docs/` (now `docs/zh-CN/`).
- Modules: models, prompts, conversation, detection, batch testing.
- References: supported models, prompt catalog, confusion matrix, result format.
- Added root `AGENTS.md`.

Still not a standalone page (only mentioned in related modules):

- Worked examples interpreting the historical `results/` JSON and `analysis_results/` charts
- Unit tests and CI (the repo has no test directory)
