# 最终推荐方案

## 问题总结

`fastmcp dev` 的 proxy 配置一直有问题，连接失败。

## ✅ 推荐方案：直接在 Cursor 中使用（最简单）

不需要 MCP Inspector，直接在 Cursor 中配置使用。

### 步骤 1: 创建 Cursor MCP 配置

```bash
# 创建配置目录（如果不存在）
mkdir -p ~/.cursor

# 编辑配置文件
nano ~/.cursor/mcp.json
```

### 步骤 2: 添加配置

将以下内容复制到配置文件中：

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

### 步骤 3: 保存并重启

1. 保存文件（`Ctrl+O`, `Enter`, `Ctrl+X`）
2. **完全退出 Cursor**（Cmd+Q）
3. 重新启动 Cursor

### 步骤 4: 使用

重启后，在 Cursor 聊天中直接说：
- "解析这篇文章: https://mp.weixin.qq.com/s/..."
- "提取这篇文章的元数据: https://mp.weixin.qq.com/s/..."
- "提取这篇文章的图片: https://mp.weixin.qq.com/s/..."

## 为什么推荐这个方案？

1. ✅ **最简单** - 不需要处理 proxy、token、端口
2. ✅ **最稳定** - 直接使用 stdio，不依赖 Web 服务器
3. ✅ **最实用** - 实际使用场景就是这样的
4. ✅ **最快速** - 不需要打开浏览器

## 如果还是想用 MCP Inspector

使用标准方式（不需要 proxy）：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

然后在打开的页面中配置：
- Transport Type: STDIO
- Command: uv
- Arguments: `run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python wechat_server.py`
- **不需要** Inspector Proxy Address
- **不需要** Proxy Session Token

直接点击 Connect 即可！

