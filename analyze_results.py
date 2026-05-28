import os
import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Any
from collections import defaultdict

class ResultsAnalyzer:
    def __init__(self, results_dir: str = "results"):
        self.results_dir = results_dir
        self.results = []
        self.model_stats = defaultdict(lambda: defaultdict(list))
        self.prompt_stats = defaultdict(lambda: defaultdict(list))
        
    def extract_model_and_prompt(self, filename: str) -> tuple:
        """从文件名中提取模型名和prompt类型"""
        try:
            if '_prompt_' in filename:
                model_name = filename.split('_prompt_')[0]
                prompt_type = filename.split('_prompt_')[1].split('_')[0] + '_' + filename.split('_prompt_')[1].split('_')[1]
            elif '_prompt' in filename:
                model_name = filename.split('_prompt')[0]
                prompt_type = 'prompt0'
            else:
                return None, None
            return model_name, prompt_type
        except Exception:
            return None, None
        
    def load_results(self):
        """加载所有结果文件"""
        json_files = glob.glob(os.path.join(self.results_dir, "*.json"))
        for file_path in json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    filename = os.path.basename(file_path)
                    model_name, prompt_type = self.extract_model_and_prompt(filename)
                    
                    if model_name and prompt_type:
                        # 存储结果
                        self.results.append({
                            'model': model_name,
                            'prompt': prompt_type,
                            'data': data
                        })
                        
                        # 更新统计信息
                        self.model_stats[model_name][prompt_type].append(data)
                        self.prompt_stats[prompt_type][model_name].append(data)
            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")
    
    def analyze_model_performance(self) -> Dict[str, Any]:
        """分析每个模型在不同prompt下的表现"""
        analysis = {}
        for model, prompt_data in self.model_stats.items():
            model_analysis = {
                'total_tests': 0,
                'leak_detected': 0,
                'refusal_detected': 0,
                'prompt_performance': {}
            }
            
            for prompt, results in prompt_data.items():
                prompt_stats = {
                    'total_tests': 0,
                    'leak_detected': 0,
                    'refusal_detected': 0,
                    'true_positives': 0,
                    'true_negatives': 0,
                    'false_positives': 0,
                    'false_negatives': 0
                }
                
                for result in results:
                    metadata = result.get('metadata', {})
                    # 获取基本统计数据
                    prompt_stats['total_tests'] += metadata.get('total_tests', 0)
                    prompt_stats['leak_detected'] += metadata.get('leak_detected', 0)
                    prompt_stats['refusal_detected'] += metadata.get('refusal_detected', 0)
                    
                    # 从confusion_matrix中获取详细指标
                    confusion_matrix = metadata.get('confusion_matrix', {})
                    prompt_stats['true_positives'] += confusion_matrix.get('TP', 0)
                    prompt_stats['true_negatives'] += confusion_matrix.get('TN', 0)
                    prompt_stats['false_positives'] += confusion_matrix.get('FP', 0)
                    prompt_stats['false_negatives'] += confusion_matrix.get('FN', 0)
                
                model_analysis['prompt_performance'][prompt] = prompt_stats
                model_analysis['total_tests'] += prompt_stats['total_tests']
                model_analysis['leak_detected'] += prompt_stats['leak_detected']
                model_analysis['refusal_detected'] += prompt_stats['refusal_detected']
            
            analysis[model] = model_analysis
        
        return analysis
    
    def analyze_prompt_performance(self) -> Dict[str, Any]:
        """分析每个prompt在不同模型下的表现"""
        analysis = {}
        for prompt, model_data in self.prompt_stats.items():
            prompt_analysis = {
                'total_tests': 0,
                'successful_tests': 0,
                'failed_tests': 0,
                'leak_detected': 0,
                'model_performance': {}
            }
            
            for model, results in model_data.items():
                model_stats = {
                    'total_tests': 0,
                    'successful_tests': 0,
                    'failed_tests': 0,
                    'leak_detected': 0
                }
                
                for result in results:
                    metadata = result.get('metadata', {})
                    model_stats['total_tests'] += metadata.get('total_tests', 0)
                    model_stats['successful_tests'] += metadata.get('successful_tests', 0)
                    model_stats['failed_tests'] += metadata.get('failed_tests', 0)
                    model_stats['leak_detected'] += metadata.get('leak_detected', 0)
                
                prompt_analysis['model_performance'][model] = model_stats
                prompt_analysis['total_tests'] += model_stats['total_tests']
                prompt_analysis['successful_tests'] += model_stats['successful_tests']
                prompt_analysis['failed_tests'] += model_stats['failed_tests']
                prompt_analysis['leak_detected'] += model_stats['leak_detected']
            
            analysis[prompt] = prompt_analysis
        
        return analysis
    
    def sort_models(self, models: List[str]) -> List[str]:
        """对模型名称进行排序"""
        def get_sort_key(model_name: str) -> tuple:
            # 提取模型系列和大小
            if 'llama' in model_name:
                series = 1  # llama排在最前
            elif 'qwen' in model_name:
                series = 2  # qwen排在中间
            elif 'gemma' in model_name:
                series = 3  # gemma排在最后
            else:
                series = 4  # 其他模型排在最后
            
            # 提取版本号和大小
            try:
                if 'llama' in model_name:
                    version = float(model_name.split('-')[1])
                    size = int(model_name.split('-')[-1].replace('b', ''))
                elif 'qwen' in model_name:
                    size = int(model_name.split('-')[-1].replace('b', ''))
                    version = 1
                elif 'gemma' in model_name:
                    version = int(model_name.split('-')[1])
                    size = int(model_name.split('-')[-1].replace('b', ''))
                else:
                    version = 0
                    size = 0
            except:
                version = 0
                size = 0
            
            # 返回排序键（负号使得大的值排在前面）
            return (series, -version, -size)
        
        return sorted(models, key=get_sort_key)
    
    def sort_prompts(self, prompts: List[str]) -> List[str]:
        """对prompt类型进行排序"""
        # 定义prompt类型的顺序
        prompt_order = {
            'prompt0': 0,
            'target_hijacking': 1,
            'privilege_escalation': 2,
            'refusal_suppression': 3,
            'role_playing': 4,
            'formatted_output': 5,
            'code_injection': 6,
            'combined': 7,
            'scenario_simulation': 8
        }
        
        def get_sort_key(prompt: str) -> tuple:
            # 获取基本prompt类型
            base_type = '_'.join(prompt.split('_')[:2])
            # 获取编号（如果有）
            try:
                number = int(''.join(filter(str.isdigit, prompt)))
            except:
                number = 0
            
            # 获取类型的排序值
            type_order = 999  # 默认值
            for key, value in prompt_order.items():
                if key in base_type:
                    type_order = value
                    break
            
            return (type_order, number)
        
        return sorted(prompts, key=get_sort_key)
    
    def generate_visualizations(self, model_analysis: Dict[str, Any], prompt_analysis: Dict[str, Any]):
        """生成可视化图表"""
        # 创建输出目录
        os.makedirs('analysis_results', exist_ok=True)
        
        # 模型表现分析
        models = self.sort_models(list(model_analysis.keys()))
        prompts = set()
        for model_data in model_analysis.values():
            prompts.update(model_data['prompt_performance'].keys())
        prompts = self.sort_prompts(list(prompts))
        
        # 创建不同指标的DataFrame
        leak_rate_df = pd.DataFrame(index=prompts, columns=models)
        rejection_rate_df = pd.DataFrame(index=prompts, columns=models)
        tp_rate_df = pd.DataFrame(index=prompts, columns=models)
        tn_rate_df = pd.DataFrame(index=prompts, columns=models)
        fp_rate_df = pd.DataFrame(index=prompts, columns=models)
        fn_rate_df = pd.DataFrame(index=prompts, columns=models)
        
        # 填充数据
        for model, data in model_analysis.items():
            for prompt, stats in data['prompt_performance'].items():
                total_tests = stats['total_tests']
                if total_tests > 0:
                    # True Positives (检测到泄露且确实泄露)
                    tp_rate_df.loc[prompt, model] = stats['true_positives']
                    
                    # True Negatives (未检测到泄露且确实未泄露)
                    tn_rate_df.loc[prompt, model] = stats['true_negatives']
                    
                    # False Positives (检测到泄露但实际未泄露)
                    fp_rate_df.loc[prompt, model] = stats['false_positives']
                    
                    # False Negatives (未检测到泄露但实际泄露)
                    fn_rate_df.loc[prompt, model] = stats['false_negatives']
                    
                    # 泄露数量
                    leak_rate_df.loc[prompt, model] = stats['leak_detected']
                    
                    # 拒绝数量
                    rejection_rate_df.loc[prompt, model] = stats['refusal_detected']
                else:
                    # 如果没有测试数据，所有值都设为0
                    tp_rate_df.loc[prompt, model] = 0
                    tn_rate_df.loc[prompt, model] = 0
                    fp_rate_df.loc[prompt, model] = 0
                    fn_rate_df.loc[prompt, model] = 0
                    leak_rate_df.loc[prompt, model] = 0
                    rejection_rate_df.loc[prompt, model] = 0
        
        # 重命名DataFrame以反映它们现在存储的是数量而不是比率
        tp_count_df = tp_rate_df.astype(float)
        tn_count_df = tn_rate_df.astype(float)
        fp_count_df = fp_rate_df.astype(float)
        fn_count_df = fn_rate_df.astype(float)
        leak_count_df = leak_rate_df.astype(float)
        rejection_count_df = rejection_rate_df.astype(float)
        
        # 确保所有值都是整数
        tp_count_df = tp_count_df.round().astype(int)
        tn_count_df = tn_count_df.round().astype(int)
        fp_count_df = fp_count_df.round().astype(int)
        fn_count_df = fn_count_df.round().astype(int)
        leak_count_df = leak_count_df.round().astype(int)
        rejection_count_df = rejection_count_df.round().astype(int)
        
        # 生成所有图表
        self._generate_heatmap(leak_count_df, 'Leak Count', 'leak_count_heatmap.png')
        self._generate_heatmap(rejection_count_df, 'Rejection Count', 'rejection_count_heatmap.png')
        self._generate_heatmap(tp_count_df, 'True Positive Count', 'tp_count_heatmap.png')
        self._generate_heatmap(tn_count_df, 'True Negative Count', 'tn_count_heatmap.png')
        self._generate_heatmap(fp_count_df, 'False Positive Count', 'fp_count_heatmap.png')
        self._generate_heatmap(fn_count_df, 'False Negative Count', 'fn_count_heatmap.png')
    
    def _generate_heatmap(self, df: pd.DataFrame, title: str, filename: str):
        """生成单个热力图"""
        fig, ax = plt.subplots(figsize=(16, 12))
        
        # 绘制热力图，设置值范围为0-20
        im = ax.imshow(df.values, cmap='YlOrRd', aspect='auto', vmin=0, vmax=20)
        
        # 添加颜色条
        cbar = plt.colorbar(im, ax=ax, label=title)
        cbar.ax.tick_params(labelsize=10)
        
        # 设置坐标轴标签
        ax.set_xticks(range(len(df.columns)))
        ax.set_yticks(range(len(df.index)))
        ax.set_xticklabels(df.columns, rotation=45, ha='right', fontsize=10)
        ax.set_yticklabels(df.index, fontsize=10)
        
        # 添加网格线
        ax.set_xticks(np.arange(-.5, len(df.columns), 1), minor=True)
        ax.set_yticks(np.arange(-.5, len(df.index), 1), minor=True)
        ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
        
        # 添加数值标签（不再显示百分比）
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                value = df.values[i, j]
                text_color = 'white' if value > 10 else 'black'
                ax.text(j, i, f'{value:.0f}', ha='center', va='center', 
                       color=text_color, fontsize=8)
        
        # 设置标题
        plt.title(title, pad=20, fontsize=14)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        plt.savefig(f'analysis_results/{filename}', 
                   bbox_inches='tight', dpi=300)
        plt.close()
    
    def save_analysis(self, model_analysis: Dict[str, Any], prompt_analysis: Dict[str, Any]):
        """保存分析结果"""
        analysis_results = {
            'model_analysis': model_analysis,
            'prompt_analysis': prompt_analysis
        }
        
        with open('analysis_results/analysis_summary.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=2)

def main():
    analyzer = ResultsAnalyzer()
    analyzer.load_results()
    
    model_analysis = analyzer.analyze_model_performance()
    prompt_analysis = analyzer.analyze_prompt_performance()
    
    analyzer.generate_visualizations(model_analysis, prompt_analysis)
    analyzer.save_analysis(model_analysis, prompt_analysis)
    
    print("分析完成！结果已保存到 analysis_results 目录")

if __name__ == "__main__":
    main() 