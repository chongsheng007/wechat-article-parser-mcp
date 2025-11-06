# Session Token 配置指南

## 服务器已启动

服务器成功启动，并生成了 session token：
```
Session token: 06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017
```

## 解决方案

### 方案 1: 使用带 Token 的 URL（推荐）

服务器已经给出了带 token 的 URL：
```
http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017
```

**直接复制这个完整 URL 到浏览器访问**，不要使用手动配置的 MCP Inspector。

### 方案 2: 在 MCP Inspector 配置中添加 Token

如果你在 MCP Inspector 中手动配置：

1. **展开 "> Authentication" 章节**
2. **找到 "Proxy Session Token" 字段**
3. **填入 Token**: `06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017`
4. **点击 Connect**

### 方案 3: 使用标准 MCP Inspector（不需要 Token）

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

这种方式不需要 proxy 和 token，直接使用 stdio。

### 方案 4: 禁用认证（仅用于开发）

如果不想每次输入 token，可以设置环境变量：

```bash
export DANGEROUSLY_OMIT_AUTH=true
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev wechat_server.py
```

**注意**: 这只用于本地开发，不要在生产环境使用。

## 推荐操作

### 立即尝试

1. **复制完整 URL**（包含 token）:
   ```
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017
   ```

2. **在浏览器中打开这个 URL**

3. **如果还是不行，检查浏览器控制台**:
   - 按 F12 打开开发者工具
   - 查看 Console 标签的错误信息

### 最简单的方案

如果 MCP Inspector 一直有问题，**直接在 Cursor 中使用**：

1. 编辑 `~/.cursor/mcp.json`
2. 添加服务器配置（使用 `wechat_server.py`）
3. 重启 Cursor
4. 在聊天中直接使用工具

这样就不需要处理 token 和 proxy 了。

