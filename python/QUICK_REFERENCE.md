# AutoGen 快速参考卡片

## 🚀 5分钟快速开始

```bash
# 1. 安装依赖
cd python && uv sync --all-extras && source .venv/bin/activate

# 2. 配置环境
cp .env.example .env
# 编辑 .env 文件，填入 DASHSCOPE_API_KEY

# 3. 启动 Ollama（如需本地模型）
ollama pull qwen3:4b

# 4. 运行示例
cd quickstart && python quickstart_multi.py
```

---

## 📂 文件结构速查

```
python/
├── DEPLOYMENT.md              ← 完整部署文档
├── .env.example               ← 环境变量模板
├── .env                       ← 你的配置（不提交）
├── model_clients_registry.py  ← 模型注册中心 ⭐
└── quickstart/
    ├── quickstart_qwen.py     ← 千问云端示例
    ├── quickstart_ollama.py   ← Ollama本地示例
    └── quickstart_multi.py    ← 多模型协作 ⭐
```

---

## 🎯 常用代码片段

### 获取模型

```python
from model_clients_registry import get_model

# 云端模型（需要 API Key）
cloud_model = get_model("qwen_dashscope")

# 本地模型（无需 API Key）
local_model = get_model("ollama_qwen3")
```

### 创建 Agent

```python
from autogen_agentchat.agents import AssistantAgent

agent = AssistantAgent(
    name="MyAgent",
    model_client=get_model("qwen_dashscope"),
    system_message="你是一个有帮助的AI助手"
)
```

### 单Agent对话

```python
from autogen_agentchat.ui import Console

await Console(agent.run_stream(task="你好"))
```

### 多Agent协作

```python
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import MaxMessageTermination

team = SelectorGroupChat(
    participants=[agent1, agent2],
    model_client=get_model("qwen_dashscope"),
    termination_condition=MaxMessageTermination(max_messages=10),
)

await Console(team.run_stream(task="你的任务"))
```

---

## 🔧 配置速查

### 已注册的模型

| 名称 | 类型 | 需要API Key | 说明 |
|------|------|-------------|------|
| `qwen_dashscope` | 云端 | ✅ | 阿里千问，功能强大 |
| `ollama_qwen3` | 本地 | ❌ | Ollama本地，快速响应 |

### 环境变量

```bash
# 千问云端（必需）
DASHSCOPE_API_KEY=sk-xxx

# Ollama本地（可选）
OLLAMA_MODEL=qwen3:4b  # 默认值
OLLAMA_BASE_URL=http://localhost:11434/v1  # 默认值
```

---

## 🐛 快速故障排查

| 问题 | 解决方案 |
|------|----------|
| 端口占用 | Ollama已运行，无需重启 |
| 缺少环境变量 | 检查 `.env` 文件 |
| 模型不存在 | `ollama pull qwen3:4b` |
| 导入失败 | `uv sync --all-extras` |

---

## 📖 详细文档

完整文档请查看：**[DEPLOYMENT.md](./DEPLOYMENT.md)**

---

## ✅ 验证安装

```python
# test_setup.py
from model_clients_registry import get_model

# 测试千问
try:
    qwen = get_model("qwen_dashscope")
    print("✅ 千问云端配置成功")
except Exception as e:
    print(f"❌ 千问配置失败: {e}")

# 测试Ollama
try:
    ollama = get_model("ollama_qwen3")
    print("✅ Ollama本地配置成功")
except Exception as e:
    print(f"❌ Ollama配置失败: {e}")
```

运行：`python test_setup.py`
