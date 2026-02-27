from zhipuai import ZhipuAI
import base64

client = ZhipuAI(api_key="e920f6d96baa4719b32d04fd98de17cd.5oJKuFLFjJxQogiG")

# 先测试纯文本（你已经跑通了）
print("=== 纯文本测试 ===")
response = client.chat.completions.create(
    model="glm-4v-plus",
    messages=[{"role": "user", "content": "你好，请简单介绍一下自己"}]
)
print("回复:", response.choices[0].message.content)

# 再测试图片
print("\n=== 图片测试 ===")
with open("test.jpg", "rb") as f:
    img_base = base64.b64encode(f.read()).decode()

response = client.chat.completions.create(
    model="glm-4v-plus",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base}"}},
                {"type": "text", "text": "这张图里有什么？"}
            ]
        }
    ]
)
print("图片理解:", response.choices[0].message.content)

