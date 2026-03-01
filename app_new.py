import gradio as gr
from openai import OpenAI
import base64
import time
import os
import shutil
import uuid
import socket
import oss2

# ========== OSS 配置 ==========
OSS_ACCESS_KEY_ID = "LTAI5tKSM4F4ZJKp3WYdAxvh"
OSS_ACCESS_KEY_SECRET = "8nl24pGJEeFQCVZCpq7zWhxfeIHW5q"
OSS_BUCKET_NAME = "talk2mag-media"
OSS_ENDPOINT = "https://oss-cn-hangzhou.aliyuncs.com"  # 华东1（杭州）

# 初始化OSS客户端
auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)

# 获取本机IP
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"📡 本机IP: {local_ip}")

# 创建临时文件夹（文件会先存这里再上传OSS）
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

# 初始化阿里云客户端
client = OpenAI(
    api_key="sk-176c555ead1f4db8a28d3ac9fc1e74b2",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def upload_to_oss(local_file_path, filename):
    """上传文件到OSS，返回公网URL（文件设为公共读）"""
    # OSS中的路径
    oss_key = f"uploads/{filename}"
    
    # 上传文件并设置权限为公共读
    bucket.put_object_from_file(oss_key, local_file_path, headers={
        'x-oss-object-acl': 'public-read'
    })
    
    # 生成公网URL - 使用你的OSS地址！
    file_url = f"https://{OSS_BUCKET_NAME}.oss-cn-hangzhou.aliyuncs.com/{oss_key}"
    
    return file_url

def chat_with_message(message, chat_history, file, max_tokens):
    """处理聊天的主函数，支持图片"""
    start_time = time.time()
    
    # 构建消息列表
    messages = []
    for user_msg, assistant_msg in chat_history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    
    # 处理文件上传
    if file is not None:
        file_name = os.path.basename(file.name)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        # 生成唯一的文件名
        unique_id = str(uuid.uuid4())[:8]
        saved_filename = f"{unique_id}_{file_name}"
        temp_path = os.path.join(TEMP_DIR, saved_filename)
        
        # 复制上传的文件到临时文件夹
        shutil.copy2(file.name, temp_path)
        
        # 上传到OSS并获取公网URL
        try:
            file_url = upload_to_oss(temp_path, saved_filename)
            print(f"📁 文件已上传到OSS: {file_url}")
        except Exception as e:
            print(f"❌ OSS上传失败: {str(e)}")
            reply = f"文件上传失败: {str(e)}"
            latency = time.time() - start_time
            chat_history.append((message, reply))
            return chat_history, chat_history, f"延迟: {latency:.2f}秒"
        
        # 图片格式
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            # 发给模型的消息（带提示词）
            model_text = f"{message} 请用少于{max_tokens}个字回答。"
            content = [
                {
                    "type": "image_url",
                    "image_url": {"url": file_url}
                },
                {
                    "type": "text",
                    "text": model_text
                }
            ]
            messages.append({"role": "user", "content": content})
            
        # 视频格式（保留但不使用）
        elif file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']:
            content = [
                {
                    "type": "video",
                    "video": file_url
                },
                {
                    "type": "text",
                    "text": message
                }
            ]
            messages.append({"role": "user", "content": content})
            
        else:
            reply = f"不支持的文件格式：{file_ext}"
            latency = time.time() - start_time
            chat_history.append((message, reply))
            return chat_history, chat_history, f"延迟: {latency:.2f}秒"
        
        # 调用API
        try:
            response = client.chat.completions.create(
                model="qwen-vl-plus",
                messages=messages,
                max_tokens=max_tokens
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"调用API时出错: {str(e)}"
            
    else:
        # 纯文本 - 重点修复部分
        # 发给模型的消息（带提示词）
        model_message = f"{message} 请用少于{max_tokens}个字回答。"
        messages.append({"role": "user", "content": model_message})
        
        try:
            response = client.chat.completions.create(
                model="qwen-vl-plus",
                messages=messages,
                max_tokens=max_tokens
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"调用API时出错: {str(e)}"
    
    # 聊天记录里显示原始消息（不带提示词）
    chat_history.append((message, reply))
    
    latency = time.time() - start_time
    return chat_history, chat_history, f"延迟: {latency:.2f}秒"

# 创建 Gradio 界面
with gr.Blocks(title="Talk 2 Mag", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 💬 Talk 2 Mag
    一个支持文字和图片的多模态聊天系统
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="对话历史", height=400)
            msg = gr.Textbox(label="输入消息", placeholder="在这里输入文字...")
            with gr.Row():
                clear = gr.Button("清空对话")
                submit = gr.Button("发送", variant="primary")
        
        with gr.Column(scale=1):
            file_input = gr.File(label="上传文件", file_types=["image", "video"])
            max_tokens = gr.Slider(minimum=50, maximum=500, value=256, step=10, label="最大生成长度")
            latency_display = gr.Textbox(label="响应时间", interactive=False)
    
    # 绑定事件
    submit.click(
        chat_with_message, 
        [msg, chatbot, file_input, max_tokens], 
        [chatbot, chatbot, latency_display]
    )
    
    msg.submit(
        chat_with_message, 
        [msg, chatbot, file_input, max_tokens], 
        [chatbot, chatbot, latency_display]
    )
    
    clear.click(lambda: None, None, chatbot, queue=False)

# 启动
if __name__ == "__main__":
    demo.launch(share=True)
