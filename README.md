# Talk 2 Mag 🗣️

基于阿里云 Qwen-VL 的多模态聊天系统，支持文字和图片输入。

## ✨ 功能特点
- ✅ 纯文本对话（多轮记忆）
- ✅ 图片理解（上传即问）
- ✅ 参数调节（控制回复长度）
- ✅ 公网访问（Gradio 自动生成链接）

## 🚀 快速开始

### 环境要求
- Python 3.9+
- 阿里云账号（百炼服务 + OSS）

### 一键启动
```bash
git clone https://github.com/MaggieL12/multimodal-chat-demo.git
cd multimodal-chat-demo
pip install -r requirements.txt
python app_new.py
```
📊 性能数据
文本延迟：0.76秒
图片延迟：2.76秒
多轮对话：0.49秒
内存占用：1.7 MB

📄 详细文档
详见 [`技术说明文档.md`](技术说明文档.md)（含失败案例分析）

🔗 相关链接
- [阿里云百炼](https://www.aliyun.com/product/bailian)
- [Gradio](https://gradio.app/)
