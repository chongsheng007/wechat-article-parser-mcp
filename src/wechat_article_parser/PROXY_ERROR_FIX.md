# MCP Inspector Proxy 错误修复

## 当前错误
```
Error Connecting to MCP Inspector Proxy - Check Console logs
连接到 MCP Inspector 代理时出错 - 检查控制台日志
```

## 问题分析

这个错误通常意味着：
1. **MCP Inspector Proxy 服务器没有运行**
2. **Proxy Session Token 需要配置**
3. **服务器地址不正确**

## 解决方案

### 方案 1: 启动 Proxy 服务器（如果使用 fastmcp dev）

`fastmcp dev` 会自动启动 proxy 服务器。确保它正在运行：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev server.py
```

在另一个终端窗口运行，不要关闭。然后：
1. 等待看到 "MCP Inspector available at http://localhost:6274"
2. 在浏览器中访问 MCP Inspector
3. 配置应该会自动填充

### 方案 2: 使用标准 MCP Inspector（不需要 Proxy）

如果 `fastmcp dev` 的 proxy 有问题，使用标准方式：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

或者手动启动：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
npx @modelcontextprotocol/inspector --transport stdio -- uv run python server.py
```

这种方式**不需要 Proxy Address 和 Proxy Session Token**，直接使用 stdio 传输。

### 方案 3: 检查浏览器控制台日志

1. 在浏览器中按 `F12` 或 `Cmd+Option+I` 打开开发者工具
2. 查看 Console（控制台）标签
3. 查看是否有详细的错误信息
4. 根据错误信息进一步排查

### 方案 4: 直接在 Cursor 中使用（最推荐）

如果 MCP Inspector 一直有问题，**直接在 Cursor 中配置**，不需要 Inspector：

1. **编辑 Cursor MCP 配置**

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

这样就不需要 MCP Inspector 了！

## 推荐操作

### 立即尝试：使用标准 MCP Inspector

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

这会使用标准方式启动，**不需要 Proxy 配置**。

### 长期方案：在 Cursor 中使用

配置 Cursor MCP，以后都在聊天中直接使用，不需要打开 Inspector。

## 检查清单

- [ ] 如果使用 fastmcp dev，确保它在运行
- [ ] 检查浏览器控制台是否有详细错误
- [ ] 尝试使用标准 MCP Inspector（不需要 Proxy）
- [ ] 或者直接在 Cursor 中配置使用

