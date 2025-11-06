# MCP Inspector 正确配置

## 当前配置问题

你输入的 Arguments：
```
run--directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python server.py
```

**问题**:
1. `run--directory` 缺少空格，应该是 `run --directory`
2. 应该使用 `wechat_server.py` 而不是 `server.py`

## ✅ 正确的配置

### Arguments 字段

**正确的值**:
```
run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python wechat_server.py
```

**注意**:
- `run` 和 `--directory` 之间有**空格**
- 使用 `wechat_server.py` 而不是 `server.py`

### 其他配置

- **Transport Type**: `STDIO` ✅
- **Command**: `uv` ✅
- **Inspector Proxy Address**: `http://localhost:6277` （注意是 6277，不是 6274）
- **Proxy Session Token**: `06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017` ✅

## 修改步骤

1. **修正 Arguments**:
   - 删除当前内容
   - 输入：`run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python wechat_server.py`
   - **注意空格**：`run` 和 `--directory` 之间必须有空格

2. **修正 Inspector Proxy Address**:
   - 改为：`http://localhost:6277` （注意是 6277 端口）

3. **点击 Connect 按钮**

## 完整配置清单

```
Transport Type: STDIO
Command: uv
Arguments: run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python wechat_server.py
Inspector Proxy Address: http://localhost:6277
Proxy Session Token: 06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017
```

