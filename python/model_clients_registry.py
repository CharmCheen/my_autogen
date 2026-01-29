"""集中管理第三方模型客户端的构造入口。

在此新增/维护各个提供商的构建函数，其他模块按需直接导入调用。

使用方式：
    1. 在 python/ 目录下创建 .env 文件（参考 .env.example）
    2. 填入对应的 API Key 和可选配置
    3. 导入并调用 get_model("模型名") 即可
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Callable, Dict

from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient

# 自动加载 .env 文件（优先当前目录，其次 python/ 根目录）
_current_dir = Path(__file__).parent
_env_locations = [
    _current_dir / ".env",          # 当前脚本同级目录
    _current_dir.parent / ".env",   # 上级目录
]
for _env_path in _env_locations:
    if _env_path.exists():
        load_dotenv(_env_path)
        break
else:
    # 未找到 .env 文件时尝试默认加载
    load_dotenv()


class MissingEnvVar(RuntimeError):
    """缺少必需环境变量时抛出的异常。"""
    pass


def _require_env(name: str) -> str:
    """获取必需的环境变量，若不存在则抛出异常。"""
    value = os.getenv(name)
    if not value:
        raise MissingEnvVar(
            f"缺少环境变量 {name}，请在 .env 文件中配置或导出到系统环境。"
        )
    return value


def build_qwen_dashscope() -> OpenAIChatCompletionClient:
    """构建阿里千问（DashScope）OpenAI 兼容客户端。

    必需环境变量:
        DASHSCOPE_API_KEY: 阿里云 DashScope API Key

    可选环境变量:
        DASHSCOPE_MODEL: 模型名称，默认 qwen-plus
        DASHSCOPE_BASE_URL: API 端点，默认官方地址
    """
    api_key = _require_env("DASHSCOPE_API_KEY")
    return OpenAIChatCompletionClient(
        model=os.getenv("DASHSCOPE_MODEL", "qwen-plus"),
        api_key=api_key,
        base_url=os.getenv(
            "DASHSCOPE_BASE_URL",
            "https://dashscope.aliyuncs.com/compatible-mode/v1",
        ),
        model_info={
            "family": "qwen",
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
            "vision": False,
        },
    )


def build_zhipu_glm() -> OpenAIChatCompletionClient:
    """构建智谱 GLM OpenAI 兼容客户端。

    必需环境变量:
        ZHIPU_API_KEY: 智谱 AI API Key

    可选环境变量:
        ZHIPU_MODEL: 模型名称，默认 glm-4-plus
        ZHIPU_BASE_URL: API 端点，默认官方地址
    """
    api_key = _require_env("ZHIPU_API_KEY")
    return OpenAIChatCompletionClient(
        model=os.getenv("ZHIPU_MODEL", "glm-4-plus"),
        api_key=api_key,
        base_url=os.getenv(
            "ZHIPU_BASE_URL",
            "https://open.bigmodel.cn/api/paas/v4/",
        ),
        model_info={
            "family": "glm",
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
            "vision": False,
        },
    )


# ============================================================================
# 模型构造注册表
# ============================================================================
# 便于在应用或测试中按名称动态获取模型客户端
MODEL_BUILDERS: Dict[str, Callable[[], OpenAIChatCompletionClient]] = {
    "qwen_dashscope": build_qwen_dashscope,
    "zhipu_glm": build_zhipu_glm,
}


def get_model(name: str) -> OpenAIChatCompletionClient:
    """根据名称获取模型客户端实例。

    Args:
        name: 模型名称，可选值见 MODEL_BUILDERS.keys()

    Returns:
        配置好的 OpenAIChatCompletionClient 实例

    Raises:
        KeyError: 未知的模型名称
        MissingEnvVar: 缺少必需的环境变量
    """
    try:
        builder = MODEL_BUILDERS[name]
    except KeyError as exc:
        raise KeyError(
            f"未知模型 '{name}'，可用选项: {sorted(MODEL_BUILDERS)}"
        ) from exc
    return builder()
