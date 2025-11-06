# Seedream 4.0 图像生成 MCP Server

使用即梦 Seedream 4.0 模型 API 生成高质量图像的 MCP 服务器。

## 功能特性

- 🎨 使用即梦 Seedream 4.0 模型生成高质量图像
- 🎯 支持自定义提示词、负面提示词
- 📐 可调节图像尺寸、生成步数、引导强度等参数
- 🎲 支持随机种子以复现结果
- 🚀 简化版工具快速生成图像

## 安装

### 依赖安装

```bash
cd /Users/changjp/my-first-mcp-server
uv pip install fastmcp requests pydantic
```

## 配置

### 1. 获取 API Key

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 开通即梦服务
3. 获取 API Key

### 2. 设置环境变量

```bash
export SEEDREAM_API_KEY='your-api-key-here'
```

## 使用方法

### 方式一：在 Cursor 中使用

1. 编辑 `~/.cursor/mcp.json`，添加以下配置：

```json
{
  "mcpServers": {
    "seedream-image-generator": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/changjp/my-first-mcp-server",
        "run",
        "python",
        "/Users/changjp/my-first-mcp-server/src/seedream_image_generator/server.py"
      ],
      "env": {
        "SEEDREAM_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

2. 重启 Cursor
3. 在聊天中可以使用 `generate_image` 或 `generate_image_simple` 工具

### 方式二：使用 fastmcp dev 调试

```bash
export SEEDREAM_API_KEY='your-api-key-here'
cd /Users/changjp/my-first-mcp-server
fastmcp dev src/seedream_image_generator/server.py
```

### 方式三：使用 MCP Inspector 测试

```bash
export SEEDREAM_API_KEY='your-api-key-here'
cd /Users/changjp/my-first-mcp-server
npx @modelcontextprotocol/inspector uv run python src/seedream_image_generator/server.py
```

## 工具说明

### generate_image

完整功能的图像生成工具，支持所有参数：

- `prompt` (必需): 图像生成提示词
- `negative_prompt` (可选): 负面提示词
- `width` (默认 1024): 图像宽度
- `height` (默认 1024): 图像高度
- `steps` (默认 30): 生成步数
- `guidance_scale` (默认 7.5): 引导强度
- `seed` (可选): 随机种子

### generate_image_simple

简化版工具，只需提供提示词即可生成图像。

## 项目结构

```
src/seedream_image_generator/
├── server.py              # MCP 服务器主文件
├── tools/
│   ├── generate_image.py
│   └── generate_image_simple.py
└── utils/
    ├── api_client.py      # API 请求客户端
    ├── errors.py          # 错误处理
    └── formatters.py      # 响应格式化
```

## API 参考

参考文档: https://www.volcengine.com/docs/82379/1541523

## 注意事项

1. 确保 API Key 安全，不要提交到代码仓库
2. 图像生成可能需要一些时间，请耐心等待
3. 根据实际 API 响应格式，可能需要调整代码中的 URL 和参数格式
4. 当前模型名称可能需要根据实际 API 文档调整

## 已知问题

1. **模型名称**: 当前使用 `Seedream-4.0`，可能需要根据实际 API 文档调整
2. **API 权限**: 确保 API Key 有权限访问 Seedream 4.0 模型
3. **错误处理**: 如果遇到 500 错误，可能是权限或配置问题

## 开发

### 代码规范

- 使用 Pydantic 进行类型安全的输入验证
- 所有错误使用 MCPError 及其子类
- 遵循 FastMCP 最佳实践

### 测试

```bash
# 语法检查
python3 -m py_compile src/seedream_image_generator/**/*.py

# 使用 fastmcp dev 调试
fastmcp dev src/seedream_image_generator/server.py
```

## 许可证

MIT


