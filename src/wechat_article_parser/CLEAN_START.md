# 清理并重新启动服务器

## 快速清理命令

如果遇到端口占用问题，运行以下命令：

```bash
# 停止所有相关进程
pkill -f "fastmcp"
pkill -f "inspector"
kill -9 $(lsof -t -i :6274) 2>/dev/null
kill -9 $(lsof -t -i :6277) 2>/dev/null

# 等待 2 秒
sleep 2

# 重新启动
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev wechat_server.py
```

## 或者使用标准 MCP Inspector（推荐）

不需要 fastmcp dev，直接使用标准方式：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

这种方式不需要 proxy 服务器，不会遇到端口冲突。

## 或者直接在 Cursor 中使用（最推荐）

不需要 MCP Inspector，直接在 Cursor 中配置：

1. 编辑 `~/.cursor/mcp.json`
2. 添加服务器配置
3. 重启 Cursor
4. 在聊天中直接使用工具

这样最简单，不需要处理端口冲突。

