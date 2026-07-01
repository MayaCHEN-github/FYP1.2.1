# 变更记录

## 2026-07-01

- 首次建立 `repo-docs/` 中文导读。
- 覆盖模块：模型层、提示词层、会话层、检测层、批量测试。
- 覆盖参考：支持的模型、提示词清单、混淆矩阵、结果文件格式。
- 新增根目录 `AGENTS.md`（英文 agent 指令块）。

未覆盖区域（待后续补页）：

- `prompts/prompt_files/prompt_composer.py` 与组合 prompt 生成流程
- `run_example.py` / `prompts/prompt_files/example.py` 示例入口
- `RegexRefusalDetector` 与 `JailbreakDetector`（LLM 版）的对比实验路径
- 仓库内已有 `results/` 历史数据与 `analysis_results/` 图表的解读范例
- 单元测试与 CI（仓库当前无测试目录）

校验：手工核对文档链接与源码路径；未运行外部 `repo-docs` validator（环境中无基线技能包）。
