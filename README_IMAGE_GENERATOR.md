# 即梦 Seedream 4.0 AI 画图 MCP Server

基于即梦 Seedream 4.0 模型的图像生成 MCP 服务器。

## 功能特性

- 使用即梦 Seedream 4.0 模型生成高质量图像
- 支持自定义提示词、负面提示词
- 可调节图像尺寸、生成步数、引导强度等参数
- 支持随机种子以复现结果

## 安装依赖

依赖已自动安装（fastmcp 和 requests）。

## 配置

### 1. 获取 API Key

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 开通即梦服务
3. 获取 API Key

### 2. 设置环境变量

```bash
export VOLCENGINE_API_KEY='your-api-key-here'
```

或者在 Cursor 的 MCP 配置中添加环境变量（推荐方式）。

## 使用方法

### 方式一：独立运行

```bash
export VOLCENGINE_API_KEY='your-api-key-here'
uv run python image_generator_server.py
```

### 方式二：在 Cursor 中使用

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
        "/Users/changjp/my-first-mcp-server/image_generator_server.py"
      ],
      "env": {
        "VOLCENGINE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

2. 重启 Cursor
3. 在聊天中可以使用 `generate_image` 或 `generate_image_simple` 工具

### 方式三：使用 MCP Inspector 测试

```bash
export VOLCENGINE_API_KEY='your-api-key-here'
cd /Users/changjp/my-first-mcp-server
npx @modelcontextprotocol/inspector uv run python image_generator_server.py
```

## 工具说明

### generate_image

完整功能的图像生成工具，支持所有参数：

- `prompt` (必需): 图像生成提示词
- `negative_prompt` (可选): 负面提示词
- `width` (默认 1024): 图像宽度
- `height` (默认 1024): 图像高度
- `steps` (默认 20): 生成步数
- `guidance_scale` (默认 7.5): 引导强度
- `seed` (可选): 随机种子

### generate_image_simple

简化版工具，只需提供提示词即可生成图像。

## API 参考

参考文档: https://www.volcengine.com/docs/82379/1541523

## 注意事项

1. 确保 API Key 安全，不要提交到代码仓库
2. 图像生成可能需要一些时间，请耐心等待
3. 根据实际 API 响应格式，可能需要调整代码中的 URL 和参数格式


