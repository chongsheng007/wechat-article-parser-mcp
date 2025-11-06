# 快速启动指南（已修复）

## ✅ 正确的启动命令

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev wechat_server.py
```

**重要**: 使用 `wechat_server.py` 而不是 `server.py`！

## 为什么？

`server.py` 使用相对导入（`from .tools.xxx`），当 `fastmcp dev` 直接运行时会出现导入错误。`wechat_server.py` 通过设置 `sys.path` 解决了这个问题。

## 其他启动方式

### 方式 1: 使用启动脚本

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

### 方式 2: 直接在 Cursor 中使用（最推荐）

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

重启 Cursor，在聊天中直接使用工具。

## 验证服务器运行

访问：http://localhost:6274

如果看到 MCP Inspector 界面，说明服务器运行正常。

