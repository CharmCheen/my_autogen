# 配置更新日志

## 2026-01-29 配置安全性优化

### 问题
- `model_clients_registry.py` 中硬编码了 API Key，存在安全隐患

### 改动

#### 1. 移除硬编码密钥
- 删除代码中直接写入的 API Key
- 改为从环境变量读取

#### 2. 引入 python-dotenv
- 自动加载 `.env` 文件
- 支持多路径查找（当前目录 → 上级目录）

#### 3. 新增 `.env` 文件
- 位置：`python/.env`（已被 .gitignore 排除）
- 包含你的实际 API Key 配置

#### 4. 完善 `.env.example`
- 添加详细注释说明
- 补充 OpenAI 配置示例

#### 5. 修复 quickstart 脚本
- 修正模块导入路径问题
- 更新为官方推荐的 API 用法
- 使用 `RoundRobinGroupChat` + `MaxMessageTermination` 实现多模型协作

### 使用方式

```powershell
# 激活环境
conda activate autogen
cd d:\CODE_WORLD\autogen\python

# 运行多模型协作示例
python .\quickstart\quickstart_multi.py
```

### 文件变更清单

| 文件 | 操作 |
|------|------|
| `model_clients_registry.py` | 修改 - 移除硬编码，增加 dotenv 支持 |
| `.env` | 新增 - 本地密钥配置 |
| `.env.example` | 修改 - 完善注释说明 |
| `quickstart/quickstart_multi.py` | 修改 - 使用官方 API |
| `quickstart/quickstart_qwen.py` | 修改 - 修复导入路径 |

### 已验证
- ✅ 千问（Qwen）客户端正常工作
- ⚠️ 智谱（Zhipu）账户余额不足（需充值）

### 注意事项
- `.env` 文件不会被提交到 Git，请妥善保管
- 如需更换模型，修改 `.env` 中对应的环境变量即可
