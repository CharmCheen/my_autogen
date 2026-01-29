<a name="readme-top"></a>

<div align="center">
<img src="https://microsoft.github.io/autogen/0.2/img/ag.svg" alt="AutoGen Logo" width="100">

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40pyautogen)](https://twitter.com/pyautogen)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Company?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/105812540)
[![Discord](https://img.shields.io/badge/discord-chat-green?logo=discord)](https://aka.ms/autogen-discord)
[![Documentation](https://img.shields.io/badge/Documentation-AutoGen-blue?logo=read-the-docs)](https://microsoft.github.io/autogen/)
[![Blog](https://img.shields.io/badge/Blog-AutoGen-blue?logo=blogger)](https://devblogs.microsoft.com/autogen/)

</div>

# AutoGen

**AutoGen** 是一个用于创建可自主行动或与人类协作的多 agent AI 应用的框架。

> **重要提示：** 如果您是 AutoGen 新用户，请先查看 Microsoft Agent Framework。AutoGen 将继续维护并接收错误修复与重要安全补丁。有关公告请参见仓库讨论。

## 安装

AutoGen 需要 **Python 3.10 或更高版本**。

```bash
pip install -U "autogen-agentchat" "autogen-ext[openai]"
```

如需无代码 GUI，请安装 AutoGen Studio：

```bash
pip install -U "autogenstudio"
```

## 快速开始

以下示例调用 OpenAI API，因此需先创建账号并将密钥导出为环境变量，例如 `export OPENAI_API_KEY="sk-..."`。

### Hello World

创建一个使用 OpenAI GPT-4o 模型的 assistant agent（示例略）。

### MCP 服务器

可创建一个使用 Playwright MCP 服务器的网页浏览助手。请注意仅连接受信任的 MCP 服务器，因为它们可能在本地执行命令或暴露敏感信息。

### 多 agent 编排

可使用 `AgentTool` 创建基本的多 agent 编排设置，或参考文档了解更高级用法。

## 为什么选择 AutoGen？

AutoGen 为创建 AI agents（尤其是多 agent 工作流）提供框架、开发工具和示例应用：
- `autogen-core`：实现消息传递、事件驱动 agent 和本地/分布式运行时。
- `autogen-agentchat`：面向快速原型的高级 API，支持常见模式。
- `autogen-ext`：提供第三方和第一方扩展（如 OpenAI 客户端、代码执行能力）。

开发者工具包括：
- AutoGen Studio：用于无代码构建多 agent 应用的 GUI。
- AutoGen Bench：用于评估 agent 性能的基准套件。

## 后续步骤

请参阅仓库中的 Python 与 .NET 目录以获取更多示例与开发指南。