# Inspector Proxy Address 配置说明

## 重要说明

**Inspector Proxy Address 不是用来在浏览器中打开的！**

- **端口 6274**: MCP Inspector 的 Web UI（在浏览器中访问）
- **端口 6277**: Proxy 服务器（用于 API 调用，不用于浏览器访问）

## 正确的配置

### 在浏览器中访问

访问：**http://localhost:6274**（带 token 的完整 URL）

```
http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017
```

### 在 MCP Inspector 配置中

**Inspector Proxy Address** 字段应该填写：
```
http://localhost:6277
```

这个地址是给 MCP Inspector 内部使用的，不是让你在浏览器中打开的。

## 如果端口 6277 无法访问

这是正常的！端口 6277 是 API 端点，不是 Web 页面。

### 检查服务器是否运行

```bash
# 检查进程
ps aux | grep "fastmcp dev"

# 检查端口
lsof -i :6277
lsof -i :6274
```

### 如果服务器没有运行

重新启动：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev wechat_server.py
```

## 正确的使用流程

1. **启动服务器**（在终端）:
   ```bash
   uv run fastmcp dev wechat_server.py
   ```

2. **在浏览器中访问**（使用完整 URL）:
   ```
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=你的token
   ```

3. **在 MCP Inspector 中配置**:
   - Transport Type: STDIO
   - Command: uv
   - Arguments: `run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python wechat_server.py`
   - Inspector Proxy Address: `http://localhost:6277`
   - Proxy Session Token: `你的token`
   - 点击 Connect

## 如果还是不行

### 使用标准 MCP Inspector（不需要 proxy）

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

### 或者直接在 Cursor 中使用（最推荐）

不需要 MCP Inspector，直接在 Cursor 中配置使用。

