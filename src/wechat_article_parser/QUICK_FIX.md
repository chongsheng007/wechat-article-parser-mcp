# MCP Inspector 连接错误快速修复

## 错误
```
Connection Error - Did you add the proxy session token in Configuration?
```

## 快速修复步骤

### 1. 停止所有相关进程
```bash
pkill -f "fastmcp"
pkill -f "server.py"
```

### 2. 重新启动服务器
```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev server.py
```

### 3. 等待服务器启动
等待看到类似输出：
```
INFO: Starting MCP server 'WeChat Article Parser'...
INFO: MCP Inspector available at http://localhost:6274
```

### 4. 访问 MCP Inspector
打开浏览器访问：**http://localhost:6274**

## 如果还是有问题

### 方案 A: 检查端口
```bash
# 检查端口是否被占用
lsof -i :6274

# 如果被占用，使用其他端口
uv run fastmcp dev server.py --port 6275
```

### 方案 B: 使用标准 MCP Inspector
```bash
# 终端 1: 启动服务器
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run python server.py

# 终端 2: 启动 Inspector
npx @modelcontextprotocol/inspector --transport stdio -- uv run python /Users/changjp/my-first-mcp-server/src/wechat_article_parser/server.py
```

### 方案 C: 直接在 Cursor 中使用（推荐）
不需要 MCP Inspector，直接在 Cursor 中配置 MCP Server：

1. 编辑 Cursor MCP 配置
2. 添加服务器配置
3. 重启 Cursor
4. 在聊天中直接使用工具

## 验证服务器工作

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run python -c "from server import mcp; print('✅ Server loaded:', mcp.name)"
```

