from typing import List, Dict, Optional, Union
from .prompts import prompts

class PromptComposer:
    def __init__(self):
        # 定义prompt类型的组合策略
        self.composition_strategies = {
            'target_hijacking': {
                'type': 'pre_execution',  # 前置型，需要最先执行
                'priority': 1  # 优先级最高
            },
            'refusal_suppression': {
                'type': 'pre_execution',  # 前置型，需要最先执行
                'priority': 2
            },
            'privilege escalation': {
                'type': 'pre_execution',  # 前置型，需要最先执行
                'priority': 3
            },
            'Role-playing': {
                'type': 'wrapper',  # 包裹型，需要包裹内容
                'priority': 1  # 包裹型中的优先级
            },
            'code_injection': {
                'type': 'content',  # 内容型，不可分割
                'priority': 1  # 内容型中的优先级
            },
            'base': {
                'type': 'content',  # 内容型，不可分割
                'priority': 2  # 内容型中的优先级
            },
            'scenario simulation': {
                'type': 'wrapper',  # 包裹型，需要包裹内容
                'priority': 2  # 包裹型中的优先级
            },
            'formatted_output': {
                'type': 'content', 
                'priority': 3 
            },
            'combined': {
                'type': 'special',  # 特殊类型，表示这是一个组合结果
                'priority': 0  # 特殊类型，不参与排序
            }
        }
    
    def _sort_prompts(self, selected_prompts: List[Dict]) -> List[Dict]:
        """根据组合策略对prompt进行排序"""
        # 将prompt按类型分组
        pre_execution_prompts = []
        wrapper_prompts = []
        content_prompts = []
        
        for prompt in selected_prompts:
            strategy = self.composition_strategies.get(prompt['type'], {})
            if strategy.get('type') == 'pre_execution':
                pre_execution_prompts.append(prompt)
            elif strategy.get('type') == 'wrapper':
                wrapper_prompts.append(prompt)
            elif strategy.get('type') == 'content':
                content_prompts.append(prompt)
        
        # 对每组按priority排序
        pre_execution_prompts.sort(
            key=lambda x: self.composition_strategies.get(x['type'], {}).get('priority', float('inf'))
        )
        wrapper_prompts.sort(
            key=lambda x: self.composition_strategies.get(x['type'], {}).get('priority', float('inf'))
        )
        content_prompts.sort(
            key=lambda x: self.composition_strategies.get(x['type'], {}).get('priority', float('inf'))
        )
        
        # 前置型在前，内容型在中间，包裹型在后
        return pre_execution_prompts + content_prompts + wrapper_prompts
    
    def _compose_content(self, prompts: List[Dict], seed: str) -> str:
        """根据组合策略组合content"""
        # 将prompt按类型分组
        pre_execution_prompts = []
        wrapper_prompts = []
        content_prompts = []
        
        for prompt in prompts:
            strategy = self.composition_strategies.get(prompt['type'], {})
            if strategy.get('type') == 'pre_execution':
                pre_execution_prompts.append(prompt)
            elif strategy.get('type') == 'wrapper':
                wrapper_prompts.append(prompt)
            elif strategy.get('type') == 'content':
                content_prompts.append(prompt)
        
        # 1. 先生成内容（不包含前置型prompt）
        if content_prompts:
            # 如果有内容型prompt，使用优先级最高的
            content = content_prompts[0]['content'].replace("{seed}", seed)
        else:
            # 如果没有内容型prompt，使用原始seed
            content = seed
            
        # 2. 处理包裹型prompt
        for prompt in wrapper_prompts:
            content = prompt['content'].replace("{seed}", content)
            
        # 3. 最后处理前置型prompt（从后往前，这样优先级高的会在最外层）
        for prompt in reversed(pre_execution_prompts):
            content = prompt['content'].replace("{seed}", content)
        
        return content
    
    def compose(self, prompt_names: List[str], seed: str) -> Dict:
        """
        智能组合多个prompt并生成新的prompt
        
        Args:
            prompt_names: 要组合的prompt名称列表
            seed: 原始seed内容
            
        Returns:
            组合后的prompt字典
        """
        # 获取所有要组合的prompt
        selected_prompts = [prompts[name] for name in prompt_names]
        
        # 根据组合策略排序
        sorted_prompts = self._sort_prompts(selected_prompts)
        
        # 组合content
        combined_content = self._compose_content(sorted_prompts, seed)
        
        # 生成新的prompt
        combined_prompt = {
            'content': combined_content,
            'type': 'combined_' + '_'.join(p['type'] for p in sorted_prompts)
        }
        
        return combined_prompt

    def get_available_prompts(self) -> Dict[str, str]:
        """
        获取所有可用的prompt及其类型
        
        Returns:
            包含prompt名称和类型的字典
        """
        return {name: prompt['type'] for name, prompt in prompts.items()}
    
    def get_composition_strategies(self) -> Dict:
        """
        获取当前的组合策略配置
        
        Returns:
            组合策略配置字典
        """
        return self.composition_strategies 

    def filter_by_component(self, components: Union[str, List[str]], match_all: bool = False) -> Dict:
        """
        根据component筛选combined prompt
        
        Args:
            components: 要筛选的component,可以是单个字符串或字符串列表
            match_all: 当components是列表时,是否要求完全匹配所有component
            
        Returns:
            包含符合条件的prompt的字典
        """
        # 将单个component转换为列表
        if isinstance(components, str):
            components = [components]
            
        # 验证参数类型
        if not isinstance(components, list):
            raise TypeError("components必须是字符串或字符串列表")
            
        filtered_prompts = {}
        
        for name, prompt in prompts.items():
            # 获取prompt的components
            prompt_components = [prompt.get('component1', ''), prompt.get('component2', '')]
            
            # 根据match_all参数决定匹配逻辑
            if match_all:
                # 要求所有component都匹配
                if all(comp in prompt_components for comp in components):
                    filtered_prompts[name] = prompt
            else:
                # 只要匹配任意一个component
                if any(comp in prompt_components for comp in components):
                    filtered_prompts[name] = prompt
                    
        return filtered_prompts 