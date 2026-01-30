# AutoGen 本地部署与配置指南

本文档提供完整的 AutoGen 本地部署、模型配置和使用指南。

---

## 📋 目录

- [环境配置](#环境配置)
- [模型配置中心](#模型配置中心)
- [快速开始示例](#快速开始示例)
- [多模型协作模式](#多模型协作模式)
- [故障排查](#故障排查)

---

## 🛠️ 环境配置

### 1. 安装依赖

```bash
# 安装 uv 包管理器（如果还没有）
pip install uv

# 进入 python 目录并安装所有依赖
cd python
uv sync --all-extras
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows
```

### 2. 配置环境变量

在 `python/` 目录下创建 `.env` 文件：

```bash
# python/.env

# =============================================================================
# 阿里千问（DashScope）云端模型配置
# =============================================================================
DASHSCOPE_API_KEY=your_dashscope_api_key_here
# DASHSCOPE_MODEL=qwen-plus                    # 可选，默认 qwen-plus
# DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# =============================================================================
# Ollama 本地模型配置（无需 API Key）
# =============================================================================
# OLLAMA_MODEL=qwen3:4b                        # 可选，默认 qwen3:4b
# OLLAMA_BASE_URL=http://localhost:11434/v1   # 可选，默认本地地址
```

### 3. 启动 Ollama 服务

```bash
# 拉取模型（首次使用）
ollama pull qwen3:4b

# Ollama 通常会自动在后台运行
# 检查是否运行：访问 http://localhost:11434 应该返回 "Ollama is running"
```

---

## 🎯 模型配置中心

### 配置文件位置

```
python/
├── model_clients_registry.py    ← 模型注册中心（核心配置文件）
├── .env                          ← 环境变量配置
└── quickstart/
    ├── quickstart_qwen.py        ← 单模型示例（千问云端）
    ├── quickstart_ollama.py      ← 单模型示例（Ollama本地）
    ├── quickstart_multi.py       ← 多模型协作示例
    └── quickstart_selector_demo.py ← 选择器模式测试
```

### 已注册的模型接口

在 `model_clients_registry.py` 中已配置以下模型：

| 模型名称 | 函数 | 类型 | API Key | 说明 |
|---------|------|------|---------|------|
| `qwen_dashscope` | `build_qwen_dashscope()` | 云端 | ✅ 必需 | 阿里千问云端模型，功能强大 |
| `ollama_qwen3` | `build_ollama_qwen3()` | 本地 | ❌ 不需要 | Ollama本地模型，快速响应 |

### 如何新增模型

编辑 `model_clients_registry.py`：

```python
# 1. 定义构建函数
def build_your_model() -> OpenAIChatCompletionClient:
    """构建你的模型客户端"""
    return OpenAIChatCompletionClient(
        model=os.getenv("YOUR_MODEL_NAME", "default-model"),
        api_key=_require_env("YOUR_API_KEY"),  # 或 "ollama" 如果是本地
        base_url=os.getenv("YOUR_BASE_URL", "https://api.example.com/v1"),
        model_info={
            "family": "your_model_family",
            "function_calling": True,    # 是否支持函数调用
            "json_output": True,         # 是否支持JSON输出
            "structured_output": True,   # 是否支持结构化输出
            "vision": False,             # 是否支持视觉理解
        },
    )

# 2. 注册到模型构造表
MODEL_BUILDERS: Dict[str, Callable[[], OpenAIChatCompletionClient]] = {
    "qwen_dashscope": build_qwen_dashscope,
    "ollama_qwen3": build_ollama_qwen3,
    "your_model": build_your_model,  # ← 新增这一行
}
```

### 使用模型

```python
from model_clients_registry import get_model

# 获取模型客户端
client = get_model("qwen_dashscope")  # 或 "ollama_qwen3"

# 使用模型创建 Agent
from autogen_agentchat.agents import AssistantAgent

agent = AssistantAgent(
    name="Assistant",
    model_client=client,
    system_message="你的系统提示词"
)
```

---

## 🚀 快速开始示例

### 示例 1：单模型对话（千问云端）

```bash
cd python/quickstart
python quickstart_qwen.py
```

**代码结构**：
```python
from model_clients_registry import get_model

# 获取千问模型
client = get_model("qwen_dashscope")

# 创建 Agent
agent = AssistantAgent(
    name="Assistant",
    model_client=client,
    system_message="你是一个有帮助的AI助手。"
)

# 运行对话
await Console(agent.run_stream(task="你好"))
```

### 示例 2：单模型对话（Ollama本地）

```bash
cd python/quickstart
python quickstart_ollama.py
```

**特点**：无需网络，完全本地运行，速度快

### 示例 3：多模型协作（选择器模式）

```bash
cd python/quickstart
python quickstart_multi.py
```

**核心代码**：
```python
from autogen_agentchat.teams import SelectorGroupChat

# 创建多个 Agent
qwen_agent = AssistantAgent(
    name="CloudExpert",
    model_client=get_model("qwen_dashscope"),
    system_message="擅长深度技术分析..."
)

ollama_agent = AssistantAgent(
    name="QuickHelper",
    model_client=get_model("ollama_qwen3"),
    system_message="擅长快速响应..."
)

# 创建选择器团队
team = SelectorGroupChat(
    participants=[qwen_agent, ollama_agent],
    model_client=get_model("qwen_dashscope"),  # 选择器使用的模型
    termination_condition=MaxMessageTermination(max_messages=10),
)

# 运行任务
await Console(team.run_stream(task="你的问题"))
```

---

## 🤝 多模型协作模式

### 1. RoundRobinGroupChat（轮询模式）

**特点**：固定顺序轮流发言
**适用场景**：需要多个视角轮流讨论的场景

```python
from autogen_agentchat.teams import RoundRobinGroupChat

team = RoundRobinGroupChat(
    participants=[agent1, agent2],
    termination_condition=MaxMessageTermination(max_messages=6),
)
```

### 2. SelectorGroupChat（选择器模式）

**特点**：根据任务自动选择最合适的 Agent
**适用场景**：不同 Agent 有明确分工，需要智能调度

```python
from autogen_agentchat.teams import SelectorGroupChat

team = SelectorGroupChat(
    participants=[cloud_expert, local_helper],
    model_client=selector_model,  # 用于决策的模型
    termination_condition=MaxMessageTermination(max_messages=10),
)
```

**优化建议**：
- 给每个 Agent 明确的 `system_message`，描述其擅长领域
- 选择器模型使用更强大的模型（如千问云端）
- 设计明确的任务类型来触发不同的 Agent

### 3. 自定义团队模式

可以继承 `BaseGroupChat` 实现自定义调度逻辑。

---

## 🔧 配置参考

### Agent 配置

```python
agent = AssistantAgent(
    name="AgentName",              # Agent 名称（唯一标识）
    model_client=client,           # 模型客户端
    system_message="...",          # 系统提示词（定义角色和能力）
    description="...",             # Agent 描述（可选）
)
```

### 终止条件配置

```python
from autogen_agentchat.conditions import (
    MaxMessageTermination,         # 最大消息数
    TextMentionTermination,        # 特定文本出现
    TimeoutTermination,            # 超时
)

# 最大消息数终止
termination = MaxMessageTermination(max_messages=10)

# 文本触发终止
termination = TextMentionTermination(text="TERMINATE")

# 多条件组合
from autogen_agentchat.conditions import AndTermination, OrTermination

termination = OrTermination([
    MaxMessageTermination(max_messages=20),
    TextMentionTermination(text="DONE"),
])
```

### 模型参数配置

在 `.env` 文件中可以配置的参数：

```bash
# 千问云端
DASHSCOPE_API_KEY=sk-xxx           # 必需
DASHSCOPE_MODEL=qwen-plus          # 可选模型：qwen-plus, qwen-max, qwen-turbo
DASHSCOPE_BASE_URL=...             # 可选，默认官方地址

# Ollama 本地
OLLAMA_MODEL=qwen3:4b              # 可选模型：qwen3:4b, llama2, mistral 等
OLLAMA_BASE_URL=http://localhost:11434/v1  # 可选，默认本地地址
```

---

## 🐛 故障排查

### 问题 1：Ollama 端口占用

**错误信息**：
```
Error: listen tcp 127.0.0.1:11434: bind: Only one usage of each socket address...
```

**解决方案**：说明 Ollama 已经在运行，无需重复启动

**验证**：访问 http://localhost:11434 应该返回 "Ollama is running"

### 问题 2：缺少环境变量

**错误信息**：
```
MissingEnvVar: 缺少环境变量 DASHSCOPE_API_KEY...
```

**解决方案**：
1. 确认 `python/.env` 文件存在
2. 检查文件中是否有对应的配置项
3. 重新激活虚拟环境

### 问题 3：模型不存在

**错误信息**：
```
KeyError: 未知模型 'xxx'，可用选项: ['qwen_dashscope', 'ollama_qwen3']
```

**解决方案**：
- 检查 `model_clients_registry.py` 中的 `MODEL_BUILDERS`
- 确认模型名称拼写正确
- 如需新模型，参考"如何新增模型"章节

### 问题 4：Ollama 模型未安装

**错误信息**：连接到 Ollama 但返回模型不存在

**解决方案**：
```bash
# 查看已安装模型
ollama list

# 安装需要的模型
ollama pull qwen3:4b
```

### 问题 5：虚拟环境问题

**症状**：导入模块失败

**解决方案**：
```bash
# 重新同步环境
cd python
uv sync --all-extras
source .venv/bin/activate  # 或 .venv\Scripts\activate (Windows)
```

---

## 📚 高级配置

### 日志配置

```python
import logging

# 设置日志级别
logging.basicConfig(level=logging.INFO)

# 查看详细的 HTTP 请求日志
logging.getLogger("autogen_ext.models.openai").setLevel(logging.DEBUG)
```

### 代理配置

如果需要通过代理访问云端模型：

```python
# 在 model_clients_registry.py 中添加
import os

def build_qwen_dashscope() -> OpenAIChatCompletionClient:
    return OpenAIChatCompletionClient(
        model=os.getenv("DASHSCOPE_MODEL", "qwen-plus"),
        api_key=_require_env("DASHSCOPE_API_KEY"),
        base_url=os.getenv("DASHSCOPE_BASE_URL", "..."),
        # 添加代理配置
        http_client=httpx.Client(
            proxies=os.getenv("HTTP_PROXY"),
            timeout=30.0,
        ),
    )
```

### 重试策略

```python
# 在创建 OpenAIChatCompletionClient 时可以配置重试
client = OpenAIChatCompletionClient(
    model="qwen-plus",
    api_key="...",
    base_url="...",
    max_retries=3,           # 最大重试次数
    timeout=60.0,            # 超时时间（秒）
)
```

---

## 📞 获取帮助

- **官方文档**：https://microsoft.github.io/autogen/
- **GitHub Issues**：https://github.com/microsoft/autogen/issues
- **Discord 社区**：https://discord.gg/pAbnFJrkgZ

---

## 🔄 版本信息

- **AutoGen 版本**：0.4.x
- **Python 版本**：3.10+
- **文档更新日期**：2026-01-30

---

## ✅ 检查清单

部署前确认：

- [ ] 已安装 `uv` 并同步依赖
- [ ] 已创建 `.env` 文件并配置 API Key
- [ ] Ollama 服务正常运行（如需使用本地模型）
- [ ] 已拉取所需的 Ollama 模型
- [ ] 能够成功导入 `from model_clients_registry import get_model`
- [ ] 运行 `quickstart_qwen.py` 或 `quickstart_ollama.py` 验证配置

---

**提示**：建议将本文档和 `.env.example` 文件一起提交到版本控制，但 `.env` 文件应该在 `.gitignore` 中排除。
