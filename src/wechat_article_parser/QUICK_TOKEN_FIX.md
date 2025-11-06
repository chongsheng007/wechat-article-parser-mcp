# 快速修复：使用 Session Token

## 当前状态

✅ 服务器已启动
✅ Session Token 已生成: `06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017`

## 立即操作

### 步骤 1: 使用完整 URL

直接复制这个完整 URL 到浏览器：

```
http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017
```

### 步骤 2: 或者在 MCP Inspector 中配置 Token

如果你已经打开了 MCP Inspector 页面：

1. **展开 "> Authentication" 章节**
2. **找到 "Proxy Session Token" 字段**
3. **粘贴 Token**: `06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017`
4. **Inspector Proxy Address** 应该是: `http://localhost:6277`
5. **点击 Connect**

## 如果还是不行

### 检查浏览器控制台

1. 按 `F12` 打开开发者工具
2. 查看 Console 标签
3. 查看 Network 标签
4. 告诉我具体的错误信息

### 或者使用标准方式（不需要 Token）

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

### 或者直接在 Cursor 中使用（最推荐）

不需要 MCP Inspector，直接在 Cursor 中配置使用，最简单。

