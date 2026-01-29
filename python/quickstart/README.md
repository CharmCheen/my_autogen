# Quickstart

本示例演示如何使用集中注册的模型客户端快速跑通单模型与多模型协作。

## 准备环境（Windows PowerShell）

```powershell
cd d:\CODE_WORLD\autogen\python
uv sync --all-extras
.\.venv\Scripts\Activate.ps1
```

> 首次 `uv sync` 需数分钟，请耐心等待。

## 设置密钥与可选参数

- 阿里千问（DashScope）：

```powershell
$env:DASHSCOPE_API_KEY="你的千问Key"
# 可选覆盖
$env:DASHSCOPE_MODEL="qwen2.5-72b-instruct"
$env:DASHSCOPE_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
```

- 智谱 AI（GLM）：

```powershell
$env:ZHIPU_API_KEY="你的智谱Key"
# 可选覆盖
$env:ZHIPU_MODEL="glm-4-plus"
$env:ZHIPU_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
```

也可参考根目录的 `.env.example` 内容，将变量写入你自己的环境管理工具。

## 运行单模型示例（千问）

```powershell
python .\quickstart\quickstart_qwen.py
```

## 运行多模型协作示例（千问 + 智谱）

```powershell
python .\quickstart\quickstart_multi.py
```

## 常见问题

- 401/403：检查 API Key 是否正确、是否对所选模型有调用权限。
- 能力差异：若模型不支持函数调用或结构化输出，可在 `model_clients_registry.py` 中将对应能力设为 `False`。
- 网络/时延：首次调用可能有网络波动，请重试或更换网络环境。
- 版本更新：如官方端点（base_url）有更新，请同步修改环境变量或注册表文件。
