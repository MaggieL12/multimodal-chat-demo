import time
import psutil
import os
from zhipuai import ZhipuAI
import base64

# 配置（换成你的 Key）
client = ZhipuAI(api_key="e920f6d96baa4719b32d04fd98de17cd.5oJKuFLFjJxQogiG")

def measure_startup():
    """测试启动时间和内存"""
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    start = time.time()
    # 模拟启动（实际是第一次调用）
    response = client.chat.completions.create(
        model="glm-4v-plus",
        messages=[{"role": "user", "content": "hi"}]
    )
    startup_time = time.time() - start
    
    mem_after = process.memory_info().rss / 1024 / 1024
    mem_used = mem_after - mem_before
    
    return startup_time, mem_used

def measure_latency(test_type="text", image_path=None):
    """测试首Token延迟"""
    start = time.time()
    
    if test_type == "text":
        messages = [{"role": "user", "content": "请用一句话介绍北京"}]
    else:
        with open(image_path, "rb") as f:
            img_base = base64.b64encode(f.read()).decode()
        messages = [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base}"}},
                {"type": "text", "text": "这张图里有什么？"}
            ]
        }]
    
    response = client.chat.completions.create(
        model="glm-4v-plus",
        messages=messages
    )
    
    latency = time.time() - start
    reply = response.choices[0].message.content
    tokens = len(reply) / 2  # 粗略估算
    
    return latency, len(reply), tokens / latency

def measure_multi_turn():
    """测试多轮对话性能"""
    messages = []
    times = []
    
    for i in range(5):
        messages.append({"role": "user", "content": f"这是第{i+1}轮对话，请简单回复我"})
        
        start = time.time()
        response = client.chat.completions.create(
            model="glm-4v-plus",
            messages=messages
        )
        latency = time.time() - start
        times.append(latency)
        
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
        
        print(f"第{i+1}轮延迟: {latency:.2f}秒")
    
    return sum(times)/len(times), max(times)

# 执行测试
print("=== 启动性能测试 ===")
startup_time, mem_used = measure_startup()
print(f"首次响应时间: {startup_time:.2f}秒")
print(f"内存占用: {mem_used:.1f} MB")

print("\n=== 纯文本延迟测试（5次平均）===")
text_latencies = []
for i in range(5):
    latency, length, speed = measure_latency("text")
    text_latencies.append(latency)
    print(f"第{i+1}次: {latency:.2f}秒, 回复长度: {length}字, 吐字率: {speed:.1f}字/秒")

print(f"\n平均文本延迟: {sum(text_latencies)/5:.2f}秒")

print("\n=== 图片延迟测试 ===")
if os.path.exists("test.jpg"):
    latency, length, speed = measure_latency("image", "test.jpg")
    print(f"图片延迟: {latency:.2f}秒")
    print(f"回复长度: {length}字")
    print(f"吐字率: {speed:.1f}字/秒")
else:
    print("未找到 test.jpg，跳过图片测试")

print("\n=== 多轮对话性能 ===")
avg_turn, max_turn = measure_multi_turn()
print(f"平均每轮延迟: {avg_turn:.2f}秒")
print(f"最高延迟: {max_turn:.2f}秒")
