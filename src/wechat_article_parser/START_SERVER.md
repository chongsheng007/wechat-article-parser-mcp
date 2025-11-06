# 启动服务器 - 正确方式

## 问题

使用 `uv run fastmcp dev server.py` 时出现：
```
ImportError: attempted relative import with no known parent package
```

## 解决方案

### ✅ 使用新的入口文件（推荐）

已创建 `wechat_server.py` 作为入口文件，使用它启动：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev wechat_server.py
```

### ✅ 或者使用标准 MCP Inspector（不需要 fastmcp dev）

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

### ✅ 或者直接在 Cursor 中使用（最推荐）

编辑 `~/.cursor/mcp.json`:

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
        "/Users/changjp/my-first-mcp-server/src/wechat_article_parser/wechat_server.py"
      ]
    }
  }
}
```

然后重启 Cursor，在聊天中直接使用。

## 为什么需要 wechat_server.py？

`fastmcp dev` 直接运行 `server.py` 时，相对导入（`from .tools.xxx`）无法工作，因为 Python 不知道包的上下文。`wechat_server.py` 通过设置 `sys.path` 解决了这个问题。

