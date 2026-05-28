from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from typing import Dict, List, Any, Optional
import json
import csv
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from .prompt_files.prompts import prompts as prompts_data

class PromptType(Enum):
    TARGET_HIJACKING = "target_hijacking"
    REFUSAL_SUPPRESSION = "refusal_suppression"
    BASE = "base"
    COMBINED = "combined"
    PRIVILEGE_ESCALATION = "privilege escalation"
    ROLE_PLAYING = "Role-playing"
    CODE_INJECTION = "code_injection"
    SCENARIO_SIMULATION = "scenario simulation"
    FORMATTED_OUTPUT = "formatted_output"

@dataclass
class PromptTemplate:
    content: str
    type: PromptType

class PromptManager:
    def __init__(self, db_config: Dict[str, str] = None):
        self.database = []
        if db_config:
            self.load_database(db_config)
            
        # 加载所有prompt文件
        self.prompt_dir = Path(__file__).parent / "prompt_files"
        self.system_messages = self._load_json_file("system_messages.json")
        self.seeds = self._load_json_file("seeds.json")
        self.prompts = {}
        
        # 从Python文件加载所有prompt
        self._load_prompts_from_python()

    def _load_json_file(self, filename: str) -> Dict:
        """加载JSON文件"""
        file_path = self.prompt_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {filename}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_prompts_from_python(self) -> None:
        """从Python文件加载prompt到prompts字典"""
        for key, data in prompts_data.items():
            self.prompts[key] = PromptTemplate(
                content=data["content"],
                type=PromptType(data["type"])
            )

    def load_database(self, config: Dict[str, str]) -> None:
        """
        从配置的文件中加载数据库
        config 格式: {
            "file_path": "path/to/file",
            "file_type": "json|csv"
        }
        """
        file_path = config.get("file_path")
        file_type = config.get("file_type", "").lower()

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"数据库文件不存在: {file_path}")

        try:
            if file_type == "json":
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.database = json.load(f)
            elif file_type == "csv":
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    self.database = list(reader)
            else:
                raise ValueError(f"不支持的文件类型: {file_type}")
        except Exception as e:
            raise Exception(f"加载数据库文件时出错: {str(e)}")

    def get_system_message(self, key: str) -> str:
        if key not in self.system_messages:
            raise ValueError(f"Unknown system message key: {key}")
        
        message = self.system_messages[key]["content"]
        # 检查消息中是否包含{database}占位符
        if "{database}" in message:
            database_str = json.dumps(self.database, ensure_ascii=False, indent=2)
            message = message.format(database=database_str)
        
        return message
    
    def get_seed(self, key: str) -> str:
        if key not in self.seeds:
            raise ValueError(f"Unknown seed key: {key}")
        return self.seeds[key]["content"]
    
    def get_prompt(self, key: str) -> str:
        if key not in self.prompts:
            raise ValueError(f"Unknown prompt key: {key}")
        return self.prompts[key].content
    
    def generate_full_prompt(self, seed_key: str, prompt_key: Optional[str] = None, prompt_types: Optional[List[PromptType]] = None) -> str:
        """
        生成完整的提示词
        
        Args:
            seed_key: 种子提示词的key
            prompt_key: 单个提示词的key
            prompt_types: 要组合的提示词类型列表
            
        Returns:
            完整的提示词
        """
        seed = self.get_seed(seed_key)
        
        if prompt_key:
            prompt_template = self.get_prompt(prompt_key)
        elif prompt_types:
            prompt_template = self.combine_prompts(prompt_types)
        else:
            raise ValueError("必须提供prompt_key或prompt_types")
            
        return prompt_template.replace("{seed}", seed)
    
    def create_chat_prompt(self, system_message_key: str, user_input: str) -> ChatPromptTemplate:
        system_message = self.get_system_message(system_message_key)
        
        system_prompt = SystemMessagePromptTemplate.from_template(system_message)
        human_prompt = HumanMessagePromptTemplate.from_template("{user_input}")
        
        return ChatPromptTemplate.from_messages([system_prompt, human_prompt])

    def combine_prompts(self, prompt_types: List[PromptType]) -> str:
        """
        组合多个类型的提示词模板
        
        Args:
            prompt_types: 要组合的提示词类型列表
            
        Returns:
            组合后的提示词模板
        """
        # 获取所有匹配类型的模板
        templates = [
            template for template in self.prompts.values()
            if template.type in prompt_types
        ]
        
        # 组合模板
        combined = ""
        for template in templates:
            combined += template.content + "\n\n"
        
        return combined.strip() 