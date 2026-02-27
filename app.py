import gradio as gr
from zhipuai import ZhipuAI
import base64
import time
import os

# 初始化客户端
client = ZhipuAI(api_key="e920f6d96baa4719b32d04fd98de17cd.5oJKuFLFjJxQogiG") 

# 存储对话历史的全局变量
history = []

def chat_with_image(message, chat_history, image):
    """处理聊天的主函数"""
    global history
    
    # 记录开始时间
    start_time = time.time()
    
    # 构建消息列表
    messages = []
    
    # 添加历史对话
    for user_msg, assistant_msg in chat_history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    
    # 处理当前输入
    if image is not None:
        # 有图片的情况
        with open(image, "rb") as f:
            img_base = base64.b64encode(f.read()).decode()
        
        content = [
            {
                "type": "image_url", 
                "image_url": {"url": f"data:image/jpeg;base64,{img_base}"}
            },
            {
                "type": "text", 
                "text": message
            }
        ]
    else:
        # 纯文本的情况
        content = message
    
    messages.append({"role": "user", "content": content})
    
    # 调用 API
    response = client.chat.completions.create(
        model="glm-4v-plus",
        messages=messages
    )
    
    # 计算延迟
    latency = time.time() - start_time
    
    reply = response.choices[0].message.content
    
    # 更新对话历史
    chat_history.append((message, reply))
    
    return chat_history, chat_history, f"延迟: {latency:.2f}秒"

# 创建 Gradio 界面
with gr.Blocks(title="多模态聊天小豆包", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🧸 多模态聊天小豆包
    可以聊文字，也可以上传图片问我问题！
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="对话历史", height=400)
            msg = gr.Textbox(label="输入消息", placeholder="在这里输入文字...")
            with gr.Row():
                clear = gr.Button("清空对话")
                submit = gr.Button("发送", variant="primary")
        
        with gr.Column(scale=1):
            image_input = gr.Image(type="filepath", label="上传图片（可选）")
            latency_display = gr.Textbox(label="响应时间", interactive=False)
    
    # 绑定事件
    submit.click(
        chat_with_image, 
        [msg, chatbot, image_input], 
        [chatbot, chatbot, latency_display]
    )
    
    msg.submit(
        chat_with_image, 
        [msg, chatbot, image_input], 
        [chatbot, chatbot, latency_display]
    )
    
    clear.click(lambda: None, None, chatbot, queue=False)

# 启动
if __name__ == "__main__":
    demo.launch(share=True)
