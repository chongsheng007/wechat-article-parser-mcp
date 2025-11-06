# MCP Inspector 手动配置指南

## 当前配置

根据你的截图，我看到：
- **Transport Type**: STDIO ✅
- **Command**: uv ✅
- **Arguments**: `run python seedream_server.py` ❌ (需要修改)

## 问题

错误提示："Connection Error - Did you add the proxy session token in Configuration?"

## 解决方案

### 步骤 1: 修正 Arguments

当前的 Arguments 是 `run python seedream_server.py`，但应该改为：

```
run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python server.py
```

或者更简单的方式：

```
run python server.py
```

但需要确保工作目录正确。

### 步骤 2: 展开 Configuration 章节

1. **点击展开 "> Configuration"**
2. 查看是否有需要配置的 proxy session token
3. 如果有相关字段，可能需要留空或使用默认值

### 步骤 3: 展开 Environment Variables（如果需要）

如果有环境变量需要设置，展开 "> Environment Variables" 并添加。

### 步骤 4: 修正配置

**推荐配置**：

```
Transport Type: STDIO
Command: uv
Arguments: run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python server.py
```

或者如果你在项目根目录：

```
Transport Type: STDIO
Command: uv
Arguments: run --directory src/wechat_article_parser python src/wechat_article_parser/server.py
```

## 更简单的方案：使用启动脚本

如果手动配置太复杂，使用我创建的启动脚本：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

这会自动启动 MCP Inspector 并正确配置。

## 最推荐：直接在 Cursor 中使用

如果 MCP Inspector 一直有问题，**直接在 Cursor 中配置**：

1. 编辑 `~/.cursor/mcp.json`
2. 添加服务器配置
3. 重启 Cursor
4. 在聊天中直接使用工具

这样就不需要 MCP Inspector 了！

