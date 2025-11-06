# Cursor MCP 配置指南

## 创建配置文件

### macOS/Linux

```bash
# 创建配置目录（如果不存在）
mkdir -p ~/.cursor
# 或
mkdir -p ~/.config/cursor

# 编辑配置文件
nano ~/.cursor/mcp.json
# 或
nano ~/.config/cursor/mcp.json
```

### 配置文件内容

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

### 保存并重启 Cursor

1. 保存文件（`Ctrl+O`, `Enter`, `Ctrl+X`）
2. **完全退出 Cursor**（Cmd+Q）
3. 重新启动 Cursor

### 验证配置

重启后，在 Cursor 聊天中问：
"你能看到 wechat-article-parser 的工具吗？"

如果配置正确，AI 会告诉你它可以使用的工具。

### 使用工具

然后就可以直接使用了：
- "解析这篇文章: https://mp.weixin.qq.com/s/..."
- "提取这篇文章的元数据: https://mp.weixin.qq.com/s/..."

## 优势

- ✅ 不需要 MCP Inspector
- ✅ 不需要处理 proxy 和 token
- ✅ 不需要打开浏览器
- ✅ 直接在聊天中使用，更方便

