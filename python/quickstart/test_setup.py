"""
配置验证脚本
用于检查 AutoGen 环境和模型配置是否正确
"""
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """测试基础导入"""
    print("🔍 检查基础导入...")
    try:
        from autogen_agentchat.agents import AssistantAgent
        from autogen_agentchat.teams import SelectorGroupChat, RoundRobinGroupChat
        from autogen_agentchat.conditions import MaxMessageTermination
        from autogen_agentchat.ui import Console
        print("✅ 基础模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("💡 提示: 运行 'uv sync --all-extras' 安装依赖")
        return False


def test_registry():
    """测试模型注册中心"""
    print("\n🔍 检查模型注册中心...")
    try:
        from model_clients_registry import get_model, MODEL_BUILDERS
        print(f"✅ 模型注册中心加载成功")
        print(f"📋 已注册的模型: {list(MODEL_BUILDERS.keys())}")
        return True
    except ImportError as e:
        print(f"❌ 无法导入 model_clients_registry: {e}")
        return False


def test_qwen_config():
    """测试千问云端配置"""
    print("\n🔍 检查千问云端模型配置...")
    try:
        from model_clients_registry import get_model
        client = get_model("qwen_dashscope")
        print("✅ 千问云端模型配置成功")
        print(f"   模型: {client.model}")
        return True
    except Exception as e:
        print(f"❌ 千问配置失败: {e}")
        print("💡 提示: 检查 .env 文件中的 DASHSCOPE_API_KEY")
        return False


def test_ollama_config():
    """测试 Ollama 本地模型配置"""
    print("\n🔍 检查 Ollama 本地模型配置...")
    try:
        from model_clients_registry import get_model
        client = get_model("ollama_qwen3")
        print("✅ Ollama 本地模型配置成功")
        print(f"   模型: {client.model}")
        print(f"   端点: {client.base_url}")
        return True
    except Exception as e:
        print(f"❌ Ollama 配置失败: {e}")
        print("💡 提示: 确保 Ollama 服务正在运行，并已安装 qwen3:4b 模型")
        print("   运行: ollama pull qwen3:4b")
        return False


def test_ollama_connection():
    """测试 Ollama 服务连接"""
    print("\n🔍 检查 Ollama 服务连接...")
    try:
        import httpx
        response = httpx.get("http://localhost:11434")
        if response.status_code == 200:
            print("✅ Ollama 服务运行正常")
            return True
        else:
            print(f"⚠️ Ollama 服务响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到 Ollama 服务: {e}")
        print("💡 提示: 确保 Ollama 已安装并正在运行")
        print("   访问 https://ollama.ai 下载安装")
        return False


def test_env_file():
    """检查 .env 文件"""
    print("\n🔍 检查环境配置文件...")
    env_path = Path(__file__).parent.parent / ".env"
    env_example_path = Path(__file__).parent.parent / ".env.example"
    
    if env_path.exists():
        print("✅ .env 文件存在")
        # 读取并检查关键配置
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'DASHSCOPE_API_KEY' in content and 'your_dashscope_api_key' not in content:
                print("✅ DASHSCOPE_API_KEY 已配置")
            else:
                print("⚠️ DASHSCOPE_API_KEY 未配置或使用默认值")
        return True
    else:
        print("❌ .env 文件不存在")
        if env_example_path.exists():
            print(f"💡 提示: 复制 .env.example 为 .env")
            print(f"   运行: cp {env_example_path} {env_path}")
        return False


def main():
    """运行所有测试"""
    print("=" * 70)
    print("AutoGen 环境配置验证")
    print("=" * 70)
    
    results = {
        "基础导入": test_imports(),
        "模型注册中心": test_registry(),
        "环境配置文件": test_env_file(),
        "千问云端": test_qwen_config(),
        "Ollama配置": test_ollama_config(),
        "Ollama连接": test_ollama_connection(),
    }
    
    print("\n" + "=" * 70)
    print("验证结果汇总")
    print("=" * 70)
    
    for name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\n通过: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 所有检查通过！你的环境配置完美！")
        print("📝 可以开始使用 quickstart 示例了")
    elif passed >= total - 2:
        print("\n⚠️ 大部分检查通过，有少量问题")
        print("📝 可以开始使用，但建议修复上述问题")
    else:
        print("\n❌ 发现多个配置问题，请先解决")
        print("📖 详细文档: DEPLOYMENT.md")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
