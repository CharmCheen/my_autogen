import asyncio
import sys
from pathlib import Path

# 添加父目录到路径以导入 model_clients_registry
sys.path.insert(0, str(Path(__file__).parent.parent))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.ui import Console
from model_clients_registry import get_model


async def main() -> None:
    # 加载两个不同的模型客户端
    qwen_client = get_model("qwen_dashscope")
    ollama_client = get_model("ollama_qwen3")

    # 创建两个助手 Agent，分别使用不同的模型
    # 明确各自擅长的领域，便于选择器根据任务自动分配
    assistant_qwen = AssistantAgent(
        name="QwenExpert",
        model_client=qwen_client,
        system_message="""你是千问云端专家，擅长：
        1. 深度技术分析和架构设计
        2. 复杂问题的详细解答
        3. 提供全面的理论支持和最佳实践
        适合处理需要深入研究、多维度分析的复杂任务。""",
    )
    assistant_ollama = AssistantAgent(
        name="OllamaAssistant",
        model_client=ollama_client,
        system_message="""你是本地快速助手，擅长：
        1. 快速响应简单查询
        2. 代码片段生成和调试
        3. 简洁明了的答案
        适合处理快速问答、代码辅助等轻量级任务。""",
    )

    # 设置终止条件：最多 10 条消息
    termination = MaxMessageTermination(max_messages=10)

    # 创建选择器模式的多模型协作团队
    # 系统会根据任务特点自动选择最合适的模型来响应
    team = SelectorGroupChat(
        participants=[assistant_qwen, assistant_ollama],
        model_client=qwen_client,  # 使用千问作为选择器决策模型
        termination_condition=termination,
    )

    # 运行并输出结果到控制台
    await Console(
        team.run_stream(task="列出 AutoGen 0.4 的三个亮点，并各自补充理由。")
    )


if __name__ == "__main__":
    asyncio.run(main())
