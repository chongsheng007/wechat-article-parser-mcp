# MCP Inspector 连接错误修复

## 错误信息
```
Connection Error - Did you add the proxy session token in Configuration?
```

## 问题原因

这个错误通常是因为：
1. MCP Inspector 需要特定的会话令牌
2. FastMCP dev 模式配置问题
3. 服务器未正确启动

## 解决方案

### 方案 1: 检查服务器是否正在运行

```bash
# 停止当前服务器（如果有）
pkill -f "fastmcp dev"

# 重新启动服务器
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev server.py
```

### 方案 2: 使用正确的启动方式

确保使用完整的路径：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev server.py
```

### 方案 3: 检查端口占用

```bash
# 检查端口 6274 是否被占用
lsof -i :6274

# 如果被占用，杀死进程
kill -9 <PID>
```

### 方案 4: 使用 npx 直接启动 MCP Inspector

如果 `fastmcp dev` 有问题，可以手动启动：

```bash
# 终端 1: 启动服务器
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run python server.py

# 终端 2: 启动 MCP Inspector
npx @modelcontextprotocol/inspector --transport stdio -- uv run python /Users/changjp/my-first-mcp-server/src/wechat_article_parser/server.py
```

### 方案 5: 检查 FastMCP 版本

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run python -c "import fastmcp; print(fastmcp.__version__)"
```

## 推荐解决方案

### 步骤 1: 停止所有相关进程

```bash
pkill -f "fastmcp"
pkill -f "server.py"
```

### 步骤 2: 重新启动服务器

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev server.py
```

### 步骤 3: 等待服务器启动

服务器启动后，你应该看到类似输出：
```
INFO: Starting MCP server 'WeChat Article Parser' with transport 'stdio'
INFO: MCP Inspector available at http://localhost:6274
```

### 步骤 4: 访问 MCP Inspector

打开浏览器访问：http://localhost:6274

## 如果仍然有问题

### 检查服务器日志

查看终端输出，确认：
- ✅ 服务器是否成功启动
- ✅ 是否有错误信息
- ✅ 端口是否正确

### 尝试不同的端口

如果 6274 端口有问题，可以尝试：

```bash
# 使用环境变量指定端口
export MCP_PORT=6275
uv run fastmcp dev server.py --port 6275
```

### 使用标准 MCP Inspector

```bash
npx @modelcontextprotocol/inspector --transport stdio -- uv run python /Users/changjp/my-first-mcp-server/src/wechat_article_parser/server.py
```

## 验证服务器工作

测试服务器是否正常工作：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run python -c "from server import mcp; print('✅ Server loaded:', mcp.name)"
```

## 常见问题

### Q: 为什么需要代理会话令牌？

A: 这是 MCP Inspector 的安全机制。如果使用 `fastmcp dev`，它会自动处理。如果手动启动，可能需要额外配置。

### Q: 可以直接在 Cursor 中使用吗？

A: 可以！配置 MCP Server 到 Cursor 后，不需要 MCP Inspector，可以直接在聊天中使用工具。

