# 最佳解决方案：使用标准 MCP Inspector

## 问题

`fastmcp dev` 的 proxy 配置一直有问题，连接失败。

## ✅ 推荐解决方案：使用标准 MCP Inspector（不需要 proxy）

这种方式不需要 proxy 和 token，直接使用 stdio 传输，更简单可靠。

### 启动步骤

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

或者手动启动：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
npx @modelcontextprotocol/inspector --transport stdio -- uv run python wechat_server.py
```

### 配置

启动后，在打开的 MCP Inspector 中：

- **Transport Type**: `STDIO` ✅
- **Command**: `uv` ✅
- **Arguments**: `run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python wechat_server.py` ✅
- **不需要** Inspector Proxy Address（留空）
- **不需要** Proxy Session Token（留空）

直接点击 Connect 即可！

## ✅ 最推荐：直接在 Cursor 中使用

如果 MCP Inspector 一直有问题，**直接在 Cursor 中配置**，最简单：

### 1. 创建/编辑 Cursor MCP 配置

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
        "/Users/changjp/my-first-mcp-server/src/wechat_article_parser/wechat_server.py"
      ]
    }
  }
}
```

### 2. 重启 Cursor

完全退出并重新启动 Cursor。

### 3. 在聊天中使用

重启后，在 Cursor 聊天中直接说：
- "解析这篇文章: https://mp.weixin.qq.com/s/..."
- "提取这篇文章的元数据: https://mp.weixin.qq.com/s/..."
- "提取这篇文章的图片: https://mp.weixin.qq.com/s/..."

这样就不需要 MCP Inspector 了！

## 为什么推荐 Cursor 直接使用？

1. ✅ **更简单** - 不需要处理 proxy、token、端口等复杂配置
2. ✅ **更稳定** - 直接使用 stdio，不依赖 Web 服务器
3. ✅ **更实用** - 实际使用场景就是这样的
4. ✅ **更快速** - 不需要打开浏览器

