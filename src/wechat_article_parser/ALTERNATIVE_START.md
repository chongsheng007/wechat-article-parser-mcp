# MCP Inspector 替代启动方式

## 问题
使用 `fastmcp dev` 时出现 "Connection Error - Did you add the proxy session token in Configuration?"

## 解决方案：使用标准 MCP Inspector

### 方式 1: 使用 npx 直接启动（推荐）

在**两个终端**中分别运行：

#### 终端 1: 启动服务器
```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run python server.py
```

#### 终端 2: 启动 MCP Inspector
```bash
npx @modelcontextprotocol/inspector --transport stdio -- uv run python /Users/changjp/my-first-mcp-server/src/wechat_article_parser/server.py
```

### 方式 2: 使用完整路径启动

```bash
cd /Users/changjp/my-first-mcp-server
npx @modelcontextprotocol/inspector --transport stdio -- uv run --directory src/wechat_article_parser python src/wechat_article_parser/server.py
```

### 方式 3: 直接在 Cursor 中使用（最简单）

如果 MCP Inspector 一直有问题，可以直接在 Cursor 中配置和使用，不需要 Inspector。

1. **创建 Cursor MCP 配置**

编辑 `~/.cursor/mcp.json` 或 `~/.config/cursor/mcp.json`:

```json
{
  "mcpServers": {
    "wechat-article-parser": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/changjp/my-first-mcp-server/src/wechat_article_parser",
        "python",
        "/Users/changjp/my-first-mcp-server/src/wechat_article_parser/server.py"
      ]
    }
  }
}
```

2. **重启 Cursor**

3. **在聊天中使用**
   - "解析这篇文章: https://mp.weixin.qq.com/s/..."
   - "提取这篇文章的元数据: https://mp.weixin.qq.com/s/..."

## 验证服务器正常工作

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run python -c "import sys; sys.path.insert(0, '.'); from server import mcp; print('✅ Server:', mcp.name)"
```

## 为什么 fastmcp dev 会有问题？

`fastmcp dev` 在某些情况下可能需要额外的配置或特定版本。使用标准的 `npx @modelcontextprotocol/inspector` 更可靠。

