# 立即修复配置

## 根据你的截图，需要修改两个地方：

### 1. 修正 Arguments

**当前（错误）**:
```
article_parser python server.py
```

**应该改为**:
```
run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python server.py
```

或者如果你在项目根目录启动，可以简化为：
```
run python src/wechat_article_parser/server.py
```

### 2. Inspector Proxy Address

**当前**: 空

**解决方案**:
- 如果使用 `fastmcp dev`，它会自动设置 proxy address
- 如果手动配置，通常可以**留空**或使用默认值
- 但根据错误提示，可能需要填写

**尝试方法 1（留空）**:
- 保持 Inspector Proxy Address 为空
- 修正 Arguments 后点击 Connect

**尝试方法 2（如果需要填写）**:
- 如果留空还是报错，尝试填写：`http://localhost:6274`
- 或者查看终端中 `fastmcp dev` 的输出，看它显示的 proxy address 是什么

## 推荐操作步骤

### 步骤 1: 修正 Arguments
```
run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python server.py
```

### 步骤 2: Inspector Proxy Address
- 先尝试留空
- 点击 Connect
- 如果还是报错，尝试填写 `http://localhost:6274`

### 步骤 3: 如果还是不行

使用我创建的启动脚本（会自动处理所有配置）：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

或者直接在 Cursor 中使用（最简单，不需要 Inspector）：

1. 编辑 `~/.cursor/mcp.json`
2. 添加服务器配置
3. 重启 Cursor
4. 在聊天中直接使用

