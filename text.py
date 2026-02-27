from zhipuai import ZhipuAI

# 初始化客户端（把Key填进去）
client = ZhipuAI(api_key="YOUR_API_KEY")

# 测试纯文本对话
response = client.chat.completions.create(
    model="glm-4v-plus",  # 多模态模型
    messages=[
        {"role": "user", "content": "你好，请简单介绍一下自己"}
    ]
)

print("回复:", response.choices[0].message.content)