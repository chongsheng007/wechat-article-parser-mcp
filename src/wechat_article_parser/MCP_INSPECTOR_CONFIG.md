# MCP Inspector 正确配置

## 根据你的截图，正确的配置应该是：

### 配置参数

```
Transport Type: STDIO
Command: uv
Arguments: run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python server.py
```

### 详细步骤

1. **Transport Type**: 保持 "STDIO"

2. **Command**: 保持 "uv"

3. **Arguments**: 修改为：
   ```
   run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python server.py
   ```

4. **展开 Configuration 章节**:
   - 点击 "> Configuration" 展开
   - 如果有 "Proxy Session Token" 字段，可以尝试留空
   - 或者查看是否有其他必需配置

5. **展开 Environment Variables** (如果需要):
   - 通常不需要，除非服务器需要特定的环境变量

6. **点击 Connect 按钮**

## 如果还是出错

### 方案 1: 使用启动脚本（推荐）

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

这会自动使用正确的配置启动。

### 方案 2: 直接在 Cursor 中使用（最推荐）

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
        "/Users/changjp/my-first-mcp-server/src/wechat_article_parser/server.py"
      ]
    }
  }
}
```

然后重启 Cursor，在聊天中直接使用工具，不需要 MCP Inspector！

