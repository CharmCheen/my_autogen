import asyncio
import sys
from pathlib import Path

# 添加父目录到路径以导入 model_clients_registry
sys.path.insert(0, str(Path(__file__).parent.parent))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.ui import Console
from model_clients_registry import get_model


async def main() -> None:
    # 加载两个不同的模型客户端
    qwen_client = get_model("qwen_dashscope")
    zhipu_client = get_model("zhipu_glm")

    # 创建两个助手 Agent，分别使用不同的模型
    assistant_qwen = AssistantAgent(
        name="Qwen",
        model_client=qwen_client,
        system_message="你是千问助手，擅长提供深入分析和补充细节。",
    )
    assistant_zhipu = AssistantAgent(
        name="Zhipu",
        model_client=zhipu_client,
        system_message="你是智谱助手，擅长总结归纳和提出不同视角。",
    )

    # 设置终止条件：最多 6 条消息
    termination = MaxMessageTermination(max_messages=6)

    # 创建轮询式多模型协作团队
    team = RoundRobinGroupChat(
        participants=[assistant_qwen, assistant_zhipu],
        termination_condition=termination,
    )

    # 运行并输出结果到控制台
    await Console(
        team.run_stream(task="列出 AutoGen 0.4 的三个亮点，并各自补充理由。")
    )


if __name__ == "__main__":
    asyncio.run(main())
