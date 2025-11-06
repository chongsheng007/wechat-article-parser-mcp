# MCP Inspector 连接错误解决方案

## 错误信息
```
Connection Error - Did you add the proxy session token in Configuration?
```

## 解决方案

### ✅ 方案 1: 刷新浏览器（最简单）

1. **硬刷新浏览器**:
   - Chrome/Edge: `Cmd+Shift+R` (Mac) 或 `Ctrl+Shift+R` (Windows)
   - Safari: `Cmd+Option+R`
   - Firefox: `Cmd+Shift+R` (Mac) 或 `Ctrl+Shift+R` (Windows)

2. **清除浏览器缓存**:
   - 打开浏览器开发者工具 (F12)
   - 右键点击刷新按钮
   - 选择 "清空缓存并硬性重新加载"

### ✅ 方案 2: 重新启动服务器

```bash
# 1. 停止服务器（在运行服务器的终端按 Ctrl+C）

# 2. 重新启动
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev server.py

# 3. 等待服务器完全启动（看到 "MCP Inspector available at..."）
# 4. 访问 http://localhost:6274
```

### ✅ 方案 3: 使用无痕模式

1. 打开浏览器的无痕/隐私模式
2. 访问 http://localhost:6274
3. 这样可以避免缓存问题

### ✅ 方案 4: 检查服务器日志

查看运行 `fastmcp dev` 的终端输出，确认：
- ✅ 服务器是否成功启动
- ✅ 是否有错误信息
- ✅ 端口是否正确（通常是 6274）

### ✅ 方案 5: 使用不同的端口

如果 6274 端口有问题：

```bash
# 停止当前服务器
pkill -f "fastmcp dev"

# 使用其他端口启动
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev server.py --port 6275
```

然后访问：http://localhost:6275

### ✅ 方案 6: 直接在 Cursor 中使用（推荐）

如果 MCP Inspector 一直有问题，可以直接在 Cursor 中使用，不需要 Inspector：

1. **配置 MCP Server**:
   - 编辑 Cursor 的 MCP 配置文件
   - 添加服务器配置

2. **重启 Cursor**

3. **在聊天中使用**:
   - "解析这篇文章: https://mp.weixin.qq.com/s/..."
   - "提取这篇文章的元数据: https://mp.weixin.qq.com/s/..."

## 验证服务器是否正常

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run python -c "from server import mcp; print('✅ 服务器正常:', mcp.name)"
```

## 常见问题

### Q: 为什么需要 proxy session token？

A: 这是 MCP Inspector 的安全机制。`fastmcp dev` 会自动处理，但如果浏览器缓存了旧的会话信息，可能会出错。

### Q: 如何确认服务器正在运行？

A: 检查：
1. 终端是否有服务器输出
2. 端口是否被占用：`lsof -i :6274`
3. 能否访问：`curl http://localhost:6274`

### Q: 可以不用 MCP Inspector 吗？

A: 可以！直接在 Cursor 中配置 MCP Server 即可，不需要 Inspector。

## 推荐操作顺序

1. **硬刷新浏览器** (Cmd+Shift+R)
2. 如果不行，**重新启动服务器**
3. 如果还不行，**使用无痕模式**
4. 如果还是不行，**直接在 Cursor 中使用**

