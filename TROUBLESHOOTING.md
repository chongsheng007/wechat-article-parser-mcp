# 故障排除指南

## 常见问题

### 1. "Missing session ID" 错误

**错误信息**:
```
响应状态码: 400
响应内容: {"jsonrpc":"2.0","id":"server-error","error":{"code":-32600,"message":"Bad Request: Missing session ID"}}
```

**原因**:
- MCP Inspector 的传输协议配置问题
- 使用了错误的启动方式

**解决方案**:

#### 方式 1: 使用 `fastmcp dev`（推荐）
```bash
export SEEDREAM_API_KEY="your-api-key"
export API_BASE_URL="https://ark.cn-beijing.volces.com"
export REQUEST_TIMEOUT="60"

uv run fastmcp dev src/seedream_image_generator/server.py
```

这会自动启动 MCP Inspector，访问 `http://localhost:6274`

#### 方式 2: 使用启动脚本
```bash
chmod +x start_dev.sh
./start_dev.sh
```

#### 方式 3: 手动启动 MCP Inspector（如果方式 1 不行）
```bash
export SEEDREAM_API_KEY="your-api-key"
export API_BASE_URL="https://ark.cn-beijing.volces.com"
export REQUEST_TIMEOUT="60"

npx @modelcontextprotocol/inspector --transport stdio -- uv run python src/seedream_image_generator/server.py
```

**重要**: 确保使用 `--transport stdio` 参数

### 2. "ModelNotOpen" 错误

**错误信息**:
```
错误代码: ModelNotOpen
错误消息: Your account 2101246886 has not activated the model doubao-seedream-4-0-250828. Please activate the model service in the Ark Console.
```

**原因**:
- 模型服务未在 Ark Console 激活

**解决方案**:
1. 登录 Ark Console: https://console.volcengine.com/ark/
2. 进入模型管理页面
3. 激活模型: `doubao-seedream-4-0-250828`
4. 等待 5-30 分钟生效
5. 重新测试

### 3. "Extra inputs are not permitted" 错误

**错误信息**:
```
1 validation error for call[generate_image] input.format Extra inputs are not permitted
```

**原因**:
- Pydantic 模型配置为 `extra: "forbid"`，拒绝了额外字段

**解决方案**:
已修复！所有工具的输入模型已更新为 `extra: "ignore"`，会忽略 MCP Inspector 添加的额外字段（如 `format`）。

### 4. 测试工具功能

如果 MCP Inspector 有问题，可以直接测试工具：

```bash
# 测试 generate_image
export SEEDREAM_API_KEY="your-api-key"
uv run python test_generate_image_simple.py

# 测试所有工具
uv run python test_all_tools.py
```

### 5. 在 Cursor 中使用

如果 MCP Inspector 有问题，可以直接在 Cursor 聊天中使用：

1. 确保 MCP 服务器已配置到 Cursor
2. 在聊天中直接说：
   - "使用即梦生成一只小猫的图片"
   - "帮我生成一张风景画"

Cursor 会自动调用 `generate_image` 工具。

## 调试技巧

### 查看详细日志

在 `api_client.py` 中，错误时会输出详细的调试信息：
- 请求 URL
- 请求头
- 请求体
- 响应状态码
- 响应内容

### 验证环境变量

```bash
echo $SEEDREAM_API_KEY
echo $API_BASE_URL
echo $REQUEST_TIMEOUT
```

### 检查服务器状态

```bash
# 检查服务器是否可以正常导入
uv run python -c "from src.seedream_image_generator.server import mcp; print('✅ 服务器模块正常')"
```

## 联系支持

如果问题持续存在：
1. 检查所有环境变量是否正确设置
2. 确认模型服务已激活
3. 查看详细的错误日志（包含 logid）
4. 联系技术支持并提供 logid


