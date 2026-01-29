import asyncio
import sys
from pathlib import Path

# 添加父目录到路径以导入 model_clients_registry
sys.path.insert(0, str(Path(__file__).parent.parent))

from autogen_core.models import UserMessage
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from model_clients_registry import get_model


async def main() -> None:
    client = get_model("qwen_dashscope")
    assistant = AssistantAgent("qwen", model_client=client)
    user = UserProxyAgent("user")

    result = await assistant.run(
        messages=[UserMessage(content="用一句话介绍 AutoGen 0.4 的核心目标")],
        sender=user,
    )
    print(result.content)


if __name__ == "__main__":
    asyncio.run(main())
