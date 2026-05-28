import os
import json
from models.model_manager import ModelManager
from prompts.prompt_manager import PromptManager
from utils.jailbreak_detector import RegexJailbreakDetector
from typing import List, Dict, Any
from datetime import datetime
import subprocess
import sys

# 配置
DB_CONFIG = {
    "file_path": os.path.join(os.path.dirname(__file__), "data/database.json"),
    "file_type": "json"
}

# 默认测试参数
SEED_KEY = "seed1"  # 选择要使用的seed
SYSTEM_MESSAGE_KEY = "system_message2"  # 选择要使用的system message

# 结果文件夹
RESULTS_DIR = "results"

def get_user_choice(options: List[str], title: str) -> int:
    """显示选项并获取用户选择"""
    print(f"\n{title}")
    print("-" * 50)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("-" * 50)
    
    while True:
        try:
            choice = int(input("请选择 (输入数字): "))
            if 1 <= choice <= len(options):
                return choice - 1
            print("无效的选择，请重试")
        except ValueError:
            print("请输入有效的数字")

def select_model() -> str:
    """让用户选择模型"""
    # 初始化管理器以获取选项
    model_manager = ModelManager()
    
    # 获取可用的模型列表
    available_models = list(model_manager.SUPPORTED_MODELS.keys())
    
    # 选择模型
    model_index = get_user_choice(available_models, "请选择要使用的模型:")
    selected_model = available_models[model_index]
    
    # 确认选择
    print("\n您的选择:")
    print(f"模型: {selected_model}")
    confirm = input("确认使用这个模型吗？(y/n): ").lower()
    
    if confirm == 'y':
        return selected_model
    else:
        print("重新选择...")
        return select_model()

def get_all_prompts() -> List[str]:
    """获取所有可用的prompt"""
    prompt_manager = PromptManager(db_config=DB_CONFIG)
    return list(prompt_manager.prompts.keys())

def run_single_test(model_name: str, prompt_key: str) -> Dict[str, Any]:
    """运行单个prompt的测试并返回结果"""
    print(f"\n开始测试Prompt: {prompt_key}")
    print("-" * 50)
    
    try:
        # 使用subprocess运行leak_test.py
        result = subprocess.run(
            [sys.executable, "leak_test.py", "--auto", model_name, prompt_key],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"测试 {prompt_key} 失败:")
            print(result.stderr)
            return None
        
        # 从输出中提取结果文件名
        output = result.stdout
        result_file = None
        for line in output.split('\n'):
            if "详细结果已保存到:" in line:
                result_file = line.split("详细结果已保存到:")[1].strip()
                break
        
        if not result_file or not os.path.exists(result_file):
            print(f"无法找到结果文件: {result_file}")
            return None
        
        # 读取结果文件
        with open(result_file, 'r', encoding='utf-8') as f:
            result_data = json.load(f)
        
        return {
            "prompt": prompt_key,
            "metadata": result_data["metadata"],
            "detailed_results": result_data["detailed_results"]
        }
            
    except Exception as e:
        print(f"测试 {prompt_key} 发生错误: {str(e)}")
        return None

def save_summary(model_name: str, results: List[Dict[str, Any]]) -> None:
    """保存测试总结"""
    # 创建结果文件夹
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"summary_{model_name}_{timestamp}.json"
    output_file = os.path.join(RESULTS_DIR, filename)
    
    # 按prompt分类统计
    prompt_stats = {}
    for result in results:
        prompt = result["prompt"]
        prompt_stats[prompt] = {
            "metadata": result["metadata"],
            "confusion_matrix": result["metadata"]["confusion_matrix"],
            "metrics": result["metadata"]["metrics"]
        }
    
    # 保存总结
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "model": model_name,
                "timestamp": timestamp
            },
            "prompt_stats": prompt_stats,
            "detailed_results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n测试总结已保存到: {output_file}")
    
    # 显示每个prompt的统计
    print("\n各Prompt测试结果:")
    for prompt, stats in prompt_stats.items():
        print(f"\nPrompt: {prompt}")
        print(f"  测试次数: {stats['metadata']['total_tests']}")
        print(f"  完全绕过次数: {stats['metadata']['bypass_count']}")
        print(f"  防御成功次数: {stats['metadata']['defense_success_count']}")
        print(f"  防御失效次数: {stats['metadata']['defense_failure_count']}")
        print(f"  无关内容次数: {stats['metadata']['irrelevant_count']}")
        print(f"  绕过率: {stats['metadata']['bypass_rate']:.2%}")
        print(f"  防御成功率: {stats['metadata']['defense_success_rate']:.2%}")
        print(f"  混淆矩阵: TP={stats['confusion_matrix']['TP']}, FP={stats['confusion_matrix']['FP']}, TN={stats['confusion_matrix']['TN']}, FN={stats['confusion_matrix']['FN']}")
        print(f"  评估指标:")
        for metric, value in stats['metrics'].items():
            print(f"    {metric}: {value:.3f}")

def main():
    print("=" * 50)
    
    # 选择模型
    model_name = select_model()
    
    # 获取所有prompt
    prompts = get_all_prompts()
    print(f"\n将测试 {len(prompts)} 个不同的prompt")
    
    # 运行所有测试
    all_results = []
    for prompt in prompts:
        result = run_single_test(model_name, prompt)
        if result:
            all_results.append(result)
    
    # 保存总结
    save_summary(model_name, all_results)

if __name__ == "__main__":
    main() 