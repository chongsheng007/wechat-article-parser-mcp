# 端口说明 - 重要！

## 两个不同的端口

### 端口 6274 - Web UI（在浏览器中访问）

**用途**: MCP Inspector 的 Web 界面

**访问方式**: 在浏览器中打开
```
http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=你的token
```

**这是你看到的界面**，用于配置和测试工具。

### 端口 6277 - API Proxy（不用于浏览器访问）

**用途**: Proxy 服务器的 API 端点

**使用方式**: 
- **不在浏览器中打开**
- 在 MCP Inspector 的配置中填写：`http://localhost:6277`
- 这是给 MCP Inspector 内部使用的，不是 Web 页面

## 正确的配置步骤

### 1. 启动服务器

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev wechat_server.py
```

等待看到：
```
🚀 MCP Inspector is up and running at:
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=...
```

### 2. 在浏览器中访问

**复制完整 URL**（包含 token）到浏览器，例如：
```
http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017
```

### 3. 在 MCP Inspector 中配置

- **Inspector Proxy Address**: `http://localhost:6277`
  - ⚠️ 这个地址是给系统用的，**不要**在浏览器中打开
  - 只需要在配置字段中填写即可

- **Proxy Session Token**: 填入服务器给出的 token

## 常见错误

❌ **错误**: 试图在浏览器中打开 `http://localhost:6277`
✅ **正确**: 在配置字段中填写 `http://localhost:6277`，浏览器访问 `http://localhost:6274`

## 如果服务器没有运行

检查并重新启动：

```bash
# 检查进程
ps aux | grep "fastmcp dev"

# 如果没有，重新启动
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev wechat_server.py
```

