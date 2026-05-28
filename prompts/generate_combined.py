from prompts.prompt_files.prompt_combined import prompts
import json

# 统计prompt数量
total_prompts = len(prompts)
print(f"总共有{total_prompts}个prompt组合")

# 生成Python文件内容
content = "prompts = {\n"

for name, prompt in prompts.items():
    # 从名称中提取组件
    components = name.split("_prompt_")
    if len(components) == 2:
        component1 = components[0].replace("prompt_", "")
        component2 = components[1]
    else:
        component1 = "unknown"
        component2 = "unknown"
        
    content += f'    "{name}": {{\n'
    content += f'        "content": """{prompt["content"]}""",\n'
    content += f'        "type": "{prompt["type"]}",\n'
    content += f'        "component1": "{component1}",\n'
    content += f'        "component2": "{component2}"\n'
    content += "    },\n"

content += "}"

# 将组合后的prompt保存到文件
with open("prompts/prompt_files/prompt_combined.py", "w", encoding="utf-8") as f:
    f.write(content)

print("组合后的prompt已保存到prompts/prompt_files/prompt_combined.py") 