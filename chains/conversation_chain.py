from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from typing import List, Tuple, Any, Generator, Dict
from models.model_manager import ModelManager
from prompts.prompt_manager import PromptManager
from queue import Queue
from threading import Event

class ConversationManager:
    def __init__(self, prompt_manager: PromptManager):
        self.model_manager = ModelManager()
        self.prompt_manager = prompt_manager
        self.conversations: Dict[str, List[dict]] = {}
    
    def initialize_conversation(self, model_name: str, system_message_key: str) -> str:
        # 生成唯一的会话ID
        conversation_id = f"{model_name}_{system_message_key}_{len(self.conversations)}"
        
        # 初始化对话历史，包含system message
        system_message = self.prompt_manager.get_system_message(system_message_key)
        self.conversations[conversation_id] = [
            {"role": "system", "content": system_message}
        ]
        return conversation_id
    
    def get_streaming_response(self, conversation_id: str, user_input: str) -> Generator[str, None, None]:
        if conversation_id not in self.conversations:
            raise ValueError(f"Unknown conversation ID: {conversation_id}")
        
        # 获取模型名称（从conversation_id中提取）
        model_name = conversation_id.split('_')[0]
        
        # 添加用户输入到对话历史
        self.conversations[conversation_id].append({"role": "user", "content": user_input})
        current_response = ""
        
        # 获取流式响应
        for token in self.model_manager.get_streaming_response(model_name, self.conversations[conversation_id]):
            current_response += token
            yield token
        
        # 将完整的助手回复添加到对话历史
        self.conversations[conversation_id].append({"role": "assistant", "content": current_response})
    
    def get_conversation_history(self, conversation_id: str) -> List[Tuple[str, str]]:
        if conversation_id not in self.conversations:
            raise ValueError(f"Unknown conversation ID: {conversation_id}")
        
        # 转换对话历史为元组格式 (不包括system message)
        history = []
        messages = self.conversations[conversation_id][1:]  # Skip system message
        
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                history.append((messages[i]["content"], messages[i + 1]["content"]))
            else:
                history.append((messages[i]["content"], ""))
        
        return history 