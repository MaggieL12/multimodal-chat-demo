# 多模态聊天小豆包

基于智谱AI glm-4v-plus 模型的多模态对话系统，支持文字和图片输入，具备多轮对话记忆能力。

## 功能特点

- ✅ **纯文本对话** - 支持多轮自然语言对话
- ✅ **图片理解** - 上传图片并提问，模型能理解图像内容
- ✅ **多轮对话记忆** - 保持上下文连贯性
- ✅ **Web界面** - 基于Gradio的友好交互界面
- ✅ **实时延迟显示** - 每次回复显示响应时间

## 快速开始

### 环境要求
- Python 3.9+
- 智谱AI API Key

### 安装步骤
```bash
# 1. 克隆项目
git clone https://github.com/MaggieL12/multimodal-chat-demo.git
cd multimodal-chat-demo

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置API Key
# 在 app.py 中替换 api_key="你的智谱AI API Key"

# 5. 运行
python app.py
```

启动后访问 http://127.0.0.1:7860 即可使用

## 📊 性能指标

| 指标 | 数值 | 说明 |
|:---|:---|:---|
| 平均文本延迟 | 0.76秒 | 5次测试平均 |
| 图片理解延迟 | 2.76秒 | 上传+理解耗时 |
| 文本吐字率 | 24.5字/秒 | 生成速度 |
| 多轮对话平均 | 0.49秒 | 5轮对话平均 |
| 内存占用 | 1.7 MB | 客户端内存 |

## 📸 功能展示

### 纯文本对话
![纯文本对话](docs/demo1.png)

### 图片理解
![图片理解](docs/demo2.png)

### 多轮对话
![多轮对话](docs/demo3.png)

## ⚠️ 已知限制

- **图片延迟较高**：图片理解比纯文本慢约2秒
- **首次调用较慢**：第一次对话比后续慢（API冷启动）
- **不支持视频**：目前仅支持图片和文字
- **依赖网络**：需要稳定互联网连接
- **图片大小**：建议不超过5MB

## 📄 许可证

MIT License
