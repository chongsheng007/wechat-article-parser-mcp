# MCP Inspector 连接错误最终解决方案

## 问题
使用 `fastmcp dev` 时出现：
```
Connection Error - Did you add the proxy session token in Configuration?
```

## ✅ 推荐解决方案：使用标准 MCP Inspector

### 方法 1: 使用启动脚本（最简单）

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

这会使用标准的 MCP Inspector 启动，避免 `fastmcp dev` 的配置问题。

### 方法 2: 手动启动

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
npx @modelcontextprotocol/inspector --transport stdio -- uv run python server.py
```

### 方法 3: 直接在 Cursor 中使用（最推荐）

如果 MCP Inspector 一直有问题，**直接在 Cursor 中使用**，不需要 Inspector：

#### 步骤 1: 创建 Cursor MCP 配置

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

#### 步骤 2: 重启 Cursor

完全退出并重新启动 Cursor。

#### 步骤 3: 在聊天中使用

重启后，在 Cursor 聊天中直接说：
- "解析这篇文章: https://mp.weixin.qq.com/s/..."
- "提取这篇文章的元数据: https://mp.weixin.qq.com/s/..."
- "提取这篇文章的图片: https://mp.weixin.qq.com/s/..."

Cursor 会自动调用相应的工具，无需 MCP Inspector！

## 为什么推荐在 Cursor 中使用？

1. ✅ **更简单** - 不需要单独的 Inspector 界面
2. ✅ **更直接** - 在聊天中直接使用工具
3. ✅ **更稳定** - 避免 Inspector 的连接问题
4. ✅ **更实用** - 实际使用场景就是这样的

## 验证配置

配置完成后，在 Cursor 中问：
"你能看到 wechat-article-parser 的工具吗？"

如果配置正确，AI 会告诉你它可以使用哪些工具。

## 测试工具

配置完成后，可以测试：

```
解析这篇文章并提取元数据: https://mp.weixin.qq.com/s/your-article-url
```

## 总结

- **开发/调试**: 使用 `start_inspector.sh` 或标准 MCP Inspector
- **日常使用**: 直接在 Cursor 中配置和使用（推荐）

