# 端口占用问题修复

## 错误
```
❌ Proxy Server PORT IS IN USE at port 6277 ❌
```

## 解决方案

### 方案 1: 停止占用端口的进程（推荐）

```bash
# 查找占用端口的进程
lsof -i :6277

# 停止进程（替换 PID 为实际进程 ID）
kill -9 <PID>

# 或者直接停止所有 fastmcp 相关进程
pkill -f "fastmcp"
```

### 方案 2: 使用其他端口

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev wechat_server.py --port 6278
```

### 方案 3: 使用标准 MCP Inspector（不需要 fastmcp dev）

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

这种方式不需要 fastmcp dev 的 proxy 服务器，直接使用 stdio 传输。

### 方案 4: 直接在 Cursor 中使用（最推荐）

不需要 MCP Inspector，直接在 Cursor 中配置：

1. 编辑 `~/.cursor/mcp.json`
2. 添加服务器配置（使用 `wechat_server.py`）
3. 重启 Cursor
4. 在聊天中直接使用工具

## 快速清理

```bash
# 停止所有 fastmcp 和 MCP Inspector 相关进程
pkill -f "fastmcp"
pkill -f "inspector"
pkill -f "node.*627"

# 然后重新启动
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev wechat_server.py
```

