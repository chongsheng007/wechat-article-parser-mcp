# 快速配置修复

## 根据你的截图，立即修改：

### Arguments 字段

**当前**: `article_parser python server.py`

**改为**:
```
run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python server.py
```

### Inspector Proxy Address 字段

**当前**: 空

**操作**:
1. 先尝试**留空**，修正 Arguments 后点击 Connect
2. 如果还是报错，尝试填写：`http://localhost:6274`

## 完整配置检查清单

- [ ] Transport Type: `STDIO`
- [ ] Command: `uv`
- [ ] Arguments: `run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python server.py`
- [ ] Inspector Proxy Address: 留空 或 `http://localhost:6274`
- [ ] Request Timeout: `300000` (可以保持默认)
- [ ] Reset Timeout on Progress: `True` (可以保持默认)
- [ ] Maximum Total Timeout: `60000` (可以保持默认)

## 如果还是不行

### 最简单的方法：使用启动脚本

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

这会自动处理所有配置。

### 最推荐的方法：直接在 Cursor 中使用

不需要 MCP Inspector，直接在 Cursor 中配置：

1. 编辑 `~/.cursor/mcp.json`
2. 添加配置（见 FINAL_SOLUTION.md）
3. 重启 Cursor
4. 在聊天中直接使用工具

