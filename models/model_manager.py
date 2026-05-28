from openai import OpenAI
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from typing import Dict, Any, List, Optional, Generator
import os
import json
import torch
from queue import Queue
from threading import Event
from huggingface_hub import InferenceClient

class StreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self, queue: Queue):
        self.queue = queue
        self.streaming_done = Event()
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.queue.put(token)
    
    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        self.streaming_done.set()
    
    def on_llm_error(self, error: Exception, **kwargs) -> None:
        self.queue.put(None)
        self.streaming_done.set()

class ModelManager:
    # 定义支持的模型
    SUPPORTED_MODELS = {
        "gpt-3.5-turbo": {
            "type": "openai",
            "model_id": "gpt-3.5-turbo"
        },
        "gpt-4": {
            "type": "openai",
            "model_id": "gpt-4"
        },
        "qwen-72b": {
            "type": "huggingface",
            "provider": "nebius",
            "model_id": "Qwen/Qwen2.5-72B-Instruct"
        },
        "qwen-32b": {
            "type": "huggingface",
            "provider": "nebius",
            "model_id": "Qwen/Qwen2.5-32B-Instruct"
        },
        "qwen-7b": {
            "type": "huggingface",
            "provider": "together",
            "model_id": "Qwen/Qwen2.5-7B-Instruct"
        },
        "llama-3.3-70b": {
            "type": "huggingface",
            "provider": "nebius",
            "model_id": "meta-llama/Llama-3.3-70B-Instruct"
        },
        "llama-3.1-8b": {
            "type": "huggingface",
            "provider": "nebius",
            "model_id": "meta-llama/Llama-3.1-8B-Instruct"
        },
        "llama-3.1-70b": {
            "type": "huggingface",
            "provider": "nebius",
            "model_id": "meta-llama/Llama-3.1-70B-Instruct"
        },
        "gemma-3-27b": {
            "type": "huggingface",
            "provider": "nebius",
            "model_id": "google/gemma-3-27b-it"
        },
        "gemma-2-27b": {
            "type": "huggingface",
            "provider": "nebius",
            "model_id": "google/gemma-2-27b-it"
        },
        "gemma-2-9b": {
            "type": "huggingface",
            "provider": "nebius",
            "model_id": "google/gemma-2-9b-it"
        }
    }
    
    def __init__(self):
        # 读取API密钥
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
            self.api_key = config.get('api_key')
            self.hf_token = config.get('huggingface_token')
        
        # 初始化OpenAI客户端
        self.client = OpenAI(api_key=self.api_key)
        
        # 初始化Inference客户端
        self.inference_clients = {}
        for model_info in self.SUPPORTED_MODELS.values():
            if model_info["type"] == "huggingface":
                provider = model_info["provider"]
                if provider not in self.inference_clients:
                    self.inference_clients[provider] = InferenceClient(
                        provider=provider,
                        api_key=self.hf_token
                    )
    
    def get_streaming_response(self, model_name: str, messages: list) -> Generator[str, None, None]:
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model: {model_name}")
        
        model_info = self.SUPPORTED_MODELS[model_name]
        
        if model_info["type"] == "openai":
            # 使用OpenAI API
            formatted_messages = []
            for msg in messages:
                if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                    formatted_messages.append({
                        "role": msg["role"],
                        "content": [{
                            "type": "text",
                            "text": msg["content"]
                        }]
                    })
            
            stream = self.client.chat.completions.create(
                model=model_info["model_id"],
                messages=formatted_messages,
                stream=True,
                temperature=0.7
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        
        elif model_info["type"] == "huggingface":
            # 使用HuggingFace Inference API
            provider = model_info["provider"]
            try:
                # 创建新的InferenceClient实例
                client = InferenceClient(
                    provider=provider,
                    api_key=self.hf_token
                )
                
                # 简化消息格式
                formatted_messages = []
                for msg in messages:
                    if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                        formatted_messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                
                # 使用更简单的API调用方式
                stream = client.chat.completions.create(
                    model=model_info["model_id"],
                    messages=formatted_messages,
                    max_tokens=2000,
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content
                        
            except Exception as e:
                print(f"Error in HuggingFace inference API ({provider}): {str(e)}")
                yield f"Error: {str(e)}"
        
        else:
            raise ValueError(f"Unknown model type: {model_info['type']}") 