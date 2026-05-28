import gradio as gr
from typing import List, Tuple, Generator
from models.model_manager import ModelManager
from prompts.prompt_manager import PromptManager
from chains.conversation_chain import ConversationManager
from utils.jailbreak_detector import RegexJailbreakDetector
from itertools import zip_longest
import os

# 数据库配置
DB_CONFIG = {
    "file_path": os.path.join(os.path.dirname(__file__), "data/database.json"),  # 默认使用JSON格式
    "file_type": "json"
}

# 初始化管理器
model_manager = ModelManager()
prompt_manager = PromptManager(db_config=DB_CONFIG)  # 传入数据库配置
conversation_manager = ConversationManager(prompt_manager=prompt_manager)
jailbreak_detector = RegexJailbreakDetector()

def generate_responses(seed_choice: str, prompt_choice: str, model1_name: str, model2_name: str, system_message_key: str) -> Generator:
    # 重置检测器状态
    jailbreak_detector.reset()
    
    # 生成完整的提示词
    user_input = prompt_manager.generate_full_prompt(seed_choice, prompt_choice)
    
    # 初始化两个对话
    conv_id1 = conversation_manager.initialize_conversation(model1_name, system_message_key)
    conv_id2 = conversation_manager.initialize_conversation(model2_name, system_message_key)
    
    # 初始化聊天历史
    history1 = [{"role": "user", "content": user_input}]
    history2 = [{"role": "user", "content": user_input}]
    yield history1, history2, "", ""  # 初始状态为空
    
    # 获取流式响应
    gen1 = conversation_manager.get_streaming_response(conv_id1, user_input)
    gen2 = conversation_manager.get_streaming_response(conv_id2, user_input)
    
    # 用于收集完整响应以进行越狱检测
    response1 = ""
    response2 = ""
    
    # 流式输出
    for chunk1, chunk2 in zip_longest(gen1, gen2, fillvalue=''):
        if chunk1:
            response1 += chunk1
            if len(history1) > 1:
                history1[-1]["content"] = response1
            else:
                history1.append({"role": "assistant", "content": response1})
        if chunk2:
            response2 += chunk2
            if len(history2) > 1:
                history2[-1]["content"] = response2
            else:
                history2.append({"role": "assistant", "content": response2})
        yield history1, history2, "", ""  # 运行过程中保持为空
    
    # 越狱检测
    if response1:
        jailbreak_result1 = jailbreak_detector.detect(response1)
        analyze_text1 = f"""Model 1 Detection Result:
            - Status: {'Leak detected' if jailbreak_result1['contains_leak'] else 'No leak detected'}
            - Details: {jailbreak_result1['result']}"""
    else:
        analyze_text1 = "Model 1: No response"
    
    if response2:
        jailbreak_result2 = jailbreak_detector.detect(response2)
        analyze_text2 = f"""Model 2 Detection Result:
            - Status: {'Leak detected' if jailbreak_result2['contains_leak'] else 'No leak detected'}
            - Details: {jailbreak_result2['result']}"""
    else:
        analyze_text2 = "Model 2: No response"
    
    yield history1, history2, analyze_text1, analyze_text2

# Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("# FYP Demo")
    
    # System Message选择
    system_message_choice = gr.Dropdown(
        choices=list(prompt_manager.system_messages.keys()),
        value="system_message0",
        label="选择 System Message"
    )
    
    system_message_display = gr.Textbox(
        value=prompt_manager.get_system_message("system_message0"),
        label="System Message (Selected)",
        lines=15,
        interactive=False
    )
    
    with gr.Row():
        with gr.Column():
            # 获取所有支持的模型名称
            supported_models = list(model_manager.SUPPORTED_MODELS.keys())
            
            model_dropdown1 = gr.Dropdown(
                choices=supported_models,
                value='gpt-3.5-turbo',
                label='选择 Model 1'
            )
            chatbot1 = gr.Chatbot(label="Model 1 Chat", type="messages")
            analyze_text1 = gr.Textbox(value="", label="Model 1 Analysis", interactive=False)
        
        with gr.Column():
            model_dropdown2 = gr.Dropdown(
                choices=supported_models,
                value='gpt-4',
                label='选择 Model 2'
            )
            chatbot2 = gr.Chatbot(label="Model 2 Chat", type="messages")
            analyze_text2 = gr.Textbox(value="", label="Model 2 Analysis", interactive=False)
    
    with gr.Row():
        seed_choice = gr.Dropdown(
            choices=list(prompt_manager.seeds.keys()),
            value="seed1",
            label="选择 Seed"
        )
        prompt_choice = gr.Dropdown(
            choices=list(prompt_manager.prompts.keys()),
            value="prompt1",
            label="选择 Prompt"
        )
    
    full_prompt_display = gr.Textbox(
        value="",
        label="Full Prompt (Generated)",
        interactive=False
    )
    
    send_btn = gr.Button("Submit")
    
    # 事件处理
    def update_prompt_display(seed_choice_value: str, prompt_choice_value: str) -> str:
        return prompt_manager.generate_full_prompt(seed_choice_value, prompt_choice_value)
    
    seed_choice.change(
        fn=update_prompt_display,
        inputs=[seed_choice, prompt_choice],
        outputs=full_prompt_display
    )
    
    prompt_choice.change(
        fn=update_prompt_display,
        inputs=[seed_choice, prompt_choice],
        outputs=full_prompt_display
    )
    
    def update_system_message_display(system_message_key: str) -> str:
        return prompt_manager.get_system_message(system_message_key)
    
    system_message_choice.change(
        fn=update_system_message_display,
        inputs=[system_message_choice],
        outputs=system_message_display
    )
    
    send_btn.click(
        fn=generate_responses,
        inputs=[seed_choice, prompt_choice, model_dropdown1, model_dropdown2, system_message_choice],
        outputs=[chatbot1, chatbot2, analyze_text1, analyze_text2],
        queue=True,
    )

if __name__ == "__main__":
    demo.launch(share=True)
