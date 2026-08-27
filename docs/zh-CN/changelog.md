**语言：** [English](../en/changelog.md) · 简体中文 · [繁體中文（香港）](../zh-HK/changelog.md)

# 变更记录

## 2026-08-27

- 审阅 `cursor/repo-docs-zh-44da` 上的中文 `repo-docs/`，合并进 `docs/`。
- 文档改为三语：English、简体中文、繁體中文（香港）；文件名改为英文，按语言分目录。
- 根目录 README 同步提供三个语言版本，并链接到本目录导读。
- 密钥示例改为 [`config.example.json`](../../config.example.json)，不再引导提交 `config.json`。
- 补上原先未覆盖的 `prompt_composer.py` / `run_example.py`，并写明 `summary_*.json` 不被 `analyze_results.py` 解析。
- 热力图文件名与当前 `analyze_results.py` 对齐：`leak_count_heatmap.png`、`rejection_count_heatmap.png`。

## 2026-07-01

- 首次建立 `repo-docs/` 中文导读（现已迁入 `docs/zh-CN/`）。
- 覆盖模块：模型层、提示词层、会话层、检测层、批量测试。
- 覆盖参考：支持的模型、提示词清单、混淆矩阵、结果文件格式。
- 新增根目录 `AGENTS.md`（英文 agent 指令块）。

仍未单独成页（仅在相关模块中提及）：

- 仓库内已有 `results/` 历史数据与 `analysis_results/` 图表的解读范例
- 单元测试与 CI（仓库当前无测试目录）
