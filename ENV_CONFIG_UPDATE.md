# 环境变量配置更新

## ✅ 已修复的问题

### 1. API 基础 URL 配置 ✅

**之前**: 硬编码在代码中
```python
API_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
```

**现在**: 从环境变量读取，支持配置
```python
# 从环境变量 API_BASE_URL 读取，默认 https://ark.cn-beijing.volces.com/api/v3
def get_api_base_url() -> str:
    base_url = os.getenv("API_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
    return base_url

def get_images_generations_url() -> str:
    return f"{get_api_base_url()}/images/generations"
```

### 2. API Key 环境变量支持 ✅

**现在支持两种环境变量名称**:
- `SEEDREAM_API_KEY`（我们的命名）
- `ARK_API_KEY`（老师的命名，与文档一致）

代码会优先使用 `SEEDREAM_API_KEY`，如果不存在则使用 `ARK_API_KEY`。

### 3. 请求超时配置 ✅

从环境变量 `REQUEST_TIMEOUT` 读取，默认 30 秒。

## 📝 .env 文件配置

根据老师的文档，`.env` 文件应该包含：

```bash
# Seedream MCP Server 环境变量配置

# Seedream API 密钥（支持两种命名）
SEEDREAM_API_KEY=your_api_key_here
# 或者使用 ARK_API_KEY（与老师文档一致）
# ARK_API_KEY=your_api_key_here

# API 基础 URL（可选，默认为 https://ark.cn-beijing.volces.com/api/v3）
API_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# 请求超时时间(秒)
REQUEST_TIMEOUT=30
```

## 🔧 代码更新位置

1. **api_client.py**
   - ✅ `get_api_base_url()` - 从环境变量读取基础 URL
   - ✅ `get_images_generations_url()` - 动态生成端点 URL
   - ✅ 所有 API 函数都使用动态 URL

2. **所有工具文件**
   - ✅ 支持 `SEEDREAM_API_KEY` 和 `ARK_API_KEY`
   - ✅ 更新了参数描述

3. **server.py**
   - ✅ 检查环境变量时支持两种命名

4. **errors.py**
   - ✅ 错误提示更新为支持两种环境变量

## ✅ 兼容性

代码现在完全兼容老师的配置方式：
- ✅ 支持 `ARK_API_KEY` 环境变量
- ✅ 支持 `API_BASE_URL` 环境变量
- ✅ 支持 `REQUEST_TIMEOUT` 环境变量
- ✅ 同时保留 `SEEDREAM_API_KEY` 支持（向后兼容）

## 🎯 使用方式

### 方式 1: 使用 .env 文件（推荐）

创建 `.env` 文件：
```bash
ARK_API_KEY=your_api_key_here
API_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
REQUEST_TIMEOUT=30
```

### 方式 2: 系统环境变量

```bash
export ARK_API_KEY="your_api_key_here"
export API_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
export REQUEST_TIMEOUT=30
```

### 方式 3: 在 Cursor MCP 配置中

在 `~/.cursor/mcp.json` 中：
```json
{
  "seedream-image-generator": {
    "command": "uv",
    "args": ["--directory", "/Users/changjp/my-first-mcp-server", "run", "python", "/Users/changjp/my-first-mcp-server/seedream_server.py"],
    "env": {
      "ARK_API_KEY": "your_api_key_here",
      "API_BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
      "REQUEST_TIMEOUT": "30"
    }
  }
}
```

## ✅ 完成

代码已更新，现在完全匹配老师的配置方式！


